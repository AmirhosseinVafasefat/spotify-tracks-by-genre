import logging

from config import LOG_FILE, LOG_DEBUG

if LOG_DEBUG:
    level = logging.DEBUG
else:
    level = logging.INFO

def setup_logger(name='logger', log_file=LOG_FILE, level=level):
    formatter = logging.Formatter(
        '%(asctime)s | %(levelname)s | %(name)s | %(message)s', 
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    handler = logging.FileHandler(log_file, encoding='utf-8')
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Avoid duplicate handlers
    if not logger.handlers:
        logger.addHandler(handler)

    return logger

logger = setup_logger()