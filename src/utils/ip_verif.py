import ipaddress


def ip_belongs_to_cidr(ip_str, cidr_str):
    try:
        # Parsear la dirección IP y el CIDR
        ip = ipaddress.IPv4Address(ip_str)
        network = ipaddress.IPv4Network(cidr_str, strict=False)

        # Verificar si la IP pertenece a la red
        return ip in network
    except (ipaddress.AddressValueError, ipaddress.NetmaskValueError):
        return False
