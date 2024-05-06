import time
import socket
import threading
from typing import Dict

from Quic import Quic

from aioquic.quic.configuration import QuicConfiguration
from aioquic.quic.connection import QuicConnection
from aioquic.quic.events import StreamDataReceived, ConnectionTerminated, DatagramReceived
from aioquic.asyncio import server
import asyncio
import ssl


class Quic_Connection:
    def __init__(self, ip, port, reordering_threshold=3, time_threshold=0.5):
        self.ip = ip
        self.port = port
        self.packet_number = 0
        self.outgoing_packets = {}
        self.sent_packets: Dict[int, Quic] = {}
        self.acknowledged_packets = {}
        self.largest_acknowledged = -1
        self.reordering_threshold = reordering_threshold
        self.time_threshold = time_threshold
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((ip, port))
        # threading.Thread(target=self._packet_loss_checker, daemon=True).start()

    def recv(self, seq):
        self.listen_for_packets()

    def send_packet(self, payload):
        packet = Quic(self.packet_number, payload)
        self.packet_number += 1
        self.outgoing_packets[packet.sequence] = packet
        self.sock.sendto(packet.encode(), (self.ip, self.port))
        print(f"Sent packet {packet.sequence}")

    def listen_for_packets(self):
        while True:
            data, _ = self.sock.recvfrom(1024)
            packet = Quic.decode(data)
            self.acknowledge_packet(packet.sequence)
            print(f"Received packet {packet.sequence} with payload: {packet.payload}")

    def acknowledge_packet(self, packet_number):
        if packet_number in self.outgoing_packets:
            packet = self.outgoing_packets[packet_number]
            packet.acknowledged = True
            self.largest_acknowledged = max(self.largest_acknowledged, packet_number)
            self._check_for_lost_packets()

    def _check_for_lost_packets(self):
        current_time = time.time()
        lost_packets = []
        for packet in self.outgoing_packets.values():
            if not packet.acknowledged:
                if packet.sequence < self.largest_acknowledged - self.reordering_threshold:
                    lost_packets.append(packet.sequence)
                elif (current_time - packet.send_time) > self.time_threshold:
                    lost_packets.append(packet.sequence)
        for sequence in lost_packets:
            self._handle_lost_packets(sequence)

    def _handle_lost_packets(self, sequence):
        packet = self.outgoing_packets.get(sequence)
        if packet and not packet.acknowledged:
            print(f"Packet {sequence} lost. Retransmitting...")
            self.sock.sendto(packet.encode(), (self.ip, self.port))

    def close(self):
        self.sock.close()

    def _packet_loss_checker(self):
        while True:
            self._check_for_lost_packets()
            time.sleep(0.1)  # Check for packet loss more frequently
