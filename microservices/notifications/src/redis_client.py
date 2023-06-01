import json

from config import config
from redis import StrictRedis

_connection = None


def get_connection():
    global _connection
    if _connection is None:
        _connection = StrictRedis.from_url(
            f"redis://{config['REDIS_HOST']}:{config['REDIS_PORT']}"
        )
    return _connection


def should_send_email():
    """
    Checks if notifier should send an email.
    """
    with get_connection() as r:
        try:
            return r.get("cooldown") is None
        except:
            print("Failed to check cooldown.")
            # Allowing send if cache is down.
            return True


def set_cooldown():
    """
    Set cooldown.
    """
    with get_connection() as r:
        try:
            return r.set("cooldown", 1, ex=config["EMAIL_COOLDOWN"])
        except:
            print("Failed to set cooldown.")
            return False


def store_notification_payload(notification_payload):
    """
    Store notification payload in the cache.
    """
    with get_connection() as r:
        try:
            return r.set(
                f"payload:{notification_payload['machine_id']}",
                json.dumps(notification_payload),
                ex=config["EMAIL_COOLDOWN"],
            )
        except:
            print("Failed to store notification payload.")
            return False


def retrieve_notification_payloads():
    """
    Retrieves all notification payloads in a dict and delete their keys.
    """
    payloads = {}
    with get_connection() as r:
        try:
            for key in r.scan_iter("payload:*"):
                payload = r.get(key)
                decoded_payload = json.loads(payload)
                payloads[decoded_payload["machine_id"]] = decoded_payload
                r.delete(key)
            return payloads
        except:
            print("Failed to retrieve notifications.")
            return {}
