from secrets.credentials import bot_key, channel_id, guild_id

import discord
from discord.ext import commands, tasks

from watcher.domain import usecases
from watcher.orm.models import db

intents = discord.Intents.default()
intents.message_content = True
intents.members = True


client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix="/", client=client, intents=intents)

db.bind(provider="sqlite", filename="datastore/moderators.sqlite", create_db=True)
db.generate_mapping(create_tables=True)


@bot.command()
async def scammers(ctx) -> None:

    await usecases.scan_matching_user(bot, guild_id, channel_id, scheduled_job=False)


@tasks.loop(seconds=30.0)
async def auto_scammers_check() -> None:

    await usecases.scan_matching_user(bot, guild_id, channel_id, scheduled_job=True)


@bot.event
async def on_ready() -> None:

    auto_scammers_check.start()


bot.run(bot_key)
