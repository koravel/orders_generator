__connection_result_text = "{} connection {} after {} attempts and {} sec with params {}"


def __get_connection_params_text(params):
    result = ""
    param_text = "{}:{}"
    i = 0
    while i < len(params) - 1:
        result += param_text.format(params[i], params[i + 1])
    return result
