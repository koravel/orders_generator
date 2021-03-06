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
    reporter = "reporter"
    mysql = "mysql"

    database = "database"
    host = "host"
    port = "port"
    keep_connection_open = "keep_connection_open"
    instant_connection_attempts = "instant_connection_attempts"
    connection_attempts = "connection_attempts"
    connection_attempts_delay = "connection_attempts_delay"
    order_table = "order_table"
    batch_delay = "batch_delay"
    password = "password"
    user = "user"


    rabbit = "rabbit"

    message_ttl = "message_ttl"
    enable_cache = "enable_cache"
    vhost = "vhost"
    mysql_table = "mysql_table"
    order_record = "order_record"
    queues = "queues"
    exchange_name = "exchange_name"
    exchange_mode = "exchange_mode"
    order_record_config = "order_record_config"
    retry_amount = "retry_amount"
    retry_timeout = "retry_timeout"




    system = "system"

    limited_therads = "limited_therads"
    out_files_max = "out_files_max"
    threads_max = "threads_max"
    queue_max = "queue_max"
    manual_stop = "manual_stop"

    logging = "logging"
    logger_files_max = "logger_files_max"
    loggers = "loggers"
