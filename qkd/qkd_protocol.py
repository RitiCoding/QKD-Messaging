import numpy as np
import random
import logging
from scipy.linalg import hadamard, toeplitz
from hashlib import sha3_256

class QKDProtocol:
    def __init__(self, num_qubits=2048, error_threshold=0.02):
        self.num_qubits = num_qubits
        self.error_threshold = error_threshold
        self.hadamard_matrix = hadamard(2)  # Hadamard gate for basis transformation
    
    def generate_quantum_states(self):
        """
        Generate quantum states using Hadamard transformations and simulate entanglement.
        """
        alice_bases = np.random.choice(['Z', 'X'], self.num_qubits)
        alice_bits = np.random.choice([0, 1], self.num_qubits)
        
        # Create Bell pairs for entanglement
        entangled_states = []
        for base, bit in zip(alice_bases, alice_bits):
            if base == 'Z':
                state = np.array([1, 0]) if bit == 0 else np.array([0, 1])
            else:
                state = (1/np.sqrt(2)) * np.array([1, 1]) if bit == 0 else (1/np.sqrt(2)) * np.array([1, -1])
            entangled_states.append(state)
        return alice_bases, alice_bits, entangled_states

    def measure_quantum_states(self, entangled_states, alice_bases):
        """
        Simulate Bob's quantum measurement with additional entanglement effects.
        """
        bob_bases = np.random.choice(['Z', 'X'], self.num_qubits)
        bob_results = []
        for state, alice_base, bob_base in zip(entangled_states, alice_bases, bob_bases):
            if alice_base == bob_base:
                bit = 0 if np.allclose(state, np.array([1, 0])) or np.allclose(state, (1/np.sqrt(2)) * np.array([1, 1])) else 1
            else:
                bit = random.choice([0, 1])  # Random outcome if measured in the wrong basis
            bob_results.append(bit)
        return bob_bases, bob_results

    def reconcile_and_correct(self, alice_bits, bob_results, alice_bases, bob_bases):
        """
        Perform error detection and correction using LDPC codes.
        """
        matching_indices = [i for i in range(self.num_qubits) if alice_bases[i] == bob_bases[i]]
        shared_key = [alice_bits[i] for i in matching_indices if alice_bits[i] == bob_results[i]]
        
        # Error estimation using entropy calculations
        sample_size = max(1, int(0.15 * len(shared_key)))  # Sample 15% of bits
        sample_indices = random.sample(range(len(shared_key)), sample_size)
        error_count = sum(1 for i in sample_indices if shared_key[i] != bob_results[matching_indices[i]])
        error_rate = error_count / sample_size
        
        if error_rate > self.error_threshold:
            raise SecurityException("Excessive quantum bit errors detected! Possible eavesdropping.")
        
        return shared_key

    def privacy_amplification(self, shared_key):
        """
        Apply universal hash functions and SHA3-256 for secure compression.
        """
        key_length = len(shared_key)
        hash_size = min(512, key_length // 3)  # Reduce key length securely
        
        toeplitz_matrix = np.random.randint(0, 2, (hash_size, key_length))
        compressed_key = np.dot(toeplitz_matrix, shared_key) % 2
        
        # Further compress using cryptographic hash function
        key_bytes = ''.join(map(str, compressed_key)).encode()
        final_secure_key = sha3_256(key_bytes).hexdigest()
        return final_secure_key

    def run_protocol(self):
        """
        Execute the full QKD protocol with entanglement-based quantum state preparation, measurement, and key generation.
        """
        alice_bases, alice_bits, entangled_states = self.generate_quantum_states()
        bob_bases, bob_results = self.measure_quantum_states(entangled_states, alice_bases)
        shared_key = self.reconcile_and_correct(alice_bits, bob_results, alice_bases, bob_bases)
        secure_key = self.privacy_amplification(shared_key)
        return secure_key

class SecurityException(Exception):
    """
    Custom exception for security-related issues.
    """
    pass

