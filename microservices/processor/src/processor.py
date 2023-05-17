import os

import database_connector
import gateway_connector
import notifier_connector


MQTT_HOST = os.environ.get("MQTT_HOST", "test.mosquitto.org")
MQTT_PORT = os.environ.get("MQTT_PORT", 1883)
MQTT_TOPIC = os.environ.get("MQTT_TOPIC", "$SYS/#")


def process(payload_dict):
    """
    Processes the payload in the dictionary format.
    """
    # Save on DB
    database_connector.save_measurement_to_db(**payload_dict)

    # Get stats for machine_id
    stats = get_stats_for_machine(**payload_dict)

    # Check for notifications
    notification_payload = notifier_connector.build_notification_payload(
        payload_dict, stats
    )
    notifier_connector.send(notification_payload)


def get_stats_for_machine(machine_id, timestamp):
    (
        temperature_avg,
        pressure_avg,
    ) = database_connector.get_averages_of_latest_measurements(machine_id, timestamp)
    defective_avg = database_connector.get_defective_average(machine_id, timestamp)

    return {
        "temperature_average": temperature_avg,
        "pressure_average": pressure_avg,
        "defective_average": defective_avg,
    }


if __name__ == "__main__":
    connector = gateway_connector.MQTTConnector(
        MQTT_HOST, MQTT_PORT, MQTT_TOPIC, process
    )
    connector.main()
