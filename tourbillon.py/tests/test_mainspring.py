import os

from tourbillon import init_db, CREATE_TABLE
from tourbillon import mainspring


def test_main_spring():
    db_file = 'tests/test.db'
    engine = init_db(db_file, CREATE_TABLE)
    table = mainspring.init_table('timestamp_authorize', engine)
    data = mainspring.TimestampAuthor("aaa", 1, "bbb", "ccc", "ddd", "eee")
    id = mainspring.save_data(data, table, engine)
    row = mainspring.get_data(table, id, engine)

    print(row)

    os.remove(os.path.abspath(db_file))
