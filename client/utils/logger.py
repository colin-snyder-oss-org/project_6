# client/utils/logger.py
import logging

def setup_logger(name, level='INFO'):
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level))
    if not logger.handlers:
        ch = logging.StreamHandler()
        formatter = logging.Formatter('[%(asctime)s] %(name)s %(levelname)s: %(message)s')
        ch.setFormatter(formatter)
        logger.addHandler(ch)
    return logger
