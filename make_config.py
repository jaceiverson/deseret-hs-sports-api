import configparser


def write(data, filepath="config.ini"):
    """
    pass in a dictionary, and filepath, and it will store the info
    in a config file to use in another program
    """
    config = configparser.ConfigParser()

    sections = list(data.keys())

    for x in sections:
        config[x] = data[x]

    # write to config file
    with open(filepath, "w") as configfile:
        config.write(configfile)


def read(filepath="config.ini", out=False):

    config = configparser.ConfigParser()

    config.read(filepath)

    if out:
        for group in config.sections():
            for key in config[group]:
                print(config[group][key])

    return config


if __name__ == "__main__":
    pass
