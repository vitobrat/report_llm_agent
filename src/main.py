import logging
import uvicorn
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

from src.depends import get_settings
from src.domains.llm_agent.app.requests.router import router as generate_analysts_router

apiV1 = FastAPI()
apiV1.include_router(generate_analysts_router)

limiter = Limiter(key_func=get_remote_address)
app = FastAPI(
    default_response_class=ORJSONResponse
)
app.mount("/api/v1", apiV1)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

settings = get_settings()

if __name__ == '__main__':
    logging.info('LLM-Manager started!')
    uvicorn.run("main:app",
                host="0.0.0.0",
                port=settings.port,
                log_level=settings.log_level,
                workers=settings.workers_number,
                loop="asyncio")
