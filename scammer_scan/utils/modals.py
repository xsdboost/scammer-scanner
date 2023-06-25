from typing import Tuple

import discord
from discord import Member

from scammer_scan.orm.models import DiscordUser


def EmbedMessages(offender: Tuple[Member, DiscordUser]) -> discord.Embed:

    return discord.Embed(
        title=f"Scammer found!",
        description=(
            f"The scammer's discord link is **<@{offender[0].id}>**\n"
            f"Scammer named **{offender[0].name}** should be banned , "
            f"impersonating admin **{offender[1].name}**, using "
            f"both using display_name **{offender[0].display_name}**, "
        ),
        color=0x00FF00,
    )
