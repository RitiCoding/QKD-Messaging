class ErrorHandling:
    def error_reconciliation(self, key):
        """
        Corrects errors in the key caused by quantum noise.
        For simplicity, assumes a perfect reconciliation process.
        """
        # Placeholder for actual error reconciliation logic
        return key

    def detect_eavesdropping(self, error_rate, threshold):
        """
        Checks if the error rate exceeds the threshold, indicating eavesdropping.
        """
        if error_rate > threshold:
            raise SecurityException("Eavesdropping detected!")

    def privacy_amplification(self, key):
        """
        Applies a hash-based transformation on the key to reduce size and remove leaked information.
        """
        # Example privacy amplification: reduce size by taking every second bit
        return key[::2]
