import logging.handlers

LOG_FILE = 'crawl_logs.log'

try:
    file = open(LOG_FILE)
except IOError as e:
    print('LOG FILE NOT FOUND')
    with open('crawl_logs.log', 'w'):
        pass

formatter = logging.Formatter(fmt='%(levelname)-8s [%(asctime)s] %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

handlers = [
    logging.StreamHandler(),
    logging.handlers.RotatingFileHandler(LOG_FILE, encoding='utf8', maxBytes=10000000, backupCount=1),
]


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


for h in handlers:
    h.setFormatter(formatter)
    h.setLevel(logging.DEBUG)
    logger.addHandler(h)


def info(s: str = 'default'):
    logger.info(s)


def warning(s: str = 'default'):
    logger.warning(s)


def error(s: str = 'default'):
    logger.error(s)
