from typing import List, Any, Tuple
from discord import Guild
from pony.orm import db_session, select
from scammer_scan.utils.admin import AdminCheck, MemberCheck
from scammer_scan.orm.models import DiscordUser


async def scan_matching_user(
        guild: Guild, scheduled_job: bool
) -> List[Tuple[Any, DiscordUser]]:
    with db_session:
        admin_users: List[DiscordUser] = select(user for user in DiscordUser).fetch()

    admin_check = AdminCheck(guild.members, admin_users)

    offending_members = admin_check.members_in_admin_list(
        MemberCheck, scheduled_job=scheduled_job
    )

    return offending_members
