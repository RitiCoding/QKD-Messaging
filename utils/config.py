class Config:
    def __init__(self):
        self.settings = {
            "num_qubits": 100,
            "error_threshold": 0.11,
            "encryption_key_length": 256
        }

    def get_config(self):
        """
        Retrieves configuration settings.
        """
        return self.settings

    def update_config(self, key, value):
        """
        Updates a configuration setting.
        """
        if key in self.settings:
            self.settings[key] = value
        else:
            raise KeyError(f"Invalid configuration key: {key}")

    def reset_config(self):
        """
        Resets all configuration settings to their defaults.
        """
        self.__init__()
