"""
wind - 上鍊，啟動陀飛輪
"""

import tourbillon
from tourbillon.surface import index, timer, record
from tourbillon.crown import event_monitor
from threading import Thread


def start_monitor():
    w3 = tourbillon.context['target_net']
    priv_key = tourbillon.context['private_key']
    tourb = tourbillon.context['tourbillon_object']

    event_filter = tourb.events.WhatTimeIsIt.createFilter(fromBlock='latest')
    # monitor = event_monitor.EventMonitor(filter, 1, tourb, w3, priv_key)
    monitor = Thread(target=event_monitor.listen_event, args=(event_filter, 1, tourb, w3, priv_key), daemon=True)
    monitor.start()

    print("start monitoring............")


if __name__ == '__main__':
    config_file = "config/tourbillon.yaml"
    passphrase = b'!QAZ 2wsx 3edc'

    tourbillon.init(config_file, passphrase)

    start_monitor()

    tourbillon.run()
