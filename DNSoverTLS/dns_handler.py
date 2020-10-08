import socketserver
import threading
import logging
import ssl
import socket
import binascii

_log = logging.getLogger(__name__)


class DNSHandler(socketserver.BaseRequestHandler):

    def handle(self):
        data, connection = self.request
        response = self.resolve(data)

        _log.info('Received UDP request.')
        connection.sendto(bytes(response), self.client_address)
        _log.info('Response UDP sent.')

    def resolve(self, query, dns_server='1.1.1.1'):
        server = (dns_server, 853)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(100)

        ctx = ssl.create_default_context()
        ctx = ssl.SSLContext(ssl.PROTOCOL_TLS)
        ctx.options |= ssl.OP_NO_TLSv1
        ctx.options |= ssl.OP_NO_TLSv1_1
        ctx.verify_mode = ssl.CERT_REQUIRED
        ctx.check_hostname = ctx.load_verify_locations(
            '/etc/ssl/certs/ca-certificates.crt')

        wrapped_socket = ctx.wrap_socket(sock, server_hostname=dns_server)
        wrapped_socket.connect(server)

        tcp_msg = "\x00".encode() + chr(len(bytes(query))).encode() + query

        wrapped_socket.send(tcp_msg)
        data = wrapped_socket.recv(1024)

        if data:
            udp_result = data[2:]
            return udp_result

        _log.error('Query not supported.')


class DNSTCPHandler(socketserver.BaseRequestHandler):

    def handle(self):
        data = self.request.recv(1024).strip()
        response = self.resolve(data)

        _log.info('Received TCP request.')
        self.request.sendall(response)
        _log.info('Response TCP sent.')

    def resolve(self, query, dns_server='1.1.1.1'):
        server = (dns_server, 853)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(100)

        ctx = ssl.create_default_context()
        ctx = ssl.SSLContext(ssl.PROTOCOL_TLS)
        ctx.options |= ssl.OP_NO_TLSv1
        ctx.options |= ssl.OP_NO_TLSv1_1
        ctx.verify_mode = ssl.CERT_REQUIRED
        ctx.check_hostname = ctx.load_verify_locations(
            '/etc/ssl/certs/ca-certificates.crt')

        wrapped_socket = ctx.wrap_socket(sock, server_hostname=dns_server)
        wrapped_socket.connect(server)

        tcp_msg = query

        wrapped_socket.send(tcp_msg)
        data = wrapped_socket.recv(1024)

        if data:
            return data

        _log.error('Query not supported.')


class DNSUDPServer():
    """A threaded DNS proxy server."""

    def __init__(self, host="0.0.0.0", udp_port=8053, tcp=False):
        self.host = host
        self.port = udp_port

        _log.info('Listening UDP request on {}:{}'.format(host, udp_port))
        self.server = socketserver.UDPServer((host, udp_port), DNSHandler)

    def start_thread(self):
        self.thread = threading.Thread(
            target=self.server.serve_forever).start()

class DNSTCPServer():
    """A threaded DNS proxy server."""

    def __init__(self, host="0.0.0.0", tcp_port=8853, tcp=False):
        self.host = host
        self.port = tcp_port

        _log.info('Listening TCP request on {}:{}'.format(host, tcp_port))
        self.server = socketserver.TCPServer((host, tcp_port), DNSTCPHandler)

    def start_thread(self):
        self.thread = threading.Thread(
            target=self.server.serve_forever).start()
