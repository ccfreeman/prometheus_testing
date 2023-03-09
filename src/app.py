import logging
import asyncio
from random import randint
import uvicorn
from pydantic import BaseModel
from fastapi import FastAPI, APIRouter
from starlette.responses import JSONResponse
from starlette_exporter import PrometheusMiddleware, handle_metrics
from prometheus_client import Summary
from prometheus_client import Counter, Gauge


logging.basicConfig(level=logging.DEBUG)


class SleepyTime(BaseModel):
    sleep_time: int


class App:

    app = FastAPI(title="SleepApp")
    app.add_middleware(PrometheusMiddleware, app_name="sleeper_app", prefix="sleeper_app")
    app.add_route("/metrics", handle_metrics)

    def __init__(self):
        self._total_time_slept = 0

        sleep_router = APIRouter(
            tags = ['Sleep'],
            prefix = '/sleep'
        )
        sleep_router.add_api_route(
            path = "/time_slept",
            endpoint = self.retrieve_total_time_slept,
            methods = ["GET"]
        )
        sleep_router.add_api_route(
            path = "",
            endpoint = self.go_to_sleep,
            methods = ["POST"]
        )
        self.app.include_router(sleep_router)

    @property
    def time_slept(self) -> int:
        return self._total_time_slept
    
    async def retrieve_total_time_slept(self) -> int:
        logging.info("Received request for total time slept")
        return JSONResponse(content={"total": self.time_slept})

    # async def count_the_sheep(self) -> JSONResponse:
    #     sleep_time = randint(1, 10)
    #     logging.info("Sending count of %d seconds", sleep_time)
    #     return JSONResponse(content={"sleep_time": sleep_time})
    
    async def go_to_sleep(self, sleepy_time: SleepyTime) -> JSONResponse:
        logging.info("Sleeping for %d seconds", sleepy_time.sleep_time)
        await asyncio.sleep(sleepy_time.sleep_time)
        self._total_time_slept += sleepy_time.sleep_time
        return JSONResponse(content={"sleep_time": sleepy_time.sleep_time})


if __name__ == "__main__":
    import os
    METRICS_PORT = int(os.environ.get("METRICS_PORT", 8000))
    sleeper_app = App()
    uvicorn.run(sleeper_app.app, host="0.0.0.0", port=METRICS_PORT)
