import re

from pony import orm


def start_db():
    db = orm.Database()

    try:
        db.bind(provider='sqlite', filename='database.sqlite')
    except OSError as ex:
        expected_path = str(ex).split(": ")[1].replace("'", "")
        file_name = re.split("/", expected_path)[-1].replace("'", "")
        open(f"{expected_path.replace(file_name, '')}/{file_name}", "a").close()
        db.bind(provider='sqlite', filename='database.sqlite')

    orm.sql_debug(True)

    return db
