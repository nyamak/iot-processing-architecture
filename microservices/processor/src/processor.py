from datetime import timedelta

import database_connector
import gateway_connector
import notifier_connector
from config import config


def process(payload_dict):
    """
    Processes the payload in the dictionary format.
    """
    # Save on DB
    database_connector.save_payload_to_db(**payload_dict)

    average_window_start = payload_dict["created_at"] - timedelta(
        seconds=config["NOTIFICATION_TIME_WINDOW"]
    )

    # Get stats for machine_id
    averages = get_averages_for_machine(
        payload_dict["machine_id"], average_window_start
    )
    if not averages:
        return

    # Check for notifications
    notification_payload = notifier_connector.build_notification_payload(
        payload_dict["machine_id"], payload_dict["created_at"], averages
    )

    if len(notification_payload.get("warnings", [])) > 0:
        notifier_connector.send(notification_payload)


def get_averages_for_machine(machine_id, timestamp):
    try:
        averages = database_connector.get_averages(machine_id, timestamp)
        return {
            "temperature": averages[0] or 0.0,
            "pressure": averages[1] or 0.0,
            "defective": (averages[2] or 0.0) * 100.0,  # multiplying by 100 for pctage
        }
    except:
        return None


if __name__ == "__main__":
    print("Starting Processor...")
    connector = gateway_connector.MQTTConnector(
        config["MQTT_HOST"], config["MQTT_PORT"], config["MQTT_TOPIC"], process
    )
    print("Starting connector.main...")
    connector.main()
