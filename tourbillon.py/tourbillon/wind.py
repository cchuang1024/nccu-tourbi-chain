"""
wind - 上鍊，啟動陀飛輪
"""

import tourbillon
from tourbillon.surface import index, timer, record
from tourbillon.crown import event_monitor

if __name__ == '__main__':
    config_file = "config/tourbillon.yaml"
    passphrase = b'!QAZ 2wsx 3edc'

    tourbillon.init(config_file, passphrase)
    event_monitor.build_monitor().start()
    tourbillon.run()
