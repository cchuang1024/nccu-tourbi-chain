import tourbillon


def context_init():
    config_file = "config/tourbillon.yaml"
    passphrase = b'!QAZ 2wsx 3edc'

    tourbillon.init(config_file, passphrase)
    print(tourbillon.context)
