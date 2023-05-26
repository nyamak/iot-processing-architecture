import database_connector
import gateway_connector
import notifier_connector
from config import config


def process(payload_dict):
    """
    Processes the payload in the dictionary format.
    """
    # Save on DB
    database_connector.save_measurement_to_db(**payload_dict)

    # Get stats for machine_id
    averages = get_averages_for_machine(**payload_dict)

    # Check for notifications
    notification_payload = notifier_connector.build_notification_payload(
        payload_dict, averages
    )
    notifier_connector.send(notification_payload)


def get_averages_for_machine(machine_id, timestamp):
    (
        temperature_avg,
        pressure_avg,
    ) = database_connector.get_averages_of_latest_measurements(machine_id, timestamp)
    defective_avg = database_connector.get_defective_average(machine_id, timestamp)

    return {
        "temperature": temperature_avg,
        "pressure": pressure_avg,
        "defective": defective_avg * 100.0,  # multiplying by 100 for pctage
    }


if __name__ == "__main__":
    connector = gateway_connector.MQTTConnector(
        config["MQTT_HOST"], config["MQTT_PORT"], config["MQTT_TOPIC"], process
    )
    connector.main()
