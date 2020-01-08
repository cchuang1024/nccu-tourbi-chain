from queue import Queue
from pyrsistent import m

import tourbillon
from tourbillon.surface import record
from tourbillon.mainspring import TimestampAuthor


def test_records():
    tourbillon.init_queue()

    tourbillon.queue.put_nowait(TimestampAuthor("1d259e3852419ddf6c75c6db2aa751df7b7e9319", 1, "bbb", "ccc", "ddd", "eee"))
    records = record.get_records()
    print(records)
