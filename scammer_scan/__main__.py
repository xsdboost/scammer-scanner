from scammer_scan.secrets.credentials import bot_key, channel_id, guild_id

import discord
from discord.ext import commands, tasks

from scammer_scan.domain import usecases
from scammer_scan.orm.models import db
from scammer_scan.utils.modals import EmbedMessages

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.reactions = True

client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix="/", client=client, intents=intents)

db.bind(provider="sqlite", filename="./datastore/moderators.sqlite", create_db=True)
db.generate_mapping(create_tables=True)


@bot.command()
async def scammers(ctx) -> None:
    scheduled_job = False
    guild = bot.get_guild(guild_id)
    channel = guild.get_channel(channel_id)

    offending_members = await usecases.scan_matching_user(guild, scheduled_job=scheduled_job)

    for offender in offending_members:
        found_embed = await channel.send(embed=EmbedMessages(offender))
        for emoji in ['🚫','🆗']:
            await found_embed.add_reaction(emoji)

    if len(offending_members) == 0 and not scheduled_job:
        await channel.send("Application completed, no scammers found!")


@tasks.loop(seconds=30.0)
async def auto_scammers_check() -> None:
    scheduled_job = True
    guild = bot.get_guild(guild_id)
    channel = guild.get_channel(channel_id)

    offending_members = await usecases.scan_matching_user(guild, scheduled_job=scheduled_job)

    for offender in offending_members:
        found_embed = await channel.send(embed=EmbedMessages(offender))
        for emoji in ['🚫', '🆗']:
            await found_embed.add_reaction(emoji)

    if len(offending_members) == 0 and not scheduled_job:
        await channel.send("Application completed, no scammers found!")


@bot.event
async def on_ready() -> None:

    auto_scammers_check.start()


@bot.event
async def on_raw_reaction_add(payload):

    if payload.member.bot:
        return

    channel = bot.get_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)

    embed = message.embeds[0]
    embed_description = embed.description
    scam_user_id = embed_description.split('**')[1].replace('<@', '').replace('>', '')

    if payload.emoji.name == '🚫':
        await channel.guild.ban(user=bot.get_user(scam_user_id))

    if payload.emoji.name == '🆗':
        await channel.guild.unban(user=bot.get_user(scam_user_id))

    user = bot.get_user(payload.user_id)
    await message.remove_reaction(payload.emoji, user)




bot.run(bot_key)
