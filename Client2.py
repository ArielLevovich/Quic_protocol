import time
# from quic import QuicConnection, QuicAddressFamily
import asyncio
from aioquic.asyncio import serve
from aioquic.h3.connection import H3_ALPN
from aioquic.quic.connection import QuicConnection
# import Quic_Connection
import Quic
from Quic_Connection import Quic_Connection


def send(server_address, file_path):
    try:
        # Create a QUIC connection to the server
        quic_client = Quic_Connection(server_address[0], server_address[1])

        with open(file_path, 'rb') as file:
            # Read the file in chunks
            chunk_size = 1024  # You can adjust the chunk size to a suitable value for your network environment
            chunk = file.read(chunk_size)
            while chunk:
                quic_client.send_packet(chunk)
                print("Sent a chunk of data")
                time.sleep(0.01)  # Short delay to prevent overwhelming the receiver
                chunk = file.read(chunk_size)

        # Close the QUIC connection
        quic_client.close()
    except Exception as e:
        print("Error sending file:", e)


def main():
    server_ip = "localhost"  # Server IP address
    server_port = 4433  # QUIC server port number

    server_address = (server_ip, server_port)

    # Path to the file to be sent
    file_path = "file.txt"

    # Send the file to the server
    send(server_address, file_path)


if __name__ == "__main__":
    main()
