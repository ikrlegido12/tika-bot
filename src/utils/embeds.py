from collections.abc import Iterable
from datetime import datetime

import discord


EmbedField = tuple[str, str, bool]


def create_embed(
    title: str,
    description: str | None = None,
    *,
    color: discord.Colour | int | None = None,
    fields: Iterable[EmbedField] = (),
    footer: str | None = None,
    timestamp: datetime | None = None,
) -> discord.Embed:
    embed = discord.Embed(
        title=title,
        description=description,
        color=color if color is not None else discord.Colour.blurple(),
        timestamp=timestamp,
    )

    for name, value, inline in fields:
        embed.add_field(name=name, value=value, inline=inline)

    if footer is not None:
        embed.set_footer(text=footer)

    return embed
