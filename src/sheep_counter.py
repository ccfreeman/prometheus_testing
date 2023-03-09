import logging
import random

from prometheus_client import Counter


logging.basicConfig(level=logging.DEBUG)


async def main():
    counter = Counter(name="sheep_counted", documentation="Number of sheep counted")
    for i in range(1, 100):
        counter.inc()
        logging.info("Sheep counted: %d", i)
        await asyncio.sleep(random.randint(1, 10))


if __name__ == "__main__":
    import os
    import asyncio
    # Start up the server to expose the metrics
    from prometheus_client import start_http_server

    METRICS_PORT = int(os.environ.get("METRICS_PORT", 8000))
    start_http_server(METRICS_PORT, addr="0.0.0.0")

    logging.info("Trying to sleep")
    asyncio.run(main())
    logging.info("zzzzz")
