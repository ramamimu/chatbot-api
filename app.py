from config import PORT
from src.server import Server
import sys

arguments = sys.argv
arg_test = arguments[1] if len(arguments) > 1 else ""
is_test = True if arg_test == "test" else False

server = Server(port=int(PORT), is_test_mode=is_test)
server.configure_middleware()
server.configure_endpoint()
server.run()
