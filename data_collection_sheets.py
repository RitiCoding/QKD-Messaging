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
import math


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
    raw_key, key_time = measure_time(qkd_protocol.generate_key)
    #results['qkd_key_time'] = key_time
    print(key_time)

    # Step 2: Key Entropy
    raw_key_str = ''.join(str(bit) for bit in raw_key)
    key_probs = [raw_key_str.count('0') / len(raw_key), raw_key_str.count('0') / len(raw_key)]
    key_entropy = entropy(key_probs, base=2)
    #results['qkd_key_entropy'] = key_entropy
    print(key_entropy)

    # Step 4: Encryption Time
    aes_key = os.urandom(32)
    encryption = Encryption(aes_key)
    data = "This is a test message"  # Test data
    iv = os.urandom(AES.block_size)
    ciphertext = encryption.encrypt_message(iv, data)  # Get both iv and ciphertext
    _, encryption_time = measure_time(lambda: encryption.encrypt_message(iv, data))
    #results['encryption_time'] = encryption_time
    print(encryption_time)

    # Step 5: Decryption Time
    # Pass both iv and ciphertext to decrypt_message
    _, decryption_time = measure_time(lambda: encryption.decrypt_message(iv, ciphertext))  # Correct call
    #results['decryption_time'] = decryption_time
    print(decryption_time)

    # Step 5: Bandwidth Overhead Simulation
    qubit_count = len(raw_key) * 2  # Assuming each bit requires 2 qubits for transmission
    reconciliation_data_size = len(raw_key) * 4  # Approximate reconciliation data size
    #results['qubit_count'] = qubit_count
    #results['reconciliation_data_size'] = reconciliation_data_size
    print(qubit_count)
    print(reconciliation_data_size)

    # Step 6: Error Rate Simulation
    noise_level = 0.1  # Simulate 10% noise in the channel
    noisy_key = [int(bit) if random.random() > noise_level else 1 - int(bit) for bit in raw_key]
    error_count = sum(1 for a, b in zip(raw_key, noisy_key) if a != b)
    error_rate = error_count / len(raw_key)
    #results['error_rate'] = error_rate
    print(error_rate)

    # Step 7: Eavesdropping Detection Test
    # try:
    #     qkd_protocol.simulate_eavesdropping(noise_level)  # Assuming this simulates and detects snooping
    #     results['eavesdropping_detected'] = True
    #     logging.info("Eavesdropping successfully detected.")
    # except SecurityException:
    #     results['eavesdropping_detected'] = False
    #     logging.info("No eavesdropping detected.")

    # Step 8: AES Encryption Comparison
    aes_cipher = AES.new(aes_key, AES.MODE_CBC)
    iv = aes_cipher.iv  # Get the IV used for encryption
    padded_data = pad(data.encode('utf-8'), AES.block_size)

    # Measure AES Encryption Time
    _, aes_encryption_time = measure_time(aes_cipher.encrypt, padded_data)
    #results['aes_encryption_time'] = aes_encryption_time
    print(aes_encryption_time)

    # Now use the same IV for decryption
    aes_ciphertext = aes_cipher.encrypt(padded_data)

    # Re-initialize AES cipher for decryption using the same IV
    aes_cipher_decrypt = AES.new(aes_key, AES.MODE_CBC, iv)

    # Measure AES Decryption Time
    _, aes_decryption_time = measure_time(aes_cipher_decrypt.decrypt, aes_ciphertext)
    #results['aes_decryption_time'] = aes_decryption_time
    print(aes_decryption_time)

    # Final results
#    logging.info("Data collection complete.")
    for metric, value in results.items():
        print(f"{metric}: {value}")

    return results

def brute_force_time(key_length, quantum=True, classical_speed=1e9):
    """
    Estimate the time to brute force a key.
    
    Parameters:
    - key_length: Length of the key in bits.
    - quantum: If True, assumes Grover's algorithm is used.
    - classical_speed: Number of operations per second (default is 1 billion).
    
    Returns:
    - Estimated time in seconds.
    """
    total_keys = 2 ** key_length

    # Grover's algorithm reduces brute force attempts to sqrt(total_keys)
    effective_keys = math.sqrt(total_keys) if quantum else total_keys

    # Estimate time based on classical speed
    time_seconds = effective_keys / classical_speed
    return time_seconds

