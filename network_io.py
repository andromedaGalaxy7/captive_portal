import subprocess
import re

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

if __name__ == "__main__":
    find_gateway_interface()