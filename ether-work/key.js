const bip39 = require('bip39');
const wallet = require('ethereumjs-wallet');
const _ = require('lodash');
const R = require('rambda');

const names = ['alice', 'bob', 'cloe', 'devil', 'elijah'];
const priv_keys = ['8FCA9928DDE93BF36F1068FBBA94398D9C1CB574A013F0611EE1DE097A7ADDAB',
                   '0EEEA958E41D60974E232885479B863646AD820CE683BDB65D10A67D322F79D6',
                   '4DC7CE17A4DCEE4BECF65ABC1D388A572BADB47E1A5D9D732CACA892DECDEC5D',
                   '525CC59F9A0D32AECB6684552EA0B4CF2B1948586E40CFD2BE7CA2634C453327',
                   'BA135AC05344A857E5E05549CBB581B4C1CE46E24B70EB2B54D3D460242A4A98'];

const value_keys = ['name', 'private', 'mnemonic', 'address', 'public'];

const name_key_map = R.zip(names, priv_keys);

const mnemonic = function (name_key) {
    name_key.push(bip39.entropyToMnemonic(name_key[1]));
    return name_key;
};

const address = function (name_key) {
    name_key.push(wallet.fromPrivateKey(Buffer.from(name_key[1], 'hex'))
                        .getAddress()
                        .toString('hex'));
    return name_key
};

const pub_key = function (name_key) {
    name_key.push(wallet.fromPrivateKey(Buffer.from(name_key[1], 'hex'))
                        .getPublicKey()
                        .toString('hex'));
    return name_key
};

const name_key_mne = R.map(mnemonic, name_key_map);
const name_key_addr = R.map(address, name_key_mne);
const name_key_pub = R.map(pub_key, name_key_addr);

console.log(name_key_pub);