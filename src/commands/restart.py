import discord
from discord import app_commands
from discord.ext import commands

from config import settings


class RestartCommand(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="restart", description="Reinicia el bot.")
    async def restart(self, interaction: discord.Interaction) -> None:
        if interaction.user.id not in settings.dev_user_ids:
            await interaction.response.send_message(
                "No tienes permiso para usar este comando.",
                ephemeral=True,
            )
            return

        await interaction.response.send_message(
            "Reinicio solicitado. El bot se cerrará; Docker lo volverá a iniciar.",
            ephemeral=True,
        )
        await self.bot.close()


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(RestartCommand(bot))
