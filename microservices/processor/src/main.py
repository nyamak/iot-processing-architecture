import os

import paho.mqtt.client as mqtt
from processing import process

MQTT_HOST = os.environ.get("MQTT_HOST", "test.mosquitto.org")
MQTT_PORT = os.environ.get("MQTT_PORT", 1883)
MQTT_TOPIC = os.environ.get("MQTT_TOPIC", "$SYS/#")


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe(MQTT_TOPIC)


def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))
    process(msg.payload)


def main():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(MQTT_HOST, MQTT_PORT, 60)

    client.loop_forever()
    client.disconnect()


if __name__ == "__main__":
    main()
