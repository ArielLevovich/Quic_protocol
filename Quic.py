import socket
import time

class Quic:
    static_id = 0

    def __init__(self, sequence_number: int, is_server: bool):
        self.sequence_number = sequence_number
        self.sent_time = time.time()
        self.acknowledged = False
        self.is_server = is_server
        self.udp_socket = None
        self.ip = None
        self.port = None
        self.payload = payload

        Quic.static_id += 1

    def create_socket(self, ip: str, port: int):
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        bind_addr = (ip, port)
        self.udp_socket.bind(bind_addr)
        self.ip = ip
        self.port = port

    def create_packet(self, data: bytes):
        return data

    def do_handshake(self):
        if self.is_server:
            data, addr = self.udp_socket.recvfrom(1024)
            if data.decode() == "SYN":
                self.udp_socket.sendto(b"SYN-ACK", addr)
        else:
            self.udp_socket.sendto(b"SYN", (self.ip, self.port))
            data, addr = self.udp_socket.recvfrom(1024)
            if data.decode() == "SYN-ACK":
                self.udp_socket.sendto(b"ACK", addr)
            else:
                print("Handshake failed")

    def create_ack_packet(self, ack: int):
        return bytes(str(ack), 'utf-8')

    def data_packet(self, data: bytes):
        return data

    def create_fin_packet(self):
        return b"FIN"

    def connect(self, ip: str, port: int):
        self.udp_socket.connect((ip, port))

    def accept(self):
        data, addr = self.udp_socket.recvfrom(1024)
        return data, addr

    def send(self, data: bytes):
        self.udp_socket.sendto(data, (self.ip, self.port))

    def recv(self):
        data, addr = self.udp_socket.recvfrom(1024)
        return data

    def close(self):
        self.udp_socket.close()