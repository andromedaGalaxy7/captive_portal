from flask import Flask, send_from_directory, Response, request
import os
import mac_filtering_tools

app = Flask(__name__)
DEFAULT_PORT = 8080
DEFAULT_BIND_ADDRESS = "127.0.0.1"

# Variable for the interface being used
interface_used = None

# password
verification_password = "fireball"

# allowed IPs list
allowed_ips = []

# Homepage route
@app.route("/", methods=["GET", "POST"])
def home() -> Response:
    """
    The homepage route, the first page the user sees
    :return: The homepage as a response object
    """
    return send_from_directory("static", "index.html")

@app.route("/verify", methods=["GET", "POST"])
def verify() -> Response:
    if request.method == "GET":
        password = request.args.get("pass")
        if password == verification_password:
                if request.remote_addr not in allowed_ips:
                    success = mac_filtering_tools.allow_ip_address(request.remote_addr)
                else:
                    success = True
                    print(f"IP Address {request.remote_addr} already in allowed IPs list.")
                if success:
                    allowed_ips.append(request.remote_addr)
                    return send_from_directory("static", "thank_you.html")
                else:
                    print("cannot find any interface with internet access.")
        else:
            print(f"Wrong password -> {password} from IP address {request.remote_addr}")

    return home()

# Fetch all the files from the static path if it even exists.
@app.route("/<path:path>", methods=["GET", "POST"])
def serve_static_file(path:str) -> Response:
    """
    Serves a static file if it exists in the static directory, else none
    :param path:The path to the static resource
    :return:Response object, containing the file to be sent
    """
    full_path = os.path.join(os.getcwd(), "static")
    full_path = os.path.join(full_path, path)

    if os.path.exists(full_path):
        return send_from_directory("static", path)
    else:
        return home()

def start_server(port=DEFAULT_PORT, bind_address=DEFAULT_BIND_ADDRESS) -> None:
    """
    Starts the HTTP server for the portal, at the provided port
    :param port: The port to run the server on, if not provided uses the DEFAULT_PORT
    :param bind_address: The bind address to bind the server to, uses localhost by default
    :return:
    """
    app.run(port=port, host=bind_address)

if __name__ == "__main__":
    start_server(bind_address="192.168.1.1", port=8080)