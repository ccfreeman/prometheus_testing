import logging
import asyncio
from random import randint
import aiohttp


logging.basicConfig(level=logging.DEBUG)


async def get_sleep_time(
    url: str,
    session: aiohttp.ClientSession
) -> int:
    sleep_time = randint(1, 10)
    logging.info("Sending count of %d seconds", sleep_time)
    async with session.post(url, json={"sleep_time": sleep_time}) as resp:
        return (await resp.json())["sleep_time"]


async def main() -> None:
    await asyncio.sleep(3)
    async with aiohttp.ClientSession(
        connector = aiohttp.TCPConnector(ssl=False),
        timeout = aiohttp.ClientTimeout(total=10)
    ) as session:
        while True:
            sleep_time = await get_sleep_time("http://app:8080/sleep", session)
            logging.info("Got response from app of '%d'", sleep_time)
            await asyncio.sleep(.1)
            

if __name__ == "__main__":
    asyncio.run(main())
