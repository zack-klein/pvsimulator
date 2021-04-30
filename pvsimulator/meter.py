import json

from random import uniform
from time import sleep

from common import get_rabbit_conn, INTERVAL_SEC, get_logger, QUEUE

logger = get_logger("meter")


def _publish_to_rabbit(val, queue=QUEUE):
    """
    Publishes a value to RabbitMQ.

    WARNING: val must be JSON serializable!

    Args:
        val - The value to publish to the queue.
        queue - Which queue to publish to. Defaults to 'meter'.
    """
    connection = get_rabbit_conn()
    channel = connection.channel()
    channel.queue_declare(queue=queue)

    _val = json.dumps(val)
    channel.basic_publish(exchange="", routing_key=queue, body=_val)
    connection.close()


def _new_entry():
    """
    Creates a random measurement.
    """
    return {"measurement": uniform(0, 9000)}


def produce():
    """
    Produces entries to the dashboard every few seconds.
    """
    while True:
        val = _new_entry()
        _publish_to_rabbit(val)
        logger.info(f"[ ] Sent: {val}")
        sleep(INTERVAL_SEC)


if __name__ == "__main__":
    produce()
