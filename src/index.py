import asyncio
import logging
import signal
import sys

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    stream=sys.stdout,
)

logger = logging.getLogger(__name__)

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
        logger.info("Shutdown signal received; closing Discord connection")
        asyncio.create_task(bot.close())

    for shutdown_signal in (signal.SIGINT, signal.SIGTERM):
        try:
            loop.add_signal_handler(shutdown_signal, request_shutdown)
        except NotImplementedError:
            signal.signal(
                shutdown_signal,
                lambda *_: loop.call_soon_threadsafe(request_shutdown),
            )

    try:
        async with bot:
            logger.info("Starting bot; %d developer user ID(s) loaded", len(settings.dev_user_ids))
            await bot.start(settings.discord_token)
    except Exception:
        logger.exception("Bot startup or connection failed")
        raise


if __name__ == "__main__":
    asyncio.run(main())
