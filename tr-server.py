import time
import random
import socket

PORT = 9999
HOST = 'localhost'

# Set to store generated transactions
generated_transactions = set()


def generate_string(start=1, stop=1024):
    characters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    length = random.randint(start, stop)
    return ''.join(random.choice(characters) for _ in range(length))


def run_server():
    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket = None  # Initialize client_socket outside try block

    try:
        # Bind the socket to the host and port
        server_socket.bind((HOST, PORT))

        # Start listening for incoming connections
        server_socket.listen(1)  # Listen for only one client
        print(f"> Listening on {HOST}:{PORT}")

        while True:
            # Accept a client connection
            client_socket, address = server_socket.accept()
            print(f"> Accepted connection from {address[0]}:{address[1]}")

            # Loop to send transactions
            while True:
                # Generate a unique transaction
                message = generate_unique_transaction()

                # Send the transaction to the client
                client_socket.sendall(message.encode('utf-8'))
                print(f"> Sent message to {address[0]}:{address[1]}: {message}")

                # Add the transaction to the set of generated transactions
                generated_transactions.add(message)

                time.sleep(1)

    except Exception as e:
        print(f"Error: {e}")

    finally:
        if client_socket:
            client_socket.close()
        server_socket.close()


def generate_unique_transaction():
    # Generate a transaction until it is unique
    while True:
        transaction = generate_string()
        if transaction not in generated_transactions:
            return transaction


if __name__ == "__main__":
    run_server()
