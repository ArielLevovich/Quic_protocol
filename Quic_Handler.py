class Quic_Handler:

    def __init__(self,arr:[]):
        __data_base = {}
        for index,value in enumerate(arr):
            self.__data_base[index] = value

    #implemeinting the recovery method and date base





    # dic = {}
    # for i in dic.keys()
    #     send(i)
    #     if receive ack for i then dic.pop(i)

    class QUICConnection:
        def __init__(self, address, reordering_threshold=3, time_threshold=0.5):
            self.address = address
            self.packet_number = 0
            self.outgoing_packets = {}
            self.acknowledged_packets = {}
            self.largest_acknowledged = -1
            self.reordering_threshold = reordering_threshold
            self.time_threshold = time_threshold
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.sock.bind(('localhost', 0))
            threading.Thread(target=self._packet_loss_checker, daemon=True).start()

        def send_packet(self, payload):
            packet = QUICPacket(self.packet_number, payload.encode())
            self.packet_number += 1
            self.outgoing_packets[packet.packet_number] = packet
            self.sock.sendto(packet.encode(), self.address)
            print(f"Sent packet {packet.packet_number}")

        def listen_for_packets(self):
            while True:
                data, _ = self.sock.recvfrom(1024)
                packet = QUICPacket.decode(data)
                self.acknowledge_packet(packet.packet_number)
                print(f"Received packet {packet.packet_number} with payload: {packet.payload.decode()}")

        def acknowledge_packet(self, packet_number):
            if packet_number in self.outgoing_packets:
                self.outgoing_packets[packet_number].acknowledged = True
                self.largest_acknowledged = max(self.largest_acknowledged, packet_number)
                self._check_for_lost_packets()

        def _check_for_lost_packets(self):
            current_time = time.time()
            lost_packets = []
            for packet_number, packet in self.outgoing_packets.items():
                if not packet.acknowledged:
                    if packet_number < self.largest_acknowledged - self.reordering_threshold:
                        lost_packets.append(packet_number)
                    elif (current_time - packet.send_time) > self.time_threshold:
                        lost_packets.append(packet_number)
            for packet_number in lost_packets:
                self.handle_lost_packet(packet_number)

        def handle_lost_packet(self, packet_number):
            print(f"Packet {packet_number} lost. Retransmitting...")
            # In a real application, you might want to implement retransmission here.

        def _packet_loss_checker(self):
            while True:
                self._check_for_lost_packets()
                time.sleep(0.1)  # Check for packet loss every 100 ms