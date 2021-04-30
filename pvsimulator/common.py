import logging

from time import sleep

import pika
from pika.exceptions import AMQPConnectionError


RESULTS_FILE = "/var/opt/pvsimulator/results.jsonl"
INTERVAL_SEC = 0.15
QUEUE = "meter"


def get_logger(name, level=logging.INFO):
    logging.basicConfig()
    logger = logging.getLogger(name)
    logger.setLevel(level)
    return logger


def get_rabbit_conn():
    """
    Gets a connection to RabbitMQ. Waits if it can't connect immediately.

    Returns:
        pika.BlockingConnection RabbitMQ connection object.
    """
    # Pika logs are unbelievably noisy
    logging.getLogger("pika").setLevel(logging.CRITICAL)

    timeout = 10
    waited = 0

    while waited < timeout:
        try:
            connection = pika.BlockingConnection(
                pika.ConnectionParameters("rabbit")
            )
            return connection
        except AMQPConnectionError:
            sleep(waited)
            waited += 1

    raise Exception("Timed out!")
