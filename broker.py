# broker.py
import asyncio
from loguru import logger

from taskiq_redis import RedisAsyncResultBackend, RedisStreamBroker

result_backend = RedisAsyncResultBackend(
    redis_url="redis://redis_task:6379",
)

# Or you can use PubSubBroker if you need broadcasting
# Or ListQueueBroker if you don't want acknowledges
broker = RedisStreamBroker(
    url="redis://redis_task:6379",
).with_result_backend(result_backend)


@broker.task
async def best_task_ever() -> None:
    """Solve all problems in the world."""
    await asyncio.sleep(5.5)
    logger.info("All problems are solved!")


async def main():
    task = await best_task_ever.kiq()
    task_info = await task.wait_result()
    logger.info(f"Task is done! {task_info}")


if __name__ == "__main__":
    asyncio.run(main())
