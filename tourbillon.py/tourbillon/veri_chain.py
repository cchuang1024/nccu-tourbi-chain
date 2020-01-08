import sys
import time

from yaml import load, CLoader
from tourbillon import crown


def verify(args):
    keystore = args[1]
    file = args[2]
    passphrase = args[3]

    priv_key, account = crown.load_keystore(keystore, passphrase)

    digest = None
    with open(file, 'rb') as file:
        raw = file.read()
        digest = crown.convert_bin_to_hash(raw)

    digest_sign = crown.sign_hash(digest, priv_key)

    print('my treasure {} : {}'.format(digest.hex(), digest_sign.hex()))

    w3, breguet = build_contract(account)
    result = breguet.functions.saveMyTreasure(account.address, digest.hex(), digest_sign.hex()).transact()
    receipt = w3.eth.waitForTransactionReceipt(result)

    print('your treasure saved: {}'.format(receipt))

    serial = breguet.functions.checkMySerial(account.address).call()
    print('my serial: {}'.format(serial))

    treasure = breguet.functions.checkMyTreasure(account.address, serial).call()
    print('my treasure: {}'.format(treasure))

    count = 0
    while count < 10:
        timestamp = breguet.functions.checkMyTime(account.address, serial).call()
        if timestamp[0] != '':
            print('my timestamp: {}'.format(timestamp))
            break
        else:
            time.sleep(1)


def build_contract(account):
    w3 = crown.init_target_net_by_web('http://127.0.0.1:8545/', account)
    config = load_config()

    tourbillon_file = crown.ContractFile('Tourbillon.sol', 'contracts/Tourbillon.sol')
    bytecode, abi = crown.compile_contract(tourbillon_file, 'Tourbillon')
    tourbillon = w3.eth.contract(address=config['contract_address']['breguet'], abi=abi)

    return w3, tourbillon


def load_config():
    with open('config/tourbillon.yaml', 'r') as file:
        return load(file, Loader=CLoader)


if __name__ == '__main__':
    verify(sys.argv)
