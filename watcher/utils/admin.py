from datetime import datetime
from typing import List, Tuple, Sequence, Type

import pytz
from discord import Member

from watcher.orm.models import DiscordUser


class MemberCheck:
    @classmethod
    def how_long_was_member_in_guild(cls, member: Member) -> int:

        return (datetime.now(pytz.UTC) - member.joined_at).days

    @classmethod
    def member_of_guild_longer_than_30days(cls, member: Member) -> bool:

        return member.joined_at is None or cls.how_long_was_member_in_guild(member) > 30


class AdminCheck:
    def __init__(
        self,
        guild_members: Sequence[Member],
        admin_users: List[DiscordUser],
    ) -> None:

        self.guild_members: Sequence[Member] = guild_members
        self.admin_users: List[DiscordUser] = admin_users

    def __diff_accounts_match(
        cls, left_user: Tuple[str, str], right_user: Tuple[str, str]
    ) -> bool:

        return left_user[0].startswith(right_user[0]) and left_user[1] != right_user[1]

    def __iter_admin_check(self, member: Member) -> Tuple[Member, DiscordUser] | None:

        for admin_user in self.admin_users:
            left_user = member.display_name, str(member.id)
            right_user = admin_user.display_name, admin_user.discord_id

            if self.__diff_accounts_match(left_user, right_user):
                return member, admin_user

    def members_in_admin_list(
        self,
        member_rules: Type[MemberCheck],
        scheduled_job: bool,
    ) -> List[Tuple[Member, DiscordUser]]:

        matching_names: List[Tuple[Member, DiscordUser]] = list()

        for member in self.guild_members:
            if member.bot:
                continue
            elif not scheduled_job:
                pass
            elif member_rules.member_of_guild_longer_than_30days(member):
                continue

            entry_found = self.__iter_admin_check(member)
            if entry_found:
                matching_names.append(entry_found)

        return matching_names
