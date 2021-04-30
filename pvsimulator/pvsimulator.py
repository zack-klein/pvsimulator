import json

from datetime import datetime
from random import uniform

from common import get_rabbit_conn, RESULTS_FILE, get_logger

logger = get_logger("pvsimulator")
QUEUE = "meter"


def _simulate_pv():
    """
    It's not quite clear to me how this should be simulated. Looking at the
    graph, it looks like this will be values between 0 and ~3.5 kW, so I
    will just generate random values.
    """
    return uniform(0, 3.5)


def _consume(ch, method, properties, body):
    """
    Transforms and writes consumed messages to disk. Serves as the callback
    provided to the Queue consumer.

    Args:
        - body: The body of the message.
        - We don't consume the other arguments, but the callback needs to
        accept them.
    """

    _body = json.loads(body.decode("utf-8"))

    simulated_pv = _simulate_pv()
    measurement = _body["measurement"] * 0.001  # Convert from W to kW
    total_power = simulated_pv + measurement

    result = {
        "pv": simulated_pv,
        "meter": measurement,
        "total_power": total_power,
        "timestamp": datetime.now().isoformat(),
    }

    with open(RESULTS_FILE, "a") as f:
        f.write(json.dumps(result) + "\n")

    logger.info(f"[x] Consumed: {_body}")


def consume(queue=QUEUE):
    """
    Consumes messages from the Queue.
    """
    connection = get_rabbit_conn()
    channel = connection.channel()
    channel.queue_declare(queue=queue)
    channel.basic_consume(
        queue=queue, auto_ack=True, on_message_callback=_consume
    )
    channel.start_consuming()


if __name__ == "__main__":
    consume()
