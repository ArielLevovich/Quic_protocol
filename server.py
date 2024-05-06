import threading
# from quic import QuicConnection, QuicAddressFamily
import Quic_Connection


def handle_client_data(quic_server):
    try:
        count = 0
        while True:
            data = quic_server.recv()
            count += 1
            if data:
                print(f"Received {len(data)} bytes")
                # Process or store data, for instance, append to a file or handle accordingly
                if len(data) < 1024:
                    print("Received all file, end")
                    break  # Assuming the end of data transmission if data received is less than 1024 bytes
            else:
                # No data means the client might have closed the connection or finished sending
                print("No data received, client may have disconnected.")
                break
    except Exception as e:
        print(f"Error handling data: {e}")


def server_main():
    host: str = "localhost"
    port = 4433
    print(f"Server is running on {host}:{port}")

    # Create a QUIC server
    quic_server = Quic_Connection.Quic_Connection(host, port)

    try:
        while True:
            # Start a new thread to handle ongoing communication with clients
            client_thread = threading.Thread(target=handle_client_data, args=(quic_server,))
            client_thread.start()
    except Exception as e:
        print("Server error:", e)
    finally:
        # Close the QUIC server
        quic_server.close()


if __name__ == "__main__":
    server_main()
