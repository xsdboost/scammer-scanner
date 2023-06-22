from typing import List
import discord
from discord import Guild
from pony.orm import db_session, select

from secrets.credentials import bot_key
from watcher.domain.usecases import members_in_admin_list
from watcher.orm.models import db, DiscordUser
from discord.ext import commands, tasks

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

guild_id: int = 999513287962148924
channel_id: int = 1000170281245093978

client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix="/", client=client, intents=intents)

db.bind(provider="sqlite", filename="datastore/moderators.sqlite", create_db=True)
db.generate_mapping(create_tables=True)


async def scan_matching_user(
    bot, guild_id: int, channel_id: int, from_beginning: bool = False
) -> None:
    guild: Guild = bot.get_guild(guild_id)
    channel = guild.get_channel(channel_id)

    if guild is None:
        raise Exception("Guild not found")

    with db_session:
        admin_users: List[DiscordUser] = select(user for user in DiscordUser).fetch()

    offending_members = members_in_admin_list(
        list(guild.members), admin_users, from_beginning=from_beginning
    )

    if len(offending_members) != 0:
        for offender in offending_members:
            embed = discord.Embed(
                title=f"Scammer found!",
                description=(
                    f"The scammer's discord link is **<@{offender[0].id}>**\n"
                    f"Scammer named **{offender[0].name}** should be banned , "
                    f"impersonating admin **{offender[1].name}**, using "
                    f"both using display_name **{offender[0].display_name}**, "
                ),
                color=0x00FF00,
            )
            await channel.send(embed=embed)

    #await channel.send(f"Searched **{len(offending_members)}** accounts")
    return


@bot.command()
async def scammers(ctx) -> None:
    await scan_matching_user(bot, guild_id, channel_id, from_beginning=True)


@tasks.loop(seconds=30.0)
async def auto_scammers_check() -> None:
    await scan_matching_user(bot, guild_id, channel_id, from_beginning=False)


@bot.event
async def on_ready() -> None:
    auto_scammers_check.start()


bot.run(bot_key)
