import socket


def get_instances(hostname):
    resp = __query_sql_browser(hostname)
    return __parse_response(resp)


def __query_sql_browser(hostname):
    port = 1434
    msg = b"\x02"

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(15)
    s.sendto(msg, (hostname, port))
    resp = s.recvfrom(1000000)[0][3:]

    resp_string = bytes.decode(resp, encoding="latin-1")
    return resp_string


def __parse_response(response):
    instance_strings = response.split(";;")
    instances = []
    for instance_string in instance_strings:
        if instance_string.strip() == "":
            continue
        instance = {}
        tokens = instance_string.split(";")
        while tokens:
            k = tokens.pop(0)
            v = tokens.pop(0)
            instance[k] = v
        instances.append(instance)
    return instances
