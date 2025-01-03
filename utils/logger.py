import logging

def setup_logger():
    """
    Configures the logger for the application.
    """
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[logging.StreamHandler()]
    )

def log_info(message):
    """
    Logs informational messages.
    """
    logging.info(message)

def log_warning(message):
    """
    Logs warnings.
    """
    logging.warning(message)

def log_error(message):
    """
    Logs critical errors.
    """
    logging.error(message)
