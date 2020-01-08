"""
Mainspring - 發條，資料儲存模組
"""

from sqlalchemy import Table, MetaData, select, create_engine, column, text
from collections import namedtuple
from tourbillon import context

TimestampAuthor = namedtuple('TimestampAuthor', ['address', 'serial',
                                                 'digest', 'digest_signature',
                                                 'timestamp', 'timestamp_signature'])


def init_table(table_name, engine):
    meta = MetaData()
    meta.reflect(engine, only=[table_name])
    return Table(table_name, meta, autoload=True, autoload_with=engine)


INSERT = """
insert into timestamp_authorize (
    address, serial,
    digest, digest_signature,
    timestamp, timestamp_signature)
values (
    :address, :serial,
    :digest, :digest_signature,
    :timestamp, :timestamp_signature);
"""


def save_data(data, table, engine):
    with engine.connect() as conn:
        insert = text(INSERT)
        return conn.execute(insert, **data._asdict()).lastrowid


def get_data(table, id, engine):
    with engine.connect() as conn:
        sql = select([table]).where(table.c.id == id)
        return conn.execute(sql).fetchone()


def save_timestamp_author(ts, ts_sign, addr, serial, digest, digest_sign):
    engine = context['engine']
    table = init_table('timestamp_authorize', engine)
    data = TimestampAuthor(addr, serial, digest, digest_sign, ts, ts_sign)
    id = save_data(data, table, engine)
    row = get_data(table, id, engine)
    return row
