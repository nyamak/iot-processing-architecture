import os
import json

import paho.mqtt.client as mqtt

from process import process

MQTT_HOST = os.environ.get('MQTT_HOST', "test.mosquitto.org")
MQTT_PORT = os.environ.get('MQTT_PORT', 1883)
MQTT_TOPIC = os.environ.get('MQTT_TOPIC',"$SYS/#")

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe(MQTT_TOPIC)

def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    converted_payload = to_dict(msg.payload)
    if converted_payload:
        process(converted_payload)

def to_dict(payload_bytes):
    try:
        decoded_payload = payload_bytes.decode('utf-8').replace("'", '"')
        return json.dumps(decoded_payload)
    except Exception:
        return None


def main():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(MQTT_HOST, MQTT_PORT, 60)

    client.loop_forever()
    client.disconnect()

if __name__ == '__main__':
    main()
