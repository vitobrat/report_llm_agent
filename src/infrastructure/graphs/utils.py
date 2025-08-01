import asyncio
import time
from collections import deque

from src.infrastructure.graphs.schema import MetadataClass


class RateLimiter:
    def __init__(self, rate=1, interval=1.5):
        self.rate = rate
        self.interval = interval
        self.timestamps = deque()
        self.lock = asyncio.Lock()

    async def wait(self):
        async with self.lock:
            now = time.monotonic()

            while self.timestamps and self.timestamps[
                0] <= now - self.interval:
                self.timestamps.popleft()

            if len(self.timestamps) >= self.rate:
                sleep_for = self.interval - (now - self.timestamps[0])
                await asyncio.sleep(sleep_for)
                now = time.monotonic()

            self.timestamps.append(now)


rate_limiter = RateLimiter(rate=1, interval=4)


async def llm_call(llm, prompt, **kwargs):
    """Вызов LLM с ограничением скорости"""
    await rate_limiter.wait()
    return await llm.ainvoke(prompt, **kwargs)


def merge_metadata(first: MetadataClass, second: MetadataClass) -> MetadataClass:
    return MetadataClass(
        output_tokens=first.output_tokens + second.output_tokens,
        input_tokens=first.input_tokens + second.input_tokens
    )