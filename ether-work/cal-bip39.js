const bip39 = require('bip39');
const arg = process.argv[2];

console.log(bip39.entropyToMnemonic(arg));
// console.log(arg);
