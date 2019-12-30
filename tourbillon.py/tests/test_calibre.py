import arrow
from tourbillon import calibre
from datetime import datetime


def test_get_now():
    now = calibre.get_now()
    assert now is not None

    arr = arrow.get(now)
    assert arr.float_timestamp < datetime.now().timestamp()
