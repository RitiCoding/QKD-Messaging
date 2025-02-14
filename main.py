import logging
from qkd.qkd_protocol import QKDProtocol, SecurityException
from qkd.key_management import KeyManagement
from Crypto.Cipher import AES
from crypto.encryption import Encryption
from crypto.key_derivation import KeyDerivation
from comms.sender import Sender
from comms.receiver import Receiver
from comms.channel import Channel
from utils.logger import setup_logger
import os

def main():
    # Step 1: Set up logging
    setup_logger()
    logging.info("Starting the Quantum Encrypted Messaging System.")

    # Step 2: Initialize QKD and Key Management
    num_qubits = 100
    error_threshold = 0.11
    qkd = QKDProtocol(num_qubits=num_qubits, error_threshold=error_threshold)
    key_manager = KeyManagement()
    key_derivation = KeyDerivation()

    # Step 3: Perform Quantum Key Distribution
    try:
        logging.info("Performing Quantum Key Distribution...")
        raw_key = qkd.generate_key()
        logging.info(f"Raw key generated: {raw_key}")
    except SecurityException as e:
        logging.error(f"Snooping detected! Aborting communication: {e}")
        return

    # Step 4: Derive the encryption key
    channel = Channel()  # Create an instance of the Channel class
    salt = channel.simulate_classical_channel(b"random_salt")
    encryption_key = key_derivation.derive_key(raw_key, salt)
    logging.info(f"Derived encryption key: {encryption_key.hex()}")


    # Step 5: Initialize Sender and Receiver
    encryption_module = Encryption(encryption_key)
    sender = Sender(encryption_module)
    receiver = Receiver(encryption_module)

    # Step 6: Simulate a Secure Message Transmission
    iv = os.urandom(AES.block_size)  # Generate a random IV for CBC mode
    message = input("Enter the message to send securely: ")
    encrypted_message = sender.send_message(iv, message)
    logging.info(f"Encrypted message: {encrypted_message}")

    decrypted_message = receiver.receive_message(iv, encrypted_message)
    logging.info(f"Decrypted message: {decrypted_message}")

    # Step 7: Display results
    print("\n--- Secure Communication Results ---")
    print(f"Original Message: {message}")
    print(f"Encrypted Message: {encrypted_message}")
    print(f"Decrypted Message: {decrypted_message}")

if __name__ == "__main__":
    main()


