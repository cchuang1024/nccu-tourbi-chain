"""
Troubillon - 陀飛輪，整個系統的核心與驅動部位
"""

import os
import pathlib
import sqlite3
import sqlalchemy

from queue import Queue
from flask import Flask
from yaml import load, dump, CLoader, CDumper
from pyrsistent import m, v, pmap, pvector

from tourbillon import crown

CREATE_TABLE = """
  create table if not exists timestamp_authorize (
    id integer primary key autoincrement,
    address text not null,
    serial integer not null,
    digest text not null,
    digest_signature text not null,
    timestamp text not null,
    timestamp_signature text not null
  );
"""

context = None
queue = None


def init_queue():
    global queue
    queue = Queue()


def deploy_contract(tourbillon_file, breguet_file, public_key, api_url, account, target_net):
    target_net.eth.defaultAccount = account.address
    tourbillon_object = crown.deploy_contract(crown.ContractFile("Tourbillon.sol", tourbillon_file),
                                              "Tourbillon", target_net,
                                              public_key, api_url)
    breguet_object = crown.deploy_contract(crown.ContractFile("Breguet.sol", breguet_file),
                                           "Breguet", target_net,
                                           tourbillon_object.address)
    return tourbillon_object, breguet_object


def init(config_file, passphrase):
    global context, queue

    # TODO: load config
    config = init_config(config_file)

    # TODO: init queue
    queue = Queue()

    # TODO: check db
    engine = init_db(config['local_database'], CREATE_TABLE)

    # TODO: check timeserver
    timeservers = config['time_server']

    # TODO: check keystore
    private_key, account = crown.load_keystore(config['owner_keystore'], passphrase)
    public_key = crown.get_pub_from_priv(private_key).hex()

    # TODO: check ethereum connection
    target_net = crown.init_target_net_by_web(config['eth_entry_point'], account)

    # TODO: check api url
    tourbillon_api_url = config['tourbillon_api_url']

    # TODO: check contract address
    tourbillon_address = config['contract_address']['tourbillon']
    breguet_address = config['contract_address']['breguet']
    tourbillon_obj = None
    breguet_obj = None

    if tourbillon_address.endswith('sol') or breguet_address.endswith('sol'):
        tourbillon_obj, breguet_obj = deploy_contract(tourbillon_address, breguet_address,
                                                      public_key, tourbillon_api_url, account, target_net)
        config['contract_address']['tourbillon'] = tourbillon_obj.address
        config['contract_address']['breguet'] = breguet_obj.address
        update_config(config, config_file)
    else:
        tourbillon_file = crown.ContractFile('Tourbillon.sol', 'contracts/Tourbillon.sol')
        bytecode, abi = crown.compile_contract(tourbillon_file, 'Tourbillon')
        tourbillon_obj = target_net.eth.contract(address=breguet_address, abi=abi)

    context = m(engine=engine,
                queue=queue,
                timeservers=timeservers,
                private_key=private_key,
                account=account,
                target_net=target_net,
                api_url=tourbillon_api_url,
                tourbillon_object=tourbillon_obj)


def init_config(config_file):
    config_file_path = pathlib.Path(config_file)
    if os.path.exists(config_file_path.absolute()):
        with open(config_file, 'r') as file:
            return load(file, Loader=CLoader)
    else:
        orig_file = os.path.join(config_file_path.parent.absolute(), 'tourbillon.original.yaml')
        return init_config(orig_file)


def init_db(db_file, create_table):
    db_file_path = os.path.abspath(db_file)
    print('db file path {}'.format(db_file_path))

    if os.path.exists(db_file_path):
        return sqlalchemy.create_engine("sqlite:///" + db_file_path)
    else:
        with sqlite3.connect(db_file_path) as conn:
            cur = conn.cursor()
            cur.execute(create_table)
            conn.commit()

        return init_db(db_file, None)


def update_config(config, config_file):
    with open(config_file, 'w') as file:
        dump(config, file, Dumper=CDumper)


app = Flask(__name__, static_folder='../static')


def run():
    app.run()
