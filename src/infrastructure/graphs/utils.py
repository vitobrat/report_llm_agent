from src.depends import get_langfuse_handler
import asyncio
import time
from collections import deque


# Глобальный rate limiter
class RateLimiter:
    def __init__(self, rate=1, interval=1.5):
        self.rate = rate  # Количество запросов
        self.interval = interval  # Временной интервал в секундах
        self.timestamps = deque()
        self.lock = asyncio.Lock()

    async def wait(self):
        async with self.lock:
            now = time.monotonic()

            # Удаляем старые временные метки
            while self.timestamps and self.timestamps[
                0] <= now - self.interval:
                self.timestamps.popleft()

            # Проверяем, не превышен ли лимит
            if len(self.timestamps) >= self.rate:
                # Вычисляем время ожидания
                sleep_for = self.interval - (now - self.timestamps[0])
                await asyncio.sleep(sleep_for)
                now = time.monotonic()  # Обновляем время после сна

            # Добавляем новую временную метку
            self.timestamps.append(now)


# Создаем глобальный экземпляр rate limiter
rate_limiter = RateLimiter(rate=1, interval=2)


async def llm_call(llm, prompt, **kwargs):
    """Вызов LLM с ограничением скорости"""
    await rate_limiter.wait()
    return await llm.ainvoke(prompt, **kwargs)