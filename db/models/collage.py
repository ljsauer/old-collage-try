from datetime import datetime

from pony import orm
from pony.orm import Required, select, db_session, FloatArray

db = orm.Database()

db.bind(provider='sqlite', filename='database.sqlite')
orm.sql_debug(True)


class Collage(db.Entity):
    image = Required(bytes)
    text = Required(str)
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
