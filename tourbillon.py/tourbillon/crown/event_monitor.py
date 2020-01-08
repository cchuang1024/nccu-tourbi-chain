import goless
import threading
import time
from threading import Thread

from web3.auto import w3

import tourbillon
from tourbillon import calibre
from tourbillon import crown
from tourbillon import mainspring


def build_monitor():
    target_net = tourbillon.context['target_net']
    priv_key = tourbillon.context['private_key']
    tourb = tourbillon.context['tourbillon_object']

    event_filter = tourb.events.WhatTimeIsIt.createFilter(fromBlock=0, toBlock='latest')
    monitor = Thread(target=listen_event, args=(event_filter, 1, tourb, w3, priv_key), daemon=True)
    return monitor


def listen_event(event_filter, sleep_time, contract, target_net, owner_priv_key):
    while True:
        for event in event_filter.get_new_entries():
            handle_event(event, contract, target_net, owner_priv_key)

        time.sleep(sleep_time)


def handle_event(event, contract, target_net, private_key):
    time = calibre.get_now()
    sig = crown.sign_hash(crown.convert_to_hash(time), private_key).hex()

    print("what time is it event: {}".format(event))
    addr = event['args']['myAddr']
    serial = event['args']['serial']
    digest = event['args']['digest']
    sign = event['args']['sign']

    result = contract.functions.timeIsIt(time, sig, addr, serial).transact()
    receipt = target_net.eth.waitForTransactionReceipt(result)

    print("it's time: {}".format(result, receipt))

    saved_data = mainspring.save_timestamp_author(time, sig, addr, serial, digest, sign)

    print('saved data {}'.format(saved_data))

    tourbillon.queue.put_nowait(saved_data)
