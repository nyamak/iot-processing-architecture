import os

from dotenv import load_dotenv

load_dotenv()

config = {
    "MQTT_HOST": os.environ.get("MQTT_HOST", "127.0.0.1"),
    "MQTT_PORT": int(os.environ.get("MQTT_PORT", 1883)),
    "MQTT_TOPIC": os.environ.get("MQTT_TOPIC", "payloads"),
    "PRESSURE_LIMIT": float(os.environ.get("PRESSURE_LIMIT", 1.2)),
    "TEMPERATURE_LIMIT": float(os.environ.get("TEMPERATURE_LIMIT", 75.0)),
    "DEFECTIVE_LIMIT": float(os.environ.get("DEFECTIVE_LIMIT", 5.0)),
    "NUMBER_OF_MACHINES": int(os.environ.get("NUMBER_OF_MACHINES", 100)),
    "NUMBER_OF_UNITS": int(os.environ.get("NUMBER_OF_UNITS", 100000)),
    "MESSAGES_PER_MINUTE_PER_USER": int(
        os.environ.get("MESSAGES_PER_MINUTE_PER_USER", 10)
    ),
}
