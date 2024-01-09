import socket
import http
import logging

# Configure logging
logging.basicConfig(filename='server.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

DEFAULT_URL = '/'
QUEUE_SIZE = 10
IP = '127.0.0.1'
PORT = 80
SOCKET_TIMEOUT = 3
WEBROOT = 'webroot'

def handle_client(client_socket):
    logging.info("New client connection")
    try:
        req = client_socket.recv(1024).decode()
        logging.debug("Received request: %s", req)
        if len(req) > 0:
            req = http.http_get(req)
            res = req.create_respons()
            logging.info("Sending response: %s %s", res.line, res.header)
            client_socket.send(res.ToBinary())
    except Exception as e:
        logging.error("Error handling request: %s", e)
    finally:
        client_socket.close()
        logging.info("Client connection closed")

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server_socket.bind((IP, PORT))
        server_socket.listen(QUEUE_SIZE)
        logging.info("Listening for connections on port %d", PORT)
        print("Listening for connections on port %d", PORT)
        while True:
            client_socket, client_address = server_socket.accept()
            try:
                print("New connection received from %s", client_address)
                client_socket.settimeout(SOCKET_TIMEOUT)
                handle_client(client_socket)
            except socket.error as err:
                logging.error("Received socket exception: %s", err)
            except Exception as err:
                logging.error("Error handling connection: %s", err)
            finally:
                client_socket.close()
    except socket.error as err:
        logging.error("Received socket exception: %s", err)
    finally:
        server_socket.close()

def test():
    req = http.http_get('GET /index.html HTTP/1.1')
    print("path:" +req.path)
    print("line:" +req.line)
    print("header:" + req.header)
    print("body:" +req.body)
    res = req.create_respons()
    print(res.body)
    print(res.ToBinary().decode("utf-8"))
if __name__ == "__main__":
    # Call the main handler function
    main()
    #test()