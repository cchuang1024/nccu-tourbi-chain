"""
Calibre - 機芯，作為 NTP 時間同步的關鍵元件
"""
import ntplib
import arrow

def get_now():
    c = ntplib.NTPClient()
    response = c.request('watch.stdtime.gov.tw', version=3)
    return arrow.get(response.tx_time).__str__()