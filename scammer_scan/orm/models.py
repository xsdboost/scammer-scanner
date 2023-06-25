from pony.orm import *

db = Database()


class DiscordUser(db.Entity):

    discord_id = PrimaryKey(str)
    display_name = Required(str)
    name = Required(str)
