import socket
import threading
import time
import Quic

def receive(client):
    while True:
        try:
            message, _ = client.recvfrom(1024)  # Buffer size is 1024 bytes
            print("Received:", message.decode())
        except Exception as e:
            print("Error receiving data:", e)
            break  # Exiting the loop in case of an error


def send(client, server_address, file_path):
    try:
        with open(file_path, 'rb') as file:
            # Read the file in chunks
            chunk_size = 1024  # You can adjust the chunk size to a suitable value for your network environment
            chunk = file.read(chunk_size)
            while chunk:
                client.sendto(chunk, server_address)
                print("Sent a chunk of data")
                time.sleep(0.01)  # Short delay to prevent overwhelming the receiver
                chunk = file.read(chunk_size)
    except Exception as e:
        print("Error sending file:", e)


def main():
    server_ip = "localhost"  # Server IP address
    server_port = 12345  # Server port number

    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = (server_ip, server_port)

    # Starting the receive thread
    recv_thread = threading.Thread(target=receive, args=(client,))
    recv_thread.daemon = True
    recv_thread.start()

    # Path to the file to be sent
    file_path = "file.txt"

    # Send the file to the server
    send(client, server_address, file_path)


if __name__ == "__main__":
    main()
