connection_result_text = "{} connection {} after {} attempts and {} sec with params {}"


def get_connection_params_text(params):
    result = ""
    param_text = "{}:{} "
    i = 0
    while i < len(params):
        result += param_text.format(params[i], params[i + 1])
        i += 2
    return result
