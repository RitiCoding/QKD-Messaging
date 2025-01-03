import json

class Sender:
    def __init__(self, encryption_module):
        """
        Initializes the sender with the encryption module.
        """
        self.encryption = encryption_module

    def send_message(self, message):
        """
        Encrypts and sends a message over the classical channel.
        """
        encrypted_message = self.encryption.encrypt_message(message)
        self.log_outgoing_message(message)
        return encrypted_message

    def prepare_message(self, message):
        """
        Prepares the message for encryption by serializing it.
        """
        return json.dumps(message)

    def log_outgoing_message(self, message):
        """
        Logs outgoing messages for debugging or record-keeping.
        """
        print(f"[Sender] Outgoing message logged: {message}")
