import time
from threading import Thread

from eth_account import Account
from web3 import Web3

from tourbillon import crown, calibre


received = False


def handle_event(event, simple, w3):
    global received

    print('event {}'.format(event))
    print('requestor {}'.format(event['args']['requestor']))

    now = calibre.get_now()
    result = simple.functions.timeIsIt(now).transact()
    receipt = w3.eth.waitForTransactionReceipt(result)
    print("it's time receipt {}".format(receipt))

    received = True


def log_loop(filter, poll_interval, simple, w3):
    while True:
        for event in filter.get_new_entries():
            handle_event(event, simple, w3)
        time.sleep(poll_interval)


def main():
    w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))
    alice = Account.from_key('8FCA9928DDE93BF36F1068FBBA94398D9C1CB574A013F0611EE1DE097A7ADDAB')
    w3.eth.defaultAccount = alice.address

    simple_file = crown.ContractFile('SimpleTime.sol', 'contracts/SimpleTime.sol')
    simple = crown.deploy_contract(simple_file, 'SimpleTime', w3)

    filter = simple.events.WhatTimeIsIt.createFilter(fromBlock='latest')
    worker = Thread(target=log_loop, args=(filter, 1, simple, w3), daemon=True)
    worker.start()

    result = simple.functions.whatTimeIsIt(alice.address).transact()
    receipt = w3.eth.waitForTransactionReceipt(result)
    print('call what time is it receipt {}'.format(receipt))

    while not received:
        time.sleep(1)

    result = simple.functions.getTime().call()
    print('get time {}'.format(result))


if __name__ == '__main__':
    main()
