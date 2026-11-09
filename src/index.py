# En el discord dev portal, tener activado 'message_content' intent.
import os
import discord
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parents[1] / ".env")
token = os.getenv('DISCORD_TOKEN')
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
client.run(token)
