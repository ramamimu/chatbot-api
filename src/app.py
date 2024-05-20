from config import PORT
from infrastructures.http.create_server import Server


if __name__ == "__main__":
  server = Server(port=int(PORT))
  server.configure_middleware()
  server.configure_endpoint()
  server.run()
