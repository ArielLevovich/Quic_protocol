import socket
import threading
import Quic


def handle_client_data(server_socket, client_addr):
    print(f"Handling data from client {client_addr}")
    try:
        while True:
            # Receive data from the client
            data, addr = server_socket.recvfrom(1024)
            if data:
                print(f"Received {len(data)} bytes from {addr}")
                if len(data) < 1024:
                    print("receive all file, end")
                # Process or store data, for instance, append to a file or handle accordingly
                # Send a simple acknowledgment for the received chunk
                server_socket.sendto(b"ACK", addr)
            else:
                # No data means the client might have closed the connection or finished sending
                break
    except Exception as e:
        print(f"Error handling data from {client_addr}: {e}")



def server_main():
    host = 'localhost'
    port = 12345
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((host, port))
    print(f"Server is running on {host}:{port}")
    print("Waiting for clients...")
    try:
        while True:
            # The server waits to receive some initial data or a connection initiation message
            data, client_addr = server_socket.recvfrom(1024)
            print(f"Received initial contact from {client_addr}")

            # Start a new thread to handle ongoing communication with this client
            client_thread = threading.Thread(target=handle_client_data, args=(server_socket, client_addr))
            client_thread.start()
    except Exception as e:
        print("Server error:", e)
    finally:
        server_socket.close()




if __name__ == "__main__":
    server_main()