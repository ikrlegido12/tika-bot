import discord
from discord.ext import commands

from config import settings


class TikaBot(commands.Bot):
    def __init__(self) -> None:
        super().__init__(
            command_prefix=commands.when_mentioned,
            intents=discord.Intents.default(),
        )

    async def setup_hook(self) -> None:
        await self.load_extension("commands.ping")
        await self.load_extension("commands.restart")

        if settings.test_guild_id is not None:
            test_guild = discord.Object(id=settings.test_guild_id)
            self.tree.copy_global_to(guild=test_guild)
            synced_commands = await self.tree.sync(guild=test_guild)
            print(f"Synced {len(synced_commands)} command(s) to test guild.")
            return

        synced_commands = await self.tree.sync()
        print(f"Synced {len(synced_commands)} global command(s).")
