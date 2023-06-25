from typing import List
from pony.orm import db_session, select

from scammer_scan.utils.admin import AdminCheck, MemberCheck
from scammer_scan.utils.modals import EmbedMessages
from scammer_scan.orm.models import DiscordUser


@db_session
async def scan_matching_user(
        bot, guild_id: int, channel_id: int, scheduled_job: bool
) -> None:

    guild = bot.get_guild(guild_id)
    channel = guild.get_channel(channel_id)

    admin_users: List[DiscordUser] = select(user for user in DiscordUser).fetch()

    admin_check = AdminCheck(guild.members, admin_users)
    offending_members = admin_check.members_in_admin_list(MemberCheck, scheduled_job=scheduled_job)

    for offender in offending_members:
        await channel.send(embed=EmbedMessages(offender))

    if len(offending_members) == 0 and not scheduled_job:
        await channel.send("Application completed, no scammers found!")
