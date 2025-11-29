import subprocess
import re
from portal import app
import os

DEFAULT_INTERFACE_PATTERN = re.compile(r"\sdev\s([A-Za-z0-9]+)\s")

def find_gateway_interface() -> str:
    """
    Find the interface that has the default route
    :return: String name of the interface that has the default route to internet
    """

    output = subprocess.run(["ip", "r", "show", "default"], capture_output=True)
    def_route = output.stdout.decode()
    if def_route:
        return DEFAULT_INTERFACE_PATTERN.findall(def_route)[0]
    return ""

def start_captive_portal(ap_interface) -> bool:
    """
    starts a captive portal
    @ap_interface: The interface where the Access Point is currently active
    :return: True if operation succeeded, False otherwise
    """

    # Redirect port 80 to port 8080
    os.system(f"sudo iptables --table nat -A PREROUTING -i {ap_interface} -p tcp --dport 80 -j REDIRECT --to-port 8080")

    # Allow only DNS and DHCP traffic
    os.system(f"sudo iptables --table filter -A FORWARD -i {ap_interface} -p udp --dport 53 -j ACCEPT")
    os.system(f"sudo iptables --table filter -A FORWARD -i {ap_interface} -p tcp --dport 53 -j ACCEPT")

    os.system(f"sudo iptables --table filter -A FORWARD -i {ap_interface} -p udp --dport 67 -j ACCEPT")
    os.system(f"sudo iptables --table filter -A FORWARD -i {ap_interface} -p udp --sport 67 -j ACCEPT")

    os.system(f"sudo iptables --table filter -A FORWARD -i {ap_interface} -p udp --dport 68 -j ACCEPT")
    os.system(f"sudo iptables --table filter -A FORWARD -i {ap_interface} -p udp --sport 68 -j ACCEPT")

    os.system(f"sudo iptables --table filter -A FORWARD -i {ap_interface} -p tcp --dport 80 -j ACCEPT")
    #os.system("sudo iptables --table filter -A FORWARD -i {ap_interface} -p tcp --dport 443 -j ACCEPT")

    os.system(f"sudo iptables --table filter -A FORWARD -i {ap_interface} -j REJECT")

    # Launch the flask application
    print(f"Launching the captive portal HTTP server.")
    os.chdir("portal")
    app.interface_used = ap_interface
    app.start_server(bind_address="192.168.1.1", port=8080)