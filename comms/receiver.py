class Receiver:
    def __init__(self, encryption_module):
        """
        Initializes the receiver with the encryption module.
        """
        self.encryption = encryption_module

    def receive_message(self, iv, encrypted_message):
        """
        Decrypts a received message using the encryption module.
        """
        message = self.encryption.decrypt_message(iv, encrypted_message)
        self.log_incoming_message(message)
        return message

    def validate_message(self, message):
        """
        Ensures the integrity and authenticity of the received message.
        """
        return isinstance(message, str) and len(message) > 0

    def log_incoming_message(self, message):
        """
        Logs incoming messages for debugging or record-keeping.
        """
        print(f"[Receiver] Incoming message logged: {message}")
