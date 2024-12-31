import re


def err_serializer(errors):
    msg = ""
    for key, val in errors.items():
        if isinstance(val, list):
            val = val[0]
        msg += "{}\n".format(val)
        # msg += "{}: {}\n".format(key, val)
        break
    return msg


def err_msg(msg, status):
    return {
        "code": status,
        "message": msg
    }


def is_mobile_number(value):
    # type of number (iran)
    mobile_number_pattern = re.compile(r'^09\d{9}$')
    if mobile_number_pattern.match(value):
        return True
    return False