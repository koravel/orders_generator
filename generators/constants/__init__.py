from config import PathProvider as provider
import services.json as sjson

constants = dict()


def load(read=sjson.read):
    global constants, default_length, x_default, y_default, a_default, m_default, c_default, t0_default,\
        zones, direction, currency_pairs, currency_values, statuses, descriptions, tags
    try:
        constants = read(provider.pathes["CONSTANTS"].location)

        default_length = constants["default_length"]
        x_default = constants["x_default"]
        y_default = constants["y_default"]
        a_default = constants["a_default"]
        m_default = constants["m_default"]
        c_default = constants["c_default"]
        t0_default = constants["t0_default"]
        zones = constants["zones"]
        direction = constants["direction"]
        currency_pairs = constants["currency_pairs"]
        currency_values = constants["currency_values"]
        statuses = constants["statuses"]
        descriptions = constants["descriptions"]
        tags = constants["tags"]

    except Exception as ex:
        set_defaults(read)
        raise ex


def set_defaults(read=sjson.read):
    global constants
    constants = read(provider.pathes["DEFAULT_CONSTANTS"].location)


id_length = 20
default_length = 1024
x_default = 12
y_default = 23
a_default = 7
c_default = 3
m_default = 32768
t0_default = 1

zones = [
    "Red",
    "Green",
    "Blue"
]

direction = [
    "Buy",
    "Sell"
]
currency_pairs = [
    "EUR/USD",
    "GBP/USD",
    "USD/JPY",
    "USD/CHF",
    "USD/CAD",
    "AUD/USD",
    "NZD/USD",
    "EUR/GBP",
    "EUR/AUD",
    "GBP/JPY",
    "EUR/JPY",
    "EUR/CAD",
    "GBP/CHF",
    "EUR/NZD",
    "GBP/NZD",
    "JPY/NZD"
]

currency_values = [
    1.21585,
    1.0743,
    0.89857,
    0.91036,
    1.23045,
    1.12326,
    1.11443,
    1.07979,
    0.97051,
    0.93516,
    0.83608,
    0.88199,
    1.15967,
    1.14843,
    1.09904,
    1.20828
]

statuses = [
    "New",
    "To provider",
    "Reject",
    "Partial filled",
    "Filled"
]

descriptions = [
    "Descrription0",
    "Descrription1",
    "Descrription2",
    "Descrription3",
    "Descrription4",
    "Descrription5",
    "Descrription6",
    "Descrription7",
    "Descrription8",
    "Descrription9",
    "Descrription1",
    "Descrription11",
    "Descrription12",
    "Descrription13",
    "Descrription14",
    "Descrription15"
]

tags = [
    "Tag0",
    "Tag1",
    "Tag2",
    "Tag3",
    "Tag4",
    "Tag5",
    "Tag6",
    "Tag7",
    "Tag8",
    "Tag9",
    "Tag1",
    "Tag11",
    "Tag12",
    "Tag13",
    "Tag14",
    "Tag15"
]
