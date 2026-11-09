# En el discord dev portal, tener activado 'message_content' intent.
import asyncio
import os
import signal
import discord
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parents[1] / ".env")
token = os.getenv('DISCORD_TOKEN')
if not token:
    raise RuntimeError("Missing required environment variable: DISCORD_TOKEN")

client_id = os.getenv('CLIENT_ID')


class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        if message.content == '!ping':
            await message.channel.send('pong!')
        print(f'Message from {message.author}: {message.content}')

intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)


async def main():
    loop = asyncio.get_running_loop()

    def request_shutdown():
        print("Shutdown signal received; closing Discord connection...")
        asyncio.create_task(client.close())

    for shutdown_signal in (signal.SIGINT, signal.SIGTERM):
        try:
            loop.add_signal_handler(shutdown_signal, request_shutdown)
        except NotImplementedError:
            signal.signal(
                shutdown_signal,
                lambda *_: loop.call_soon_threadsafe(request_shutdown),
            )

    async with client:
        await client.start(token)


asyncio.run(main())
