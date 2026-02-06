# from getmac import get_mac_address
from scapy.all import ARP
from scapy.all import Ether
from scapy.all import srp

# # Get MAC address of a local interface
# mac_local = get_mac_address()
# print(f"Local MAC: {mac_local}")

# # Get MAC address of a remote host by IP
# mac_remote = get_mac_address(ip="192.168.1.100")
# print(f"Remote MAC: {mac_remote}")

# # Get MAC address of a remote host by hostname
# mac_remote_host = get_mac_address(hostname="google.com")
# print(f"Remote Host MAC: {mac_remote_host}")


"""
@return list with ip and mac
@param subnet "192.168.0.0/24"
"""


def scan_network_ip_addresses(subnet) -> list:
    arp_request = Ether(dst='ff:ff:ff:ff:ff:ff') / ARP(pdst=subnet)
    answered, unanswered = srp(arp_request, timeout=1, verbose=False)

    results = []
    for sent, received in answered:
        results.append({'ip': received.psrc, 'mac': received.hwsrc})
    return results


if __name__ == '__main__':
    subnet = '192.168.0.0/24'  # Replace with your network range
    print('scanning network')
    devices = scan_network_ip_addresses(subnet)
    print(F'found {len(devices)} devices')
    for device in devices:
        print(f"IP: {device['ip']}, MAC: {device['mac']}")
