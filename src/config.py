import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parents[1] / ".env")


@dataclass(frozen=True)
class Settings:
    discord_token: str
    test_guild_id: int | None
    dev_user_ids: frozenset[int]


def load_settings() -> Settings:
    token = os.getenv("DISCORD_TOKEN")
    if not token:
        raise RuntimeError("Missing required environment variable: DISCORD_TOKEN")

    test_guild_id_value = os.getenv("TEST_GUILD_ID")
    if test_guild_id_value:
        try:
            test_guild_id = int(test_guild_id_value)
        except ValueError as error:
            raise RuntimeError("TEST_GUILD_ID must be a valid Discord server ID") from error
        if test_guild_id <= 0:
            raise RuntimeError("TEST_GUILD_ID must be a positive Discord server ID")
    else:
        test_guild_id = None

    dev_user_ids: set[int] = set()
    for user_id_value in os.getenv("DEV_USER_IDS", "").split(","):
        user_id_value = user_id_value.strip()
        if not user_id_value:
            continue
        try:
            user_id = int(user_id_value)
        except ValueError as error:
            raise RuntimeError("DEV_USER_IDS must contain comma-separated Discord user IDs") from error
        if user_id <= 0:
            raise RuntimeError("DEV_USER_IDS must contain positive Discord user IDs")
        dev_user_ids.add(user_id)

    return Settings(
        discord_token=token,
        test_guild_id=test_guild_id,
        dev_user_ids=frozenset(dev_user_ids),
    )


settings = load_settings()
