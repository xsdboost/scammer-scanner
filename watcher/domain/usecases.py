from datetime import datetime
from typing import List, Tuple
import pytz
from discord import Member, Guild

from watcher.orm.models import DiscordUser


def how_long_was_member_in_guild(member: Member) -> int:
    return (datetime.now(pytz.UTC) - member.joined_at).days


def was_member_longer_than_30_days(member: Member) -> bool:
    return member.joined_at is None or how_long_was_member_in_guild(member) > 30


def diff_accounts_match(
    left_name: str,
    left_id: str,
    right_name: str,
    right_id: str,
) -> bool:
    return left_name.startswith(right_name) and left_id != right_id


def iter_admin_check(
    member: Member, admin_users: List[DiscordUser]
) -> Tuple[Member, DiscordUser] | None:
    for admin_user in admin_users:
        if diff_accounts_match(
            member.display_name,
            str(member.id),
            admin_user.display_name,
            admin_user.discord_id,
        ):
            return member, admin_user


def members_in_admin_list(
    guild_members: List[Member],
    admin_users: List[DiscordUser],
    from_beginning: bool = False,
) -> List[Tuple[Member, DiscordUser]]:
    matching_names: List[Tuple[Member, DiscordUser]] = list()

    for member in guild_members:
        if from_beginning and not member.bot:
            pass
        elif was_member_longer_than_30_days(member) or member.bot:
            continue

        entry = iter_admin_check(member, admin_users)
        if entry:
            matching_names.append(entry)

    return matching_names
