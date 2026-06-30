"""
Module: events.dlq

Purpose:
Dead Letter Queue (DLQ) handler for unprocessable events.

Responsibilities:
- Move repeatedly failing messages from the primary stream to a DLQ stream.
- Acknowledge the poison pill message in the primary stream to unblock consumers.

Dependencies:
- redis.asyncio, backend.db.cache.redis_client.
- backend.shared.exceptions.infrastructure.

Owner:
SentinelVision
"""

import logging

from redis.exceptions import ConnectionError, RedisError

from backend.db.cache.redis_client import get_redis
from backend.shared.exceptions.infrastructure import EventBusError

logger = logging.getLogger(__name__)


class DeadLetterQueue:
    """Manages moving poison pill messages to a Dead Letter Queue."""

    def __init__(self) -> None:
        """Initialise with the global Redis client."""
        self.client = get_redis()

    async def move_to_dlq(self, source_topic: str, group_name: str, message_id: str, raw_payload: bytes | str, error_msg: str) -> None:
        """Move a failed message to the DLQ and ack it in the source stream.
        
        Args:
            source_topic: Original stream name.
            group_name: Consumer group that failed.
            message_id: ID of the failed message.
            raw_payload: The raw event payload.
            error_msg: The exception or reason for failure.
        """
        dlq_topic = f"{source_topic}:dlq"
        
        try:
            # 1. Add to DLQ stream
            await self.client.xadd(
                name=dlq_topic,
                fields={
                    "payload": raw_payload,
                    "original_id": message_id,
                    "error": error_msg,
                    "group": group_name,
                },
                maxlen=10000,
                approximate=True,
            )
            
            # 2. Ack in original stream so the consumer group can advance
            await self.client.xack(source_topic, group_name, message_id)
            
            logger.warning(f"Moved message {message_id} from {source_topic} to {dlq_topic}. Reason: {error_msg}")
            
        except (ConnectionError, RedisError) as e:
            logger.error(f"Critical failure moving message {message_id} to DLQ {dlq_topic}: {e}")
            raise EventBusError(f"DLQ operation failed: {e}", topic=dlq_topic, operation="dlq_move") from e
