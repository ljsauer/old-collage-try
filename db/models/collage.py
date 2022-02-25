from datetime import datetime

from pony.orm import Required, select, db_session, StrArray, PrimaryKey, Optional

from db.database import start_db

with open('db/database.sqlite', 'w') as db_file:
    # Create new database file if none exists
    pass

db = start_db()


class Collage(db.Entity):
    id = PrimaryKey(int, auto=True)
    words = Required(StrArray)
    name = Optional(str)
    path = Optional(str)
    created_datetime = Required(
        datetime, default=datetime.now(), sql_type="timestamp with time zone"
    )
    last_updated_datetime = Required(
        datetime, default=datetime.now(), sql_type="timestamp with time zone"
    )

    @db_session
    def find(self, collage_id: str):
        return select(c for c in Collage if c.id == collage_id)


db.generate_mapping(create_tables=True)
