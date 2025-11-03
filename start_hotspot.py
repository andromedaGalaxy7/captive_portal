import os
import sys
import file_io
import time

# CONFIG FILES PATH
HOSTAPD_CONFIG = "hostapd.conf"
DNSMASQ_CONFIG = "dnsmasq.conf"
INTERFACE_REPLACE_STRING = "%INTERFACE%"

HOSTAPD_TARGET_PATH = "/etc/hostapd/hostapd.conf"
DNSMASQ_TARGET_PATH = "/"

# TIME TO WAIT FOR ACCESS POINT TO FIRE
AP_WAIT_DELAY = 10 # Seconds

def start_hotspot(interface_name:str) -> None:
    """
    Start a WiFi hotspot on the given interface
    :param interface_name: The interface to start the WiFi hotspot on
    :return: None
    """
    # Read the config files
    status, hostapd_configuration = file_io.read_protected_file(HOSTAPD_CONFIG)
    if not status:
        abrupt_exit(hostapd_configuration)

    status, dnsmasq_configuration = file_io.read_protected_file(DNSMASQ_CONFIG)
    if not status:
        abrupt_exit(dnsmasq_configuration)

    hostapd_configuration = hostapd_configuration.replace(INTERFACE_REPLACE_STRING, interface_name)
    dnsmasq_configuration = dnsmasq_configuration.replace(INTERFACE_REPLACE_STRING, interface_name)

    # [Over]write the current config files
    status, error_msg = file_io.write_protected_file(HOSTAPD_TARGET_PATH, hostapd_configuration)
    if not status:
        abrupt_exit(error_msg)

    status, error_msg = file_io.write_protected_file(DNSMASQ_TARGET_PATH, dnsmasq_configuration)
    if not status:
        abrupt_exit(error_msg)

    # Start hostapd service
    os.system("systemctl start hostapd.service")
    time.sleep(AP_WAIT_DELAY)

    # Assign an IP address to the interface
    os.system("ip addr add 192.168.1.1/24 dev " + interface_name)

    # Start dnsmasq service
    os.system("systemctl start dnsmasq.service")


def abrupt_exit(error_msg:str) -> None:
    """
    Abruptly exit the program on a fatal error
    :param error_msg: The message to print on the console
    :return: None
    """
    print(error_msg)
    sys.exit(1)