def __open(obj_location, mode):
    return open(obj_location, mode)


def open_read(obj_location):
    return __open(obj_location, 'r')


def open_write(obj_location):
    return __open(obj_location, 'w')


def open_append(obj_location):
    return __open(obj_location, 'a')


def read_all_yield(obj_location):
    try:
        with open(obj_location, 'r') as file_stream:
            for line in file_stream:
                yield line
    except Exception as ex:
        raise ex


def read_all(obj_location):
    try:
        with open(obj_location, 'r') as file_stream:
            return file_stream.read()
    except Exception as ex:
        raise ex


def __write(obj, obj_location, mode):
    try:
        with open(obj_location, mode) as file_stream:
            file_stream.write(str(obj))
    except Exception as ex:
        raise ex


def __write_array(obj, obj_location, mode):
    try:
        counter = 0
        with open(obj_location, mode) as file_stream:
            for item in obj:
                file_stream.write("{}\n".format(str(item)))
                counter += 1
        return counter
    except Exception as ex:
        raise ex


def append(obj, obj_location):
    __write(obj, obj_location, 'a')


def write(obj, obj_location):
    __write(obj, obj_location, 'w')


def write_array(obj, obj_location):
    return __write_array(obj, obj_location, 'w')


def append_array(obj, obj_location):
    return __write_array(obj, obj_location, 'a')
