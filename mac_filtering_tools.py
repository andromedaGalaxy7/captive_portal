import os
from typing import Optional
import re
import network_io

MAC_ADDRESS_REGEX = r"(([0-9A-Fa-f]){2}:){5}(([0-9A-Fa-f]){2})"

def get_mac_from_ip(ip_addr: str) -> Optional[str]:
    """
    Uses the arp tool using a pipe to get MAC address from ip address
    :param ip_addr: The IPv4 address as a string
    :return: the MAC address, as a string, None if not found
    """
    stream = os.popen(f"arp -n {ip_addr}")
    output = stream.read()
    stream.close()

    ### Processing
    if "no entry" in output:
        return None
    matches = re.search(MAC_ADDRESS_REGEX, output)
    return matches[0]

def allow_mac_address(mac_addr: str, ap_interface: str) -> bool:
    """
    Add a mac address to the allow list using iptables.
    :param mac_addr: Incoming mac address as a string
    :param ap_interface: The Access Point Interface
    :return: True if operation succeeded, False otherwise.
    """
    exit_interface = network_io.find_gateway_interface()
    if exit_interface:
        # Add rule in the filter table forward chain
        os.system(f"iptables --table filter -I FORWARD -m mac --mac-source {mac_addr} -j ACCEPT")

        # Add rule in the nat post-routing chain
        os.system(f"iptables --table nat -I POSTROUTING -m mac --mac-source {mac_addr} -i {ap_interface} -o {exit_interface} -j masquerade")

        return True
    return False

if __name__ == "__main__":
    print(get_mac_from_ip("192.168.1.6"))
