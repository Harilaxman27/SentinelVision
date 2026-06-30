"""
Module: events.consumer_group

Purpose:
Manages Redis Streams consumer groups, pending message recovery, and scaling.

Responsibilities:
- Claim pending messages (PEL) from crashed consumers.
- Expose a reliable message processing loop with auto-retry.

Dependencies:
- redis.asyncio, backend.db.cache.redis_client.
- backend.events.interfaces, backend.events.dlq.

Owner:
SentinelVision
"""

import asyncio
import logging
from typing import Awaitable, Callable

from redis.exceptions import ConnectionError, RedisError

from backend.db.cache.redis_client import get_redis
from backend.events.dlq import DeadLetterQueue
from backend.events.interfaces import IEventBus
from backend.events.schemas import BaseEvent

logger = logging.getLogger(__name__)


class ConsumerGroupManager:
    """Manages reliable consumption and recovery for a consumer group."""

    def __init__(self, bus: IEventBus, topic: str, group_name: str, consumer_name: str):
        self.bus = bus
        self.client = get_redis()
        self.topic = topic
        self.group_name = group_name
        self.consumer_name = consumer_name
        self.dlq = DeadLetterQueue()
        self.max_retries = 3

    async def start_processing(self, handler: Callable[[BaseEvent], Awaitable[None]]) -> None:
        """Start the main processing loop.
        
        Will first attempt to recover pending messages, then switch to waiting for new ones.
        """
        logger.info(f"Starting consumer {self.consumer_name} for group {self.group_name} on {self.topic}")
        
        # 1. Process Pending (PEL) first to recover from crashes
        await self._claim_and_process_pending(handler)
        
        # 2. Subscribe to new messages
        async for msg_id, event in self.bus.subscribe(self.topic, self.group_name, self.consumer_name):
            await self._process_with_retry(msg_id, event, handler)

    async def _claim_and_process_pending(self, handler: Callable[[BaseEvent], Awaitable[None]]) -> None:
        """Claim messages that were sent to a consumer but never acked."""
        try:
            # Look for messages pending for more than 10 seconds across ALL consumers in the group
            pending = await self.client.xpending_range(self.topic, self.group_name, min="-", max="+", count=100)
            
            for msg_info in pending:
                msg_id = msg_info["message_id"]
                idle_time_ms = msg_info["time_since_delivered"]
                delivery_count = msg_info["times_delivered"]
                
                if idle_time_ms > 10000:
                    logger.info(f"Claiming idle message {msg_id} (delivered {delivery_count} times)")
                    
                    # Claim it for this consumer
                    claimed = await self.client.xclaim(
                        self.topic, 
                        self.group_name, 
                        self.consumer_name, 
                        min_idle_time=10000, 
                        message_ids=[msg_id]
                    )
                    
                    for _, fields in claimed:
                        # In XCLAIM, the return is [(msg_id, fields), ...]
                        # Parse and process
                        msg_id_str = msg_id.decode("utf-8") if isinstance(msg_id, bytes) else str(msg_id)
                        
                        if delivery_count >= self.max_retries:
                            # Move straight to DLQ
                            await self.dlq.move_to_dlq(
                                self.topic, self.group_name, msg_id_str, 
                                fields.get(b"payload", b""), f"Max retries ({delivery_count}) exceeded."
                            )
                            continue
                            
                        # Re-parse and try again
                        from backend.events.schemas import parse_event
                        try:
                            event = parse_event(fields.get(b"payload", b""))
                            await self._process_with_retry(msg_id_str, event, handler)
                        except Exception as e:
                            logger.error(f"Failed to parse claimed message {msg_id_str}: {e}")
                            await self.dlq.move_to_dlq(self.topic, self.group_name, msg_id_str, fields.get(b"payload", b""), str(e))
                            
        except (ConnectionError, RedisError) as e:
            logger.error(f"Failed to process pending messages for {self.topic}: {e}")

    async def _process_with_retry(self, msg_id: str, event: BaseEvent, handler: Callable[[BaseEvent], Awaitable[None]]) -> None:
        """Attempt to process a message with backoff. Move to DLQ on repeated failure."""
        for attempt in range(1, self.max_retries + 1):
            try:
                await handler(event)
                await self.bus.ack(self.topic, self.group_name, msg_id)
                return  # Success
            except Exception as e:
                logger.warning(f"Handler failed on attempt {attempt} for message {msg_id}: {e}")
                if attempt == self.max_retries:
                    # Final failure, move to DLQ
                    await self.dlq.move_to_dlq(
                        self.topic, self.group_name, msg_id, 
                        event.to_json_str(), f"Handler exception: {e}"
                    )
                    return
                # Exponential backoff
                await asyncio.sleep(2 ** attempt)
