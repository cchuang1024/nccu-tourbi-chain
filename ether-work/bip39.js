const bip39 = require('bip39');

const alice_key = '8FCA9928DDE93BF36F1068FBBA94398D9C1CB574A013F0611EE1DE097A7ADDAB';
const alice_mnemonic = bip39.entropyToMnemonic(alice_key);
const alice_address = '1d259e3852419ddf6c75c6db2aa751df7b7e9319';
const alice_serial = '123';

console.log('alice_key: ', alice_key);
console.log('alice_mnemonic: ', alice_mnemonic);
console.log('alice_address: ', alice_address);

const bob_key = '0EEEA958E41D60974E232885479B863646AD820CE683BDB65D10A67D322F79D6';
const bob_mnemonic = bip39.entropyToMnemonic(bob_key);
const bob_address = '19e74a1813c73291c97f271bfae3a947eb385eac';
const bob_serial = '108';

console.log('bob_key: ', bob_key);
console.log('bob_mnemonic: ', bob_mnemonic);
console.log('bob_address: ', bob_address);

const cloe_key = '4DC7CE17A4DCEE4BECF65ABC1D388A572BADB47E1A5D9D732CACA892DECDEC5D';
const cloe_mnemonic = bip39.entropyToMnemonic(cloe_key);
const cloe_address = '94020a8513391af84cfa320e56c13f0ca724d427';
const cloe_serial = '1024';

console.log('cloe_key: ', cloe_key);
console.log('cloe_mnemonic: ', cloe_mnemonic);
console.log('cloe_address: ', cloe_address);

const devil_key='525CC59F9A0D32AECB6684552EA0B4CF2B1948586E40CFD2BE7CA2634C453327';
const devil_mnemonic = bip39.entropyToMnemonic(devil_key);
const devil_address = 'b450c1d01fe18e9d278255b5a240bc9deb3a0664';
const devil_serial = '104';

console.log('devil_key: ', devil_key);
console.log('devil_mnemonic: ', devil_mnemonic);
console.log('devil_address: ', devil_address);

const elijah_key='BA135AC05344A857E5E05549CBB581B4C1CE46E24B70EB2B54D3D460242A4A98';
const elijah_mnemonic = bip39.entropyToMnemonic(elijah_key);
const elijah_address = '534eb986dd72630ecfc494eb2843f31496a65d9b';
const elijah_serial = '148';

console.log('elijah_key: ', elijah_key);
console.log('elijah_mnemonic: ', elijah_mnemonic);
console.log('elijah_address: ', elijah_address);
