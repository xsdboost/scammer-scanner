from pathlib import Path

from pony.orm import db_session

from watcher.orm.models import DiscordUser, db

database_file = "../watcher/datastore/moderators.sqlite"
file_ptr = Path(database_file)

if file_ptr.is_file():
    file_ptr.unlink()

db.bind(provider="sqlite", filename=database_file, create_db=True)
db.generate_mapping(create_tables=True)

with db_session:
    user = DiscordUser(
        discord_id="709177976968970344", display_name="namo ebur", name="jako_mako"
    )

    user = DiscordUser(
        discord_id="643407344673464374", display_name="Jackson Herson", name="mambo_don"
    )
