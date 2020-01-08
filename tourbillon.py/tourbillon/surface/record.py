from flask import jsonify
from pyrsistent import m, v, pmap, pvector
from collections import namedtuple

import tourbillon
from tourbillon import app

NAME_ADDRESS = \
    m().set('0x1d259e3852419ddf6c75c6db2aa751df7b7e9319', 'Alice') \
        .set('0x19e74a1813c73291c97f271bfae3a947eb385eac', 'Bob') \
        .set('0x94020a8513391af84cfa320e56c13f0ca724d427', 'Cloe') \
        .set('0xb450c1d01fe18e9d278255b5a240bc9deb3a0664', 'Devil') \
        .set('0x534eb986dd72630ecfc494eb2843f31496a65d9b', 'Elijah')

ViewModel = namedtuple('ViewModel', ['record_time', 'user', 'evidence', 'operation'])


@app.route('/records', methods=['GET'])
def get_records():
    if tourbillon.queue.empty():
        return jsonify({'records': 'empty'})
    else:
        return jsonify({'records': list(map(build_model, get_all(tourbillon.queue, v())))})


def get_all(queue, vector):
    return vector if queue.empty() else vector.append(queue.get_nowait())


def build_model(tsa):
    vm = ViewModel(tsa.timestamp, NAME_ADDRESS[tsa.address.lower()], tsa.digest, '存證')
    return vm._asdict()
