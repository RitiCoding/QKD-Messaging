class Channel:
    def simulate_quantum_channel(self, qubits):
        """
        Simulates the behavior of a quantum channel, including potential noise.
        """
        # Introduce noise randomly to simulate real-world behavior
        noisy_qubits = [q ^ 1 if random.random() < 0.1 else q for q in qubits]
        return noisy_qubits

    def simulate_classical_channel(self, data):
        """
        Simulates the classical communication channel.
        """
        print("[Channel] Sending data over classical channel...")
        return data

    def introduce_noise(self, qubits):
        """
        Adds noise to the quantum channel.
        """
        return [q ^ 1 if random.random() < 0.05 else q for q in qubits]

    def simulate_eavesdropping(self, qubits):
        """
        Simulates an eavesdropper intercepting and measuring qubits.
        """
        return [random.randint(0, 1) for _ in qubits]  # Random measurements
