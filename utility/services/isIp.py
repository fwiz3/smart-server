import ipaddress
def is_ip(value:str):
    try:
        ipaddress.ip_address(value)
        return True
    except ValueError:
        return False

