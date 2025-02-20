import time
import random
import logging
from scipy.stats import entropy
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from qkd.qkd_protocol import QKDProtocol, SecurityException
from crypto.encryption import Encryption
from crypto.key_derivation import KeyDerivation
import os


# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Function to measure execution time
def measure_time(func, *args, **kwargs):
    start_time = time.time()
    result = func(*args, **kwargs)
    end_time = time.time()
    return result, end_time - start_time

# Data collection script
def collect_data():
    results = {}

    # Step 1: QKD Key Generation Time
    qkd_protocol = QKDProtocol()
    raw_key, key_time = measure_time(qkd_protocol.run_protocol)
    results['qkd_key_time'] = key_time
    logging.info(f"QKD key generation time: {key_time:.6f} seconds")

    # Step 2: Key Entropy
    raw_key_str = ''.join(str(bit) for bit in raw_key)
    key_probs = [raw_key_str.count('0') / len(raw_key), raw_key_str.count('0') / len(raw_key)]
    key_entropy = entropy(key_probs, base=2)
    results['qkd_key_entropy'] = key_entropy
    logging.info(f"QKD key entropy: {key_entropy:.6f} bits")

    # Step 4: Encryption Time
    aes_key = os.urandom(32)
    encryption = Encryption(aes_key)
    data = "This is a test message"  # Test data
    iv = os.urandom(AES.block_size)
    ciphertext = encryption.encrypt_message(iv, data)  # Get both iv and ciphertext
    _, encryption_time = measure_time(lambda: encryption.encrypt_message(iv, data))
    results['encryption_time'] = encryption_time
    logging.info(f"Encryption time: {encryption_time:.6f} seconds")

    # Step 5: Decryption Time
    # Pass both iv and ciphertext to decrypt_message
    _, decryption_time = measure_time(lambda: encryption.decrypt_message(iv, ciphertext))  # Correct call
    results['decryption_time'] = decryption_time
    logging.info(f"Decryption time: {decryption_time:.6f} seconds")

    # Step 5: Bandwidth Overhead Simulation
    qubit_count = len(raw_key) * 2  # Assuming each bit requires 2 qubits for transmission
    reconciliation_data_size = len(raw_key) * 4  # Approximate reconciliation data size
    results['qubit_count'] = qubit_count
    results['reconciliation_data_size'] = reconciliation_data_size
    logging.info(f"Qubits transmitted: {qubit_count}")
    logging.info(f"Reconciliation data size: {reconciliation_data_size} bytes")

    # Step 7: Eavesdropping Detection Test
    try:
        qkd_protocol.simulate_eavesdropping(noise_level)  # Assuming this simulates and detects snooping
        results['eavesdropping_detected'] = True
        logging.info("Eavesdropping successfully detected.")
    except SecurityException:
        results['eavesdropping_detected'] = False
        logging.info("No eavesdropping detected.")

    # Step 8: AES Encryption Comparison
    aes_cipher = AES.new(aes_key, AES.MODE_CBC)
    iv = aes_cipher.iv  # Get the IV used for encryption
    padded_data = pad(data.encode('utf-8'), AES.block_size)

    # Measure AES Encryption Time
    _, aes_encryption_time = measure_time(aes_cipher.encrypt, padded_data)
    results['aes_encryption_time'] = aes_encryption_time
    logging.info(f"AES encryption time: {aes_encryption_time:.6f} seconds")

    # Now use the same IV for decryption
    aes_ciphertext = aes_cipher.encrypt(padded_data)

    # Re-initialize AES cipher for decryption using the same IV
    aes_cipher_decrypt = AES.new(aes_key, AES.MODE_CBC, iv)

    # Measure AES Decryption Time
    _, aes_decryption_time = measure_time(aes_cipher_decrypt.decrypt, aes_ciphertext)
    results['aes_decryption_time'] = aes_decryption_time
    logging.info(f"AES decryption time: {aes_decryption_time:.6f} seconds")

    # Final results
    logging.info("Data collection complete.")
    for metric, value in results.items():
        print(f"{metric}: {value}")

    return results


if __name__ == "__main__":
    data = collect_data()
