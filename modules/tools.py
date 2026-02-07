import ipaddress


def is_valid_subnet(subnet: str, default_prefix: str = '24') -> tuple[bool, str]:
    # If no mask is provided, append the default
    if '/' not in subnet:
        subnet = f'{subnet}/{default_prefix}'

    try:
        # ip_interface allows inputs like 192.168.1.10/24 without error
        interface = ipaddress.ip_interface(subnet)

        # .with_prefixlen returns the IP/Prefix format you want
        return True, interface.with_prefixlen

    except ValueError as e:
        print(f"ERROR: '{subnet}' is not valid! Details: {e}")
        return False, ''
