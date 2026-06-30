"""
Module: events.redis_bus

Purpose:
Concrete implementation of IEventBus using Redis Streams.

Responsibilities:
- Publish events to Redis Streams (XADD).
- Subscribe to events using consumer groups (XREADGROUP).
- Handle payload serialisation and message ID tracking.

Dependencies:
- redis.asyncio, backend.db.cache.redis_client.
- backend.events.interfaces, backend.events.schemas.
- backend.shared.exceptions.infrastructure.

Owner:
SentinelVision
"""

import logging
from typing import AsyncGenerator

from redis.exceptions import ConnectionError, RedisError

from backend.db.cache.redis_client import get_redis
from backend.events.interfaces import IEventBus
from backend.events.schemas import BaseEvent, parse_event
from backend.shared.exceptions.infrastructure import EventBusError

logger = logging.getLogger(__name__)


class RedisEventBus(IEventBus):
    """Event Bus implementation backed by Redis Streams."""

    def __init__(self) -> None:
        """Initialise with the global Redis client."""
        # get_redis() must be called after init_redis() during startup
        self.client = get_redis()

    async def publish(self, topic: str, event: BaseEvent) -> str:
        """Publish an event to a Redis stream.
        
        Uses XADD. Caps the stream length to approximately 10,000 to prevent OOM.
        """
        payload = event.to_json_str()
        try:
            # Add to stream, maxlen limits stream size to prevent unbounded growth
            message_id = await self.client.xadd(
                name=topic,
                fields={"payload": payload},
                maxlen=10000,
                approximate=True,
            )
            return message_id.decode("utf-8") if isinstance(message_id, bytes) else str(message_id)
        except (ConnectionError, RedisError) as e:
            logger.error(f"Failed to publish event {event.event_id} to {topic}: {e}")
            raise EventBusError(f"Publish failed: {e}", topic=topic, operation="xadd") from e

    async def _ensure_group(self, topic: str, group_name: str) -> None:
        """Ensure the consumer group exists, creating it at the end of the stream if it doesn't."""
        try:
            await self.client.xgroup_create(name=topic, groupname=group_name, id="$", mkstream=True)
        except redis.exceptions.ResponseError as e:
            # BUSYGROUP means the group already exists, which is fine
            if "BUSYGROUP" not in str(e):
                raise EventBusError(f"Failed to create group {group_name}: {e}", topic=topic, operation="xgroup_create") from e

    async def subscribe(self, topic: str, group_name: str, consumer_name: str) -> AsyncGenerator[tuple[str, BaseEvent], None]:
        """Subscribe to a Redis stream using a consumer group.
        
        Yields (message_id, BaseEvent) tuples. 
        Blocks until new messages arrive.
        """
        await self._ensure_group(topic, group_name)

        while True:
            try:
                # Block for up to 5 seconds waiting for new messages (id=">")
                streams = await self.client.xreadgroup(
                    groupname=group_name,
                    consumername=consumer_name,
                    streams={topic: ">"},
                    count=10,
                    block=5000,
                )

                for stream_name, messages in streams:
                    for message_id, fields in messages:
                        msg_id_str = message_id.decode("utf-8") if isinstance(message_id, bytes) else str(message_id)
                        payload = fields.get(b"payload") or fields.get("payload")
                        
                        if payload is None:
                            logger.warning(f"Empty payload for message {msg_id_str} in {topic}. Acking and skipping.")
                            await self.ack(topic, group_name, msg_id_str)
                            continue

                        try:
                            event = parse_event(payload)
                            yield msg_id_str, event
                        except Exception as e:
                            logger.error(f"Failed to parse event {msg_id_str} from {topic}: {e}")
                            # In a real system, this should go to a Dead Letter Queue (DLQ).
                            # For now, we ack to prevent a poison pill loop.
                            await self.ack(topic, group_name, msg_id_str)

            except (ConnectionError, RedisError) as e:
                logger.error(f"Connection error in subscriber for {topic}: {e}. Retrying in 5s.")
                import asyncio
                await asyncio.sleep(5.0)

    async def ack(self, topic: str, group_name: str, message_id: str) -> None:
        """Acknowledge a message using XACK."""
        try:
            await self.client.xack(topic, group_name, message_id)
        except (ConnectionError, RedisError) as e:
            logger.error(f"Failed to ack message {message_id} in {topic}: {e}")
            raise EventBusError(f"Ack failed: {e}", topic=topic, operation="xack") from e
