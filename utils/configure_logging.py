import logging


def get_logger(logger_name):
    logger = logging.getLogger(logger_name)
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(logging.Formatter("%(asctime)s [%(name)s] %(levelname)s: %(message)s",
                                      datefmt="%Y-%m-%d %H:%M:%S"))
    logger.addHandler(ch)
    return logger
