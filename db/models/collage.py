import re
from datetime import datetime

from pony import orm
from pony.orm import Required, select, db_session, StrArray, PrimaryKey, Optional

db = orm.Database()

try:
    db.bind(provider='sqlite', filename='database.sqlite')
except OSError as ex:
    expected_path = str(ex).split(": ")[1].replace("'", "")
    file_name = re.split("/", expected_path)[-1].replace("'", "")
    open(f"{expected_path.replace(file_name, '')}/{file_name}", "a").close()
    db.bind(provider='sqlite', filename='database.sqlite')

orm.sql_debug(True)


class Collage(db.Entity):
    id = PrimaryKey(int, auto=True)
    words = Required(StrArray)
    name = Optional(str)
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
