#!/usr/bin/env python3
import socket
import os
import sys
import datetime
from urllib.parse import urlparse
import signal

def current_time():
    return datetime.datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")

def send_error(client, code, message):
    response = f"HTTP/1.0 {code} {message}\r\n" \
               f"Content-Type: text/html\r\n" \
               f"Connection: close\r\n\r\n" \
               f"<html><body><h1>{code} {message}</h1></body></html>\r\n"
    try:
        client.sendall(response.encode())
    except Exception:
        pass
    client.close()

def handle_client(client_socket, client_address):
    try:
        request = client_socket.recv(4096)
        if not request:
            client_socket.close()
            os._exit(0)
        
        request_line = request.split(b'\r\n')[0].decode()
        parts = request_line.split()
        if len(parts) < 3:
            send_error(client_socket, 400, "Bad Request")
            os._exit(0)
        
        method, url, version = parts[0], parts[1], parts[2]
        print(f"{current_time()} Request from {client_address}: {request_line}")

        if method.upper() != "GET":
            send_error(client_socket, 501, "Not Implemented")
            os._exit(0)

        parsed_url = urlparse(url)
        if not parsed_url.scheme or not parsed_url.netloc:
            send_error(client_socket, 400, "Bad Request")
            os._exit(0)

        remote_host = parsed_url.hostname
        remote_port = parsed_url.port if parsed_url.port else 80
        remote_path = parsed_url.path if parsed_url.path else "/"
        if parsed_url.query:
            remote_path += "?" + parsed_url.query

        remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        remote_socket.connect((remote_host, remote_port))

        remote_request = f"GET {remote_path} HTTP/1.0\r\n"
        headers = request.decode().split("\r\n")[1:]
        header_lines = []
        host_present = False
        for header in headers:
            if header == "":
                break
            if header.lower().startswith("host:"):
                host_present = True
            if header.lower().startswith("connection:"):
                continue
            header_lines.append(header)
        if not host_present:
            header_lines.insert(0, f"Host: {remote_host}")
        remote_request += "\r\n".join(header_lines)
        remote_request += "\r\n\r\n"

        remote_socket.sendall(remote_request.encode())

        while True:
            data = remote_socket.recv(4096)
            if data:
                client_socket.sendall(data)
            else:
                break

        remote_socket.close()
        client_socket.close()
    except Exception as e:
        print(f"{current_time()} Error handling client {client_address}: {e}")
        try:
            client_socket.close()
        except Exception:
            pass
    finally:
        os._exit(0)

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 proxy.py <port>")
        sys.exit(1)

    listen_port = int(sys.argv[1])
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('', listen_port))
    server_socket.listen(100)
    print(f"{current_time()} Proxy server listening on port {listen_port}...")

    while True:
        try:
            client_socket, client_address = server_socket.accept()
            pid = os.fork()
            if pid == 0:
                server_socket.close()
                handle_client(client_socket, client_address)
            else:
                client_socket.close()
        except KeyboardInterrupt:
            print(f"{current_time()} Shutting down proxy server.")
            server_socket.close()
            sys.exit(0)
        except Exception as e:
            print(f"{current_time()} Error: {e}")

if __name__ == "__main__":
    signal.signal(signal.SIGCHLD, signal.SIG_IGN)
    main()