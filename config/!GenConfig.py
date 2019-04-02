from generator.constant import ConstKeys


class GenConfig:
    settings = dict()

    __zones_def = [
        "Red",
        "Green",
        "Blue"
    ]
    __direction_def = [
        "Buy",
        "Sell"
    ]
    currency_def = {
        "EUR/USD": 1.21585,
        "GBP/USD": 1.0743,
        "USD/JPY": 0.89857,
        "USD/CHF": 0.91036,
        "USD/CAD": 1.23045,
        "AUD/USD": 1.12326,
        "NZD/USD": 1.11443,
        "EUR/GBP": 1.07979,
        "EUR/AUD": 0.97051,
        "GBP/JPY": 0.93516,
        "EUR/JPY": 0.83608,
        "EUR/CAD": 0.88199,
        "GBP/CHF": 1.15967,
        "EUR/NZD": 1.14843,
        "GBP/NZD": 1.09904,
        "JPY/NZD": 1.20828
    }
    __statuses_def = [
        "New",
        "To provider",
        "Reject",
        "Partial filled",
        "Filled"
    ]
    __descriptions_def = [
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
    __tags_def = [
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

    constants_default = {
        ConstKeys.id_length: 20,
        ConstKeys.default_length: 2000,
        ConstKeys.x_default: 12,
        ConstKeys.y_default: 23,
        ConstKeys.a_default: 7,
        ConstKeys.c_default: 3,
        ConstKeys.m_default: 32768,
        ConstKeys.t0_default: 1,
        ConstKeys.zones: __zones_def,
        ConstKeys.direction: __direction_def,
        ConstKeys.statuses: __statuses_def,
        ConstKeys.descriptions: __descriptions_def,
        ConstKeys.tags: __tags_def
    }




