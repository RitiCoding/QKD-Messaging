import math
from qkd.qkd_protocol import QKDProtocol

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
        return f"{seconds:.2f} seconds"
    elif seconds < 3600:
        return f"{seconds / 60:.2f} minutes"
    elif seconds < 86400:
        return f"{seconds / 3600:.2f} hours"
    elif seconds < 31536000:
        return f"{seconds / 86400:.2f} days"
    else:
        return f"{seconds / 31536000:.2f} years"

def compare_brute_force(qkd_key_length, aes_key_length, quantum=False):
    """
    Compare brute force times for QKD and AES keys.
    """
    # Brute force time estimates
    qkd_brute_force_time = display_time(2 ** (qkd_key_length / (2 if quantum else 1)) / (10**9))
    aes_brute_force_time = display_time(2 ** (aes_key_length / (2 if quantum else 1)) / (10**9))

    print("--- Brute Force Time Comparison ---")
    print(f"QKD Key Length: {qkd_key_length} bits")
    print(f"AES Key Length: {aes_key_length} bits")
    print(f"Quantum Brute Force: {'Yes' if quantum else 'No'}")
    print("Time to brute force QKD:", qkd_brute_force_time)
    print("Time to brute force AES:", aes_brute_force_time)

# Example usage
if __name__ == "__main__":
    # Initialize QKD simulation
    qkd_protocol = QKDProtocol(num_qubits=1024, error_threshold=0.05)

    # Generate a key
    qkd_key = qkd_protocol.generate_key()
    qkd_key_length = len(qkd_key)

    # AES key length (e.g., AES-256)
    aes_key_length = 256

    # Classical brute force comparison
    print("Classical Brute Force Comparison:")
    compare_brute_force(qkd_key_length=qkd_key_length, aes_key_length=aes_key_length, quantum=False)

    print("\nQuantum Brute Force Comparison:")
    # Quantum brute force comparison (Grover's algorithm)
    compare_brute_force(qkd_key_length=qkd_key_length, aes_key_length=aes_key_length, quantum=True)
