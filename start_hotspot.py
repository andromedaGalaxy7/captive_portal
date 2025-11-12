import os
import sys
import file_io
import time
import network_io

# CONFIG FILES PATH
HOSTAPD_CONFIG = "hostapd.conf"
DNSMASQ_CONFIG = "dnsmasq.conf"
INTERFACE_REPLACE_STRING = "%INTERFACE%"

HOSTAPD_TARGET_PATH = "/etc/hostapd/hostapd.conf"
DNSMASQ_TARGET_PATH = "/etc/dnsmasq.conf"

# TIME TO WAIT FOR ACCESS POINT TO FIRE
AP_WAIT_DELAY = 10 # Seconds

# IP ADDRESS CONFIG
SELF_IP_ADDRESS = "192.168.1.1/24"

# INTERFACE WITH WAN ACCESS
WAN_INTERFACE = ""

def start_hotspot(interface_name:str, internet_enabled=True) -> None:
    """
    Start a WiFi hotspot on the given interface
    :param interface_name: The interface to start the WiFi hotspot on
    :param internet_enabled: True -> Enables IP Masquerading to the interface with default route
                             False -> Does nothing, and the new hotspot is not connected to the internet
    :return: None
    """
    print(f"Interface name received: {interface_name}")

    # Read the config files
    print(f"Reading file {HOSTAPD_CONFIG}")
    status, hostapd_configuration = file_io.read_protected_file(HOSTAPD_CONFIG)
    if not status:
        abrupt_exit(hostapd_configuration)

    print(f"Reading file {DNSMASQ_CONFIG}")
    status, dnsmasq_configuration = file_io.read_protected_file(DNSMASQ_CONFIG)
    if not status:
        abrupt_exit(dnsmasq_configuration)

    hostapd_configuration = hostapd_configuration.replace(INTERFACE_REPLACE_STRING, interface_name)
    dnsmasq_configuration = dnsmasq_configuration.replace(INTERFACE_REPLACE_STRING, interface_name)

    # [Over]write the current config files
    print(f"Writing file {HOSTAPD_TARGET_PATH}")
    status, error_msg = file_io.write_protected_file(HOSTAPD_TARGET_PATH, hostapd_configuration)
    if not status:
        abrupt_exit(error_msg)

    print(f"Writing file {DNSMASQ_TARGET_PATH}")
    status, error_msg = file_io.write_protected_file(DNSMASQ_TARGET_PATH, dnsmasq_configuration)
    if not status:
        abrupt_exit(error_msg)

    # Start hostapd service
    print("Starting hostapd service.")
    os.system("systemctl start hostapd.service")

    print("Waiting for Access Point to start", end="")
    seconds_waited = 0
    while seconds_waited < AP_WAIT_DELAY:
        print(".", end="")
        time.sleep(0.5)
        seconds_waited += 0.5
    print("")

    # Assign an IP address to the interface
    print(f"Assigning IP address {SELF_IP_ADDRESS} to {interface_name}.")
    os.system(f"ip addr add {SELF_IP_ADDRESS} dev {interface_name}")

    # Start dnsmasq service
    print("Starting dnsmasq service")
    os.system("systemctl start dnsmasq.service")

    if internet_enabled:
        # Add iptable masquerading rule
        print("Adding iptable rule to allow WAN/INTERNET access")
        if WAN_INTERFACE:
            alternate_interface = WAN_INTERFACE
        else:
            alternate_interface = network_io.find_gateway_interface()

        if alternate_interface:
            print(f"Assuming interface {alternate_interface} has internet access.")
            os.system(f"iptables --table nat -A POSTROUTING -o {alternate_interface} -j MASQUERADE")
        else:
            print("No interface has a default route. Please fix your internet connection to allow internet access to the hotspot.")
    print("\n\nWiFi Hotspot has been started successfully.\n\tEnjoy !!! ")

def abrupt_exit(error_msg:str) -> None:
    """
    Abruptly exit the program on a fatal error
    :param error_msg: The message to print on the console
    :return: None
    """
    print(error_msg)
    sys.exit(1)

"""
-----------------------
---- ENTRY POINT ------
-----------------------
"""

if __name__ == "__main__":
    if len(sys.argv) == 1:
        input_interface_name = input("Please type the name of the interface to run the hotspot >>")
    else:
        input_interface_name = sys.argv[1]
        if len(sys.argv) == 3:
            globals()["WAN_INTERFACE"] = sys.argv[2]

    start_hotspot(input_interface_name)