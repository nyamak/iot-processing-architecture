import json
import time
import unittest

from redis_client import (
    get_connection,
    retrieve_notification_payloads,
    set_cooldown,
    should_send_email,
    store_notification_payload,
)


class RedisTests(unittest.TestCase):
    def _clear_cache(self):
        with get_connection() as r:
            r.flushall()

    def setUp(self):
        self._clear_cache()

    def tearDown(self):
        self._clear_cache()

    def test_should_send_email_true(self):
        res = should_send_email()

        self.assertTrue(res)

    def test_should_send_email_false(self):
        with get_connection() as r:
            r.set("cooldown", 1)

        res = should_send_email()

        self.assertFalse(res)

    def test_should_send_email_false_expired(self):
        with get_connection() as r:
            r.set("cooldown", 1, ex=1)
            self.assertFalse(should_send_email())
        # Wait until it expires
        time.sleep(2)

        res = should_send_email()

        self.assertTrue(res)

    def test_set_cooldown(self):
        res = set_cooldown()
        self.assertTrue(res)

    def test_store_notification_payload(self):
        payload = {
            "machine_id": 123,
            "created_at": "2022-05-18T11:40:22.519222",
            "warnings": [
                {
                    "type": "pressure",
                    "current_value": 1,
                    "target_value": 0.9,
                    "unit": "atm",
                }
            ],
        }
        res = store_notification_payload(payload)
        self.assertTrue(res)

        with get_connection() as r:
            cached = r.get("payload:123")
            self.assertEqual(cached.decode("utf-8"), json.dumps(payload))

    def test_store_notification_payload_repeated(self):
        payload_one = {
            "machine_id": 123,
            "created_at": "2022-05-18T11:40:22.519222",
            "warnings": [
                {
                    "type": "pressure",
                    "current_value": 1,
                    "target_value": 0.9,
                    "unit": "atm",
                }
            ],
        }
        self.assertTrue(store_notification_payload(payload_one))
        payload_two = {
            "machine_id": 123,
            "created_at": "2022-05-18T11:40:22.519222",
            "warnings": [
                {
                    "type": "defective",
                    "current_value": 10.0,
                    "target_value": 5.0,
                    "unit": "%",
                }
            ],
        }
        self.assertTrue(store_notification_payload(payload_two))

        with get_connection() as r:
            cached = r.get("payload:123")
            self.assertEqual(cached.decode("utf-8"), json.dumps(payload_two))

    def test_retrieve_notification_payload_success(self):
        payload = {
            "machine_id": 123,
            "created_at": "2022-05-18T11:40:22.519222",
            "warnings": [
                {
                    "type": "pressure",
                    "current_value": 1,
                    "target_value": 0.9,
                    "unit": "atm",
                }
            ],
        }
        self.assertTrue(store_notification_payload(payload))

        res = retrieve_notification_payloads()

        self.assertEqual(res, {123: payload})

    def test_retrieve_notification_payload_success_multiple(self):
        payload_one = {
            "machine_id": 123,
            "created_at": "2022-05-18T11:40:22.519222",
            "warnings": [
                {
                    "type": "pressure",
                    "current_value": 1,
                    "target_value": 0.9,
                    "unit": "atm",
                }
            ],
        }
        self.assertTrue(store_notification_payload(payload_one))
        payload_two = {
            "machine_id": 456,
            "created_at": "2022-05-18T11:40:22.519222",
            "warnings": [
                {
                    "type": "pressure",
                    "current_value": 1,
                    "target_value": 0.9,
                    "unit": "atm",
                }
            ],
        }
        self.assertTrue(store_notification_payload(payload_two))

        res = retrieve_notification_payloads()

        self.assertEqual(res, {123: payload_one, 456: payload_two})


if __name__ == "__main__":
    unittest.main()
