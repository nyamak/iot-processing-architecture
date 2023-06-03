import json
import random
import time
from datetime import datetime

from config import config
from locust import TaskSet, task
from locust.user.wait_time import between
from locust_plugins.users import MqttUser


class MyUser(MqttUser):
    host = config["MQTT_HOST"]
    port = config["MQTT_PORT"]
    wait_time = between(
        60.0 / (config["MESSAGES_PER_MINUTE_PER_USER"] - 1),
        60.0 / (config["MESSAGES_PER_MINUTE_PER_USER"] + 1),
    )

    @task
    class MyTasks(TaskSet):
        # Sleep for a while to allow the client time to connect.
        def on_start(self):
            time.sleep(5)

        @task
        def send_payload(self):
            payload = {
                "unit_id": random.randint(1, config["NUMBER_OF_UNITS"]),
                "created_at": datetime.now().isoformat(),
                # Random between True and False
                "is_defective": get_random_defective(),
                "machine_id": random.randint(1, config["NUMBER_OF_MACHINES"]),
                "machine_temperature": get_random_temperature(),
                "machine_pressure": get_random_pressure(),
            }
            payload_bytes = json.dumps(payload).replace('"', "'").encode("utf-8")
            self.client.publish(config["MQTT_TOPIC"], payload_bytes)


def get_random_pressure():
    return random.uniform(
        config["PRESSURE_LIMIT"] - 0.9, config["PRESSURE_LIMIT"] + 0.1
    )


def get_random_temperature():
    return random.uniform(
        config["TEMPERATURE_LIMIT"] - 9.0, config["TEMPERATURE_LIMIT"] + 1.0
    )


def get_random_defective():
    return random.random() < (config["DEFECTIVE_LIMIT"] / 100.0)
