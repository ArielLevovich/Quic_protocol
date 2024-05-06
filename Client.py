# import socket
# import threading
# import time
# import random
# # import matplotlib.pyplot as plt
#
# # Constants
# HOST = 'localhost'
# PORT = 12345
# FILE_SIZE = 10 * 1024 * 1024  # 10 MB file
#
#
# def send_file(stream_id, packet_size, num_packets, addr, results):
#     sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#     start_time = time.time()
#     total_bytes_sent = 0
#
#     for _ in range(num_packets):
#         # Simulate sending a packet
#         packet = bytearray(random.getrandbits(8) for _ in range(packet_size))
#         sock.sendto(packet, addr)
#         total_bytes_sent += packet_size
#         time.sleep(0.01)  # simulate network delay
#
#     sock.close()
#     end_time = time.time()
#     duration = end_time - start_time
#     data_rate = total_bytes_sent / duration
#     packet_rate = num_packets / duration
#
#     results.append((total_bytes_sent, num_packets, data_rate, packet_rate))
#
#
# def simulate_streams(num_streams):
#     server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#     server_socket.bind((HOST, PORT))
#
#     addr = (HOST, PORT)
#     threads = []
#     results = []
#
#     for i in range(num_streams):
#         packet_size = random.randint(1000, 2000)
#         num_packets = FILE_SIZE // packet_size
#         thread = threading.Thread(target=send_file, args=(i, packet_size, num_packets, addr, results))
#         threads.append(thread)
#         thread.start()
#
#     for thread in threads:
#         thread.join()
#
#     server_socket.close()
#
#     total_data_rate = sum(r[2] for r in results) / num_streams
#     total_packet_rate = sum(r[3] for r in results) / num_streams
#
#     return (results, total_data_rate, total_packet_rate)
#
#
# def main():
#     num_streams_list = range(1, 11)  # From 1 to 10 streams
#     total_data_rates = []
#     total_packet_rates = []
#
#     for num_streams in num_streams_list:
#         _, data_rate, packet_rate = simulate_streams(num_streams)
#         total_data_rates.append(data_rate)
#         total_packet_rates.append(packet_rate)
#
#     # Plotting
#     plt.figure(figsize=(10, 5))
#     plt.subplot(1, 2, 1)
#     plt.plot(num_streams_list, total_data_rates, marker='o')
#     plt.title('Total Data Rate vs. Number of Streams')
#     plt.xlabel('Number of Streams')
#     plt.ylabel('Data Rate (Bytes/sec)')
#
#     plt.subplot(1, 2, 2)
#     plt.plot(num_streams_list, total_packet_rates, marker='o')
#     plt.title('Total Packet Rate vs. Number of Streams')
#     plt.xlabel('Number of Streams')
#     plt.ylabel('Packet Rate (Packets/sec)')
#
#     plt.tight_layout()
#     plt.show()
#
#
# if __name__ == '__main__':
#     main()
#
#
#
#