def display_time(seconds):
    """
    Convert time in seconds to human-readable format.
    """
    if seconds < 60:
        return seconds
    elif seconds < 3600:
        return seconds / 60
    elif seconds < 86400:
        return seconds / 3600
    elif seconds < 31536000:
        return seconds / 86400
    else:
        return seconds / 31536000

def compare_brute_force(qkd_key_length, aes_key_length, quantum=False):
    """
    Compare brute force times for QKD and AES keys.
    """
    # Brute force time estimates
    qkd_brute_force_time = display_time(2 ** (qkd_key_length / (2 if quantum else 1)) / (10**9))
    aes_brute_force_time = display_time(2 ** (aes_key_length / (2 if quantum else 1)) / (10**9))

#    print("--- Brute Force Time Comparison ---")
    print(qkd_key_length)
    print(aes_key_length)
#    print(f"Quantum Brute Force: {'Yes' if quantum else 'No'}")
    print(qkd_brute_force_time)
    print(aes_brute_force_time)

def estimate_computing_power(key_length_bits, num_qubits, num_repetitions, clock_speed_ghz):
    """
    Estimate the computational power required to run a QKD simulation.

    Parameters:
    - key_length_bits: Length of the QKD key in bits.
    - num_qubits: Number of qubits processed per run.
    - num_repetitions: Number of protocol repetitions for key generation.
    - clock_speed_ghz: Clock speed of the hardware in GHz.

    Returns:
    - total_operations: Total number of operations required.
    - time_required_seconds: Estimated time required for simulation (in seconds).
    """
    # Estimate operations per key bit
    operations_per_qubit = 1000  # Assume 1000 operations per qubit for error correction, privacy amplification, etc.
    operations_per_bit = operations_per_qubit * num_qubits

    # Total operations
    total_operations = operations_per_bit * key_length_bits * num_repetitions

    # Compute time required (assuming 1 GHz = 1 billion operations per second)
    time_required_seconds = total_operations / (clock_speed_ghz * 1e9)

    return total_operations, time_required_seconds


def display_results(total_operations, time_required_seconds, clock_speed_ghz):
    """
    Display the results in a readable format.
    """
#    print("\n--- QKD Simulation Computational Power Estimate ---")
    print(total_operations)
    print(time_required_seconds)
    print(clock_speed_ghz)
#    print("----------------------------------------------------")


if __name__ == "__main__":
#     data = collect_data()

# #    Initialize QKD simulation
#     num_qubits = 1024
#     error_threshold = .05
#     qkd_protocol = QKDProtocol(num_qubits, error_threshold)

# #    Generate a key
#     qkd_key = qkd_protocol.generate_key()
#     qkd_key_length = len(qkd_key)

#     # AES key length (e.g., AES-256)
#     aes_key_length = 256

#     # Classical brute force comparison
# #    print("Classical Brute Force Comparison:")
#     compare_brute_force(qkd_key_length=qkd_key_length, aes_key_length=aes_key_length, quantum=False)

# #    print("\nQuantum Brute Force Comparison:")
#     # Quantum brute force comparison (Grover's algorithm)
#     compare_brute_force(qkd_key_length=qkd_key_length, aes_key_length=aes_key_length, quantum=True)

# #    Input parameters for the QKD simulation
#     num_repetitions = 1
#     clock_speed_ghz = 1

#     # Estimate computing power
#     total_operations, time_required_seconds = estimate_computing_power(
#         qkd_key_length, num_qubits, num_repetitions, clock_speed_ghz
#     )

#     # Display results
#     display_results(total_operations, time_required_seconds, clock_speed_ghz)
    num_qubits = 1590
    for i in range(530):
        num_qubits = num_qubits + 1
        error_threshold = .05
        qkd_protocol = QKDProtocol(num_qubits, error_threshold)
        qkd_key = qkd_protocol.generate_key()
        qkd_key_length = len(qkd_key)
        num_repetitions = 1
        clock_speed_ghz = 1
        quantum = True
        total_operations, time_required_seconds = estimate_computing_power(qkd_key_length, num_qubits, num_repetitions, clock_speed_ghz)
        qkd_brute_force_time = 2 ** (qkd_key_length / (2 if quantum else 1)) / (10**9)
        print(qkd_brute_force_time)
#        print(time_required_seconds)
