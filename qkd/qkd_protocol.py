import random
import logging

class QKDProtocol:
    def __init__(self, num_qubits=100, error_threshold=0.11):
        """
        Initializes the QKD protocol with the number of qubits and error threshold.
        """
        self.num_qubits = num_qubits
        self.error_threshold = error_threshold
    
    def simulate_measurement(self, alice_bases, alice_bits, bob_bases):
        # Simulate Bob's measurements based on Alice's bases, bits, and Bob's bases
        bob_results = []
        for alice_base, alice_bit, bob_base in zip(alice_bases, alice_bits, bob_bases):
            if alice_base == bob_base:
                bob_results.append(alice_bit)  # Bob gets the same bit if bases match
            else:
                bob_results.append(random.choice([0, 1]))  # Random result if bases mismatch
        return bob_results

    def generate_key(self):
        """
        Simulates the QKD process to generate a shared secret key between Alice and Bob.
        """
        # Step 1: Alice prepares qubits
        alice_bases = [random.choice(['X', 'Z']) for _ in range(self.num_qubits)]
        alice_bits = [random.randint(0, 1) for _ in range(self.num_qubits)]

        # Step 2: Bob measures qubits
        bob_bases = [random.choice(['X', 'Z']) for _ in range(self.num_qubits)]
        bob_results = self.simulate_measurement(alice_bases, alice_bits, bob_bases)

        # Step 3: Basis comparison
        matching_bases = [
            i for i in range(self.num_qubits) if alice_bases[i] == bob_bases[i]
        ]
        key_bits = [bob_results[i] for i in matching_bases]

        # Step 4: Error detection
        sample_size = int(len(key_bits) * 0.1)  # 10% of key for testing
        sample_indices = random.sample(range(len(key_bits)), sample_size)
        error_rate = self.calculate_error_rate(
            sample_indices, alice_bits, bob_results, matching_bases
        )

        if error_rate > self.error_threshold:
            raise SecurityException("Snooping detected! Key exchange aborted.")

        # Step 5: Privacy amplification
        final_key = self.apply_privacy_amplification(key_bits, sample_indices)
        return final_key

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

    def apply_privacy_amplification(self, key, sample_indices):
        """
        Reduces the key size by removing sampled bits for security.
        """
        return [bit for i, bit in enumerate(key) if i not in sample_indices]

class SecurityException(Exception):
    """
    Custom exception for security-related issues (e.g., eavesdropping detected).
    """
    pass
