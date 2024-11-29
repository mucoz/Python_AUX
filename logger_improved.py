import logging
import os
from datetime import datetime


class Logger:
    _configured = False

    @staticmethod
    def configure(
        log_dir="Logs",
        log_level=logging.INFO,
        log_format="%(levelname)s %(asctime)s [%(name)s] - %(message)s",
    ):
        """
        Configures the root logger. Should be called once at the start of the application.
        """
        if Logger._configured:
            return

        # Ensure the logs directory exists
        if not os.path.exists(log_dir):
            os.mkdir(log_dir)

        # Create log file with date
        log_file = os.path.join(log_dir, f"Log_{datetime.now().strftime('%Y-%m-%d')}.log")

        # Set up handlers
        formatter = logging.Formatter(log_format)

        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)

        # Configure the root logger
        root_logger = logging.getLogger()
        root_logger.setLevel(log_level)
        root_logger.addHandler(file_handler)
        root_logger.addHandler(stream_handler)

        Logger._configured = True

    @staticmethod
    def get_logger(module_name):
        """
        Returns a logger instance for the specified module.
        """
        if not Logger._configured:
            raise RuntimeError("Logger has not been configured. Call Logger.configure() first.")
        return logging.getLogger(module_name)

    @staticmethod
    def start():
        logger = Logger.get_logger("SYSTEM")
        logger.info("=" * 20 + " NEW PROCESS " + "=" * 20)
        logger.info("Process started by: " + os.environ.get('USERNAME', 'Unknown'))

    @staticmethod
    def finish():
        logger = Logger.get_logger("SYSTEM")
        logger.info("=" * 20 + " END PROCESS " + "=" * 20)
