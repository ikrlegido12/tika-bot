import asyncio
import signal

from bot import TikaBot
from config import settings


async def main() -> None:
    bot = TikaBot()
    loop = asyncio.get_running_loop()
    shutdown_requested = False

    def request_shutdown() -> None:
        nonlocal shutdown_requested
        if shutdown_requested:
            return
        shutdown_requested = True
        print("Shutdown signal received; closing Discord connection...")
        asyncio.create_task(bot.close())

    for shutdown_signal in (signal.SIGINT, signal.SIGTERM):
        try:
            loop.add_signal_handler(shutdown_signal, request_shutdown)
        except NotImplementedError:
            signal.signal(
                shutdown_signal,
                lambda *_: loop.call_soon_threadsafe(request_shutdown),
            )

    async with bot:
        await bot.start(settings.discord_token)


if __name__ == "__main__":
    asyncio.run(main())
