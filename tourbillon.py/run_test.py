import time
from threading import Thread

from eth_account import Account
from eth_keys import KeyAPI
from eth_keys.backends import NativeECCBackend
from web3 import Web3

from tourbillon import crown, calibre

received = False
serial = -1


def handle_event(event, tourb, w3, private_key):
    global received, serial

    print("what time is it event: {}".format(event))

    addr = event['args']['myAddr']
    serial = event['args']['serial']
    time = calibre.get_now()
    sig = crown.sign_hash(crown.convert_to_hash(time), private_key).hex()

    result = tourb.functions.itsTime(addr, serial, time, sig).transact()
    receipt = w3.eth.waitForTransactionReceipt(result)
    print("it's time: {}".format(result, receipt))

    received = True


def listen_time_event(filter, poll_interval, tourb, w3, private_key):
    while True:
        for event in filter.get_new_entries():
            handle_event(event, tourb, w3, private_key)
        time.sleep(poll_interval)


if __name__ == '__main__':
    w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))
    key_hex = '8FCA9928DDE93BF36F1068FBBA94398D9C1CB574A013F0611EE1DE097A7ADDAB'
    alice = Account.from_key(key_hex)
    alice_priv = crown.init_private_key_from_hex(bytes.fromhex(key_hex))
    w3.eth.defaultAccount = alice.address

    tourb_file = crown.ContractFile('Tourbillon.sol', 'contracts/Tourbillon.sol')
    tourb = crown.deploy_contract(tourb_file, 'Tourbillon', w3)
    print('tourbillon address: {}'.format(tourb.address))

    filter = tourb.events.WhatTimeIsIt.createFilter(fromBlock='latest')
    worker = Thread(target=listen_time_event, args=(filter, 1, tourb, w3, alice_priv), daemon=True)
    worker.start()

    digest = '0x9eb66e90d9455a4847e5fdb070ebdba498b0dab9eef1c34b44bbb7638b37d79e'
    sign = '0xc295e2ec32d797ad83f8fad5ddf163130ec55fab178355276d76a83759cb7d392f7b55146e83cd73896cbfb6945bc0d9a2e12ad9894340729f115491fb7471bd00'

    result = tourb.functions.saveMyTreasure(alice.address, digest, sign).transact()
    receipt = w3.eth.waitForTransactionReceipt(result)
    print('save my treasure: {}'.format(receipt))

    while not received:
        time.sleep(1)

    result = tourb.functions.checkMyTreasure(alice.address, serial).call()
    print('check my treasure: {}'.format(result))
