from flask import Flask, send_from_directory, Response
import os

app = Flask(__name__)
DEFAULT_PORT = 8080

# Homepage route
@app.route("/")
def home() -> Response:
    """
    The homepage route, the first page the user sees
    :return: The homepage as a response object
    """
    return send_from_directory("static", "index.html")

# Fetch all the files from the static path if it even exists.
@app.route("/<path:path>")
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

def start_server(port=DEFAULT_PORT) -> None:
    """
    Starts the HTTP server for the portal, at the provided port
    :param port: The port to run the server on, if not provided uses the DEFAULT_PORT
    :return:
    """
    app.run(port=port)