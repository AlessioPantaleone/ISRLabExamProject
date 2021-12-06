import logging


class CustomFormatter(logging.Formatter):
    grey = "\x1b[37;21m"
    yellow = "\x1b[33;21m"
    red = "\x1b[31;21m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format = "%(asctime)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"

    FORMATS = {
        logging.DEBUG: grey + format + reset,
        logging.INFO: yellow + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset,
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


def get_complete_logger(Filename: str):
    File_Handler = logging.FileHandler(Filename, "w")
    File_Handler.setFormatter(CustomFormatter())
    Console_Handler = logging.StreamHandler()
    Console_Handler.setFormatter(CustomFormatter())
    Logger = logging.getLogger()
    logging.getLogger("urllib3").setLevel(logging.WARNING)

    Logger.addHandler(Console_Handler)
    Logger.addHandler(File_Handler)
    Logger.setLevel(logging.DEBUG)

    return Logger
