import logging
from typing import Any

import discord
from discord import app_commands
from discord.ext import commands

from config import settings

logger = logging.getLogger(__name__)


class TikaBot(commands.Bot):
    def __init__(self) -> None:
        super().__init__(
            command_prefix=commands.when_mentioned,
            intents=discord.Intents.default(),
        )
        self.tree.on_error = self.on_app_command_error

    async def setup_hook(self) -> None:
        await self.load_extension("commands.ping")
        await self.load_extension("commands.restart")
        logger.info("Loaded command extensions")

        if settings.test_guild_id is not None:
            test_guild = discord.Object(id=settings.test_guild_id)
            self.tree.copy_global_to(guild=test_guild)
            synced_commands = await self.tree.sync(guild=test_guild)
            logger.info("Synced %d command(s) to test guild %s", len(synced_commands), test_guild.id)
            return

        synced_commands = await self.tree.sync()
        logger.info("Synced %d global command(s)", len(synced_commands))

    async def on_ready(self) -> None:
        user_id = self.user.id if self.user else "unknown"
        logger.info("Connected to Discord as %s (user ID %s)", self.user, user_id)

    async def on_interaction(self, interaction: discord.Interaction) -> None:
        interaction_data = interaction.data or {}
        command_name = interaction_data.get("name")
        logger.info(
            "Received %s interaction%s from user %s in guild %s",
            interaction.type.name,
            f" for command /{command_name}" if command_name else "",
            interaction.user.id,
            interaction.guild_id or "DM",
        )

    async def on_app_command_completion(
        self,
        interaction: discord.Interaction,
        command: app_commands.Command[Any, ..., Any] | app_commands.ContextMenu,
    ) -> None:
        logger.info(
            "Command /%s completed for user %s in guild %s",
            command.qualified_name if isinstance(command, app_commands.Command) else command.name,
            interaction.user.id,
            interaction.guild_id or "DM",
        )
        if interaction.extras.pop("restart_requested", False):
            logger.info("Closing bot after completed /restart command")
            await self.close()

    async def on_app_command_error(
        self,
        interaction: discord.Interaction,
        error: app_commands.AppCommandError,
    ) -> None:
        command = interaction.command
        command_name = getattr(command, "qualified_name", "unknown")
        logger.error(
            "Command /%s failed for user %s in guild %s",
            command_name,
            interaction.user.id,
            interaction.guild_id or "DM",
            exc_info=(type(error), error, error.__traceback__),
        )
        if not interaction.response.is_done():
            await interaction.response.send_message(
                "Ha ocurrido un error al ejecutar el comando.",
                ephemeral=True,
            )

    async def on_error(self, event_method: str, /, *args: Any, **kwargs: Any) -> None:
        logger.exception(
            "Unhandled error in Discord event %s (%d positional and %d keyword arguments)",
            event_method,
            len(args),
            len(kwargs),
        )
