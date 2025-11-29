from flask import Flask, send_from_directory, Response
import os

app = Flask(__name__)
DEFAULT_PORT = 8080
DEFAULT_BIND_ADDRESS = "127.0.0.1"

# Homepage route
@app.route("/", methods=["GET", "POST"])
def home() -> Response:
    """
    The homepage route, the first page the user sees
    :return: The homepage as a response object
    """
    return send_from_directory("static", "index.html")

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