import socket
import time
# import Quic_Connection


class Quic:
    def __init__(self, seq, payload):
        #self.udp_socket = None  # when being asked to create a socket, it will be created
        self.sequence = seq
        self.payload = payload
        self.sent_time = time.time()
        self.acknowledged = False
        self.ip = "local host"
        self.port = 12345
        #self.dick = {}
        #self.static_id = 0

    def decode(data: bytes):
        if not data:
            return {}
        # Define an empty dictionary to store decoded data
        decoded_data = {}
        # Check data type
        if isinstance(data, bytes):
            # Try to decode data as UTF-8 string
            try:
                decoded_data["data"] = data.decode("utf-8")
            except UnicodeDecodeError:
                # If decoding fails, data is treated as binary
                decoded_data["data"] = data.hex()
        else:
            # If data is not bytes, raise an error
            raise TypeError("data must be a bytes object")
        return decoded_data

    # I have no idea what I have done in hte incode!!!!!!!!!!!
    def encode(self, data: bytes):
        return data.encode()

    def create_socket(self, ip: str, port: int):
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        bind_addr = (ip, port)
        self.udp_socket.bind(bind_addr)
        self.ip = ip
        self.port = port

    def create_packet(self, data: bytes):
        return data

    def do_handshake(self):
        data, addr = self.udp_socket.recvfrom(1024)
        if data.decode() == "SYN":
            self.udp_socket.sendto(b"SYN-ACK", addr)

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

    # def send(self, data: bytes):
    #     self.dick[self.static_id] = data #
    #     self.static_id+=1
    #     data = self.encode(data)
    #     self.udp_socket.sendto(data, (self.ip, self.port))
    #
    # def recv(self,seq):
    #     data, _ = self.udp_socket.recvfrom(1024)
    #     packet = data.decode()
    #     if self._is_packet_valid(seq):
    #         packet.
    #     return data

    def _is_packet_valid(self, seq):
        return self.static_id == seq

    def close(self):
        self.udp_socket.close()
