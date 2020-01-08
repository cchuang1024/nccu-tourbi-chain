"""
Crown - 表冠，介接 ETH 進行合約操作
"""
import json

from collections import namedtuple

from eth_keyfile import extract_key_from_keyfile
from eth_hash.auto import keccak
from eth_keys import KeyAPI
from eth_keys.datatypes import Signature, PublicKey
from eth_keys.backends import base
from eth_keys.backends import NativeECCBackend
from eth_account import Account
from web3 import Web3
from solc import compile_standard, compile_source, compile_files

from tourbillon import util


def init_private_key_from_hex(key_hex):
    keys = KeyAPI(NativeECCBackend)
    return keys.PrivateKey(key_hex)


def load_keystore(keystore, passphrase):
    keys = KeyAPI(NativeECCBackend)
    priv = extract_key_from_keyfile(keystore, passphrase)
    acc = Account.from_key(priv)
    return keys.PrivateKey(priv), acc


def convert_to_hash(text):
    return keccak(text.encode('utf-8'))


def convert_bin_to_hash(binary):
    return keccak(binary)


def sign_hash(hash, priv):
    keys = KeyAPI(NativeECCBackend)
    sign = keys.ecdsa_sign(hash, priv)
    return sign.to_bytes()


def get_pub_from_priv(priv):
    keys = KeyAPI(NativeECCBackend)
    pub = keys.private_key_to_public_key(priv)
    return pub.to_bytes()


def verify_signature(hash, sig, pub):
    keys = KeyAPI(NativeECCBackend)
    sign = keys.Signature(sig)
    public = keys.PublicKey(pub, base.BaseECCBackend)
    return keys.ecdsa_verify(hash, sign, public)


######### NOT FULL TESTED YET ##########

def init_target_net_by_web(provider_url, account, **request_kwargs):
    target_net = Web3(Web3.HTTPProvider(provider_url, request_kwargs=request_kwargs))
    target_net.eth.defaultAccount = account.address
    return target_net


def compile_sol(sol_file, sol_content):
    return compile_standard({
        'language': 'Solidity',
        'sources': {
            sol_file: {
                'content': sol_content
            }
        },
        'settings': {
            'outputSelection': {
                '*': {
                    '*': ['metadata', 'evm.bytecode', 'evm.bytecode.sourceMap']
                }
            }
        }
    })


def parse_compiled_sol(compiled_sol, contract_file, contract_name):
    bytecode = compiled_sol['contracts'][contract_file.file_name][contract_name]['evm']['bytecode']['object']
    abi = json.loads(compiled_sol['contracts'][contract_file.file_name][contract_name]['metadata'])['output']['abi']
    return bytecode, abi


ContractFile = namedtuple('ContractFile', ['file_name', 'file_path'])


def compile_contract(contract_file, contract_name):
    sol_content = util.load_file_content(contract_file.file_path)
    compiled = compile_sol(contract_file.file_name, sol_content)
    bytecode, abi = parse_compiled_sol(compiled, contract_file, contract_name)
    return bytecode, abi


def build_contract_obj(bytecode, abi, target_net):
    return target_net.eth.contract(abi=abi, bytecode=bytecode)


def init_contract(contract_obj, target_net, *init_args):
    tx_hash = contract_obj.constructor().transact() if len(init_args) == 0 else contract_obj.constructor(*init_args).transact()
    tx_receipt = target_net.eth.waitForTransactionReceipt(tx_hash)

    return tx_receipt


def deploy_contract(contract_file, contract_name, target_net, *init_args):
    bytecode, abi = compile_contract(contract_file, contract_name)
    contract_obj = build_contract_obj(bytecode, abi, target_net)
    tx_receipt = init_contract(contract_obj, target_net, *init_args)

    return target_net.eth.contract(address=tx_receipt.contractAddress, abi=abi)
