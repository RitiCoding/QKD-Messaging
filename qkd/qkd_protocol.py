import random
import logging

class QKDProtocol:
    def __init__(self, num_qubits=256, error_threshold=0.05):
        self.num_qubits = num_qubits
        self.error_threshold = error_threshold

    def generate_key(self):
        """
        Simulate QKD key generation using a high number of qubits
        and perform basic error correction and privacy amplification.
        """
        # Simulating bases and bits for Alice and Bob
        alice_bases = [random.choice('01') for _ in range(self.num_qubits)]
        alice_bits = [random.choice('01') for _ in range(self.num_qubits)]
        bob_bases = [random.choice('01') for _ in range(self.num_qubits)]

        # Matching bases
        shared_key = [
            alice_bits[i]
            for i in range(self.num_qubits)
            if alice_bases[i] == bob_bases[i]
        ]

        # Simulate error correction by discarding random bits
        errors = int(len(shared_key) * self.error_threshold)
        for _ in range(errors):
            idx = random.randint(0, len(shared_key) - 1)
            del shared_key[idx]

        # Privacy amplification (optional truncation to 256 bits)
        if len(shared_key) > 4096:
            shared_key = shared_key[:4096]

        return ''.join(shared_key)

    def simulate_eavesdropping(self, noise_level):
        """
        Simulates eavesdropping in the QKD protocol by adding noise to the key.
        Higher noise level means more eavesdropping.
        """
        # Simulate eavesdropping by introducing random noise to the key.
        # This is a simple example of how noise could be simulated.
        if random.random() < noise_level:
            raise SecurityException("Eavesdropping detected!")
        else:
            logging.info("No eavesdropping detected.")

    def calculate_error_rate(self, sample_indices, alice_bits, bob_results, matching_bases):
        """
        Calculates the error rate of the key exchange based on a sampled subset.
        """
        errors = 0
        for idx in sample_indices:
            if alice_bits[matching_bases[idx]] != bob_results[matching_bases[idx]]:
                errors += 1
        return errors / len(sample_indices)

    def simulate_measurement(self, alice_bases, alice_bits, bob_bases):
        # Simulate Bob's measurements based on Alice's bases, bits, and Bob's bases
        bob_results = []
        for alice_base, alice_bit, bob_base in zip(alice_bases, alice_bits, bob_bases):
            if alice_base == bob_base:
                bob_results.append(alice_bit)  # Bob gets the same bit if bases match
            else:
                bob_results.append(random.choice([0, 1]))  # Random result if bases mismatch
        return bob_results

class SecurityException(Exception):
    """
    Custom exception for security-related issues (e.g., eavesdropping detected).
    """
    pass
