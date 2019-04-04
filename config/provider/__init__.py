class PathKeys:
    ROOT = "ROOT"
    LOG = "LOG"
    SETTINGS = "SETTINGS"
    GEN_SETTINGS = "GEN_SETTINGS"
    DEFAULT_SETTINGS = "DEFAULT_SETTINGS"
    DEFAULT_GEN_SETTINGS = "DEFAULT_GEN_SETTINGS"
    GEN_OUT = "GEN_OUT"


class GenSettingsKeys:
    date = "date"
    days_amount = "days_amount"
    orders_amount = "orders_amount"
    portion_amount = "portion_amount"
    price_precision = "price_precision"
    volume_precision = "volume_precision"
    id_length = "id_length"
    default_length = "default_length"
    x = "x"
    y = "y"
    a = "a"
    c = "c"
    m = "m"
    t0 = "t0"
    zones = "zones"
    zones_percents = "zones_percents"
    direction = "direction"
    statuses = "statuses"
    descriptions = "descriptions"
    tags = "tags"
    weekends = "weekends"
    currency_pairs = "currency_pairs"
    one_state_percent = "one_state_percent"


class SettingsKeys:


    mysql = "mysql"

    database = "database"
    host = "host"
    port = "port"
    keep_connection_open = "keep_connection_open"
    order_table = "order_table"
    password = "password"
    user = "user"


    rabbit = "rabbit"

    cache_message_lifetime = "cache_message_lifetime"
    enable_cache = "enable_cache"
    exchange = "exchange"
    #host = ""
    mysql_table = "mysql_table"
    routing_key = "routing_key"


    system = "system"

    limited_therads = "limited_therads"
    out_files_max = "out_files_max"
    threads_max = "threads_max"

    logging = "logging"
    logger_files_max = "logger_files_max"
    loggers = "loggers"
