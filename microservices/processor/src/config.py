import os

from dotenv import load_dotenv

if os.environ.get("ENV") == "DEV":
    load_dotenv()

config = {
    "DB_HOST": os.environ.get("DB_HOST", "postgres"),
    "DB_PORT": int(os.environ.get("DB_PORT", 5432)),
    "DB_USER": os.environ.get("DB_USER"),
    "DB_PASSWORD": os.environ.get("DB_PASSWORD"),
    "DB_NAME": os.environ.get("DB_NAME"),
    "MQTT_HOST": os.environ.get("MQTT_HOST", "test.mosquitto.org"),
    "MQTT_PORT": int(os.environ.get("MQTT_PORT", 1883)),
    "MQTT_TOPIC": os.environ.get("MQTT_TOPIC", "$SYS/#"),
    "ENV": os.environ.get("ENV"),
    "NOTIFIER_HOST": os.environ.get("NOTIFIER_HOST"),
    "NOTIFIER_PORT": int(os.environ.get("NOTIFIER_PORT", 5000)),
    "TEMPERATURE_LIMIT": float(os.environ.get("TEMPERATURE_LIMIT", 75.0)),
    "PRESSURE_LIMIT": float(os.environ.get("PRESSURE_LIMIT", 1.2)),
    "DEFECTIVE_LIMIT": float(os.environ.get("DEFECTIVE_LIMIT", 5.0)),
    "NOTIFICATION_TIME_WINDOW": float(os.environ.get("NOTIFICATION_TIME_WINDOW", 60)),
}
