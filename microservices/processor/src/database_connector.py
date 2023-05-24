import os
from contextlib import contextmanager
from datetime import datetime

from psycopg2 import pool

DB_HOST = os.environ.get("DB_HOST")
DB_PORT = int(os.environ.get("DB_PORT"))
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_NAME = os.environ.get("DB_NAME")

db_pool = pool.SimpleConnectionPool(
    1,
    5,
    host=DB_HOST,
    port=DB_PORT,
    user=DB_USER,
    password=DB_PASSWORD,
    database=DB_NAME,
)


@contextmanager
def _get_connection():
    conn = db_pool.getconn()

    try:
        yield conn
    finally:
        db_pool.putconn(conn)


def save_unit_to_db(machine_id, unit_id, is_defective, created_at):
    """
    Saves a new unit to the database.
    """
    created_at = datetime.fromisoformat(created_at)
    with _get_connection() as conn:
        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO units(
                    machine_id, unit_id, is_defective, created_at
                )
                VALUES
                    (%s, %s, %s, %s);
                """,
                (machine_id, unit_id, is_defective, created_at),
            )
            cursor.close()
            conn.commit()
        except:
            conn.rollback()


def save_measurement_to_db(machine_id, temperature, pressure, created_at):
    """
    Saves a new measurement to the database.
    """
    created_at = datetime.fromisoformat(created_at)
    with _get_connection() as conn:
        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO measurements(
                    machine_id, temperature, pressure, created_at
                )
                VALUES
                    (%s, %s, %s, %s);
                """,
                (machine_id, temperature, pressure, created_at),
            )
            cursor.close()
            conn.commit()
        except:
            conn.rollback()


def get_averages_of_latest_measurements(machine_id, timestamp):
    """
    Fetches averages of latest measurements from device with machine_id, up until timestamp.
    """
    with _get_connection() as conn:
        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT
                    AVG(temperature),
                    AVG(pressure)
                FROM
                    measurements
                WHERE
                    machine_id = %s
                    AND created_at >= %s;
                """,
                (machine_id, timestamp),
            )
            result = cursor.fetchone()
            cursor.commit()
            cursor.close()
            return result
        except:
            conn.rollback()


def get_defective_average(machine_id, timestamp):
    """
    Fetches rate of defective products for a machine_id from timestamp to now.
    """
    with _get_connection() as conn:
        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT
                    AVG(is_defective::int::float4)
                FROM
                    units
                WHERE
                    machine_id = %s
                    AND created_at >= %s;
                """,
                (machine_id, timestamp),
            )
            result = cursor.fetchone()
            cursor.commit()
            cursor.close()
            return result
        except:
            conn.rollback()
