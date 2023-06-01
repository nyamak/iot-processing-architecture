from contextlib import contextmanager

from config import config
from psycopg2 import pool

db_pool = pool.SimpleConnectionPool(
    1,
    5,
    host=config["DB_HOST"],
    port=config["DB_PORT"],
    user=config["DB_USER"],
    password=config["DB_PASSWORD"],
    database=config["DB_NAME"],
)


@contextmanager
def _get_connection():
    conn = db_pool.getconn()

    try:
        yield conn
    finally:
        db_pool.putconn(conn)


def save_payload_to_db(
    unit_id, created_at, is_defective, machine_id, machine_temperature, machine_pressure
):
    """
    Saves all data from a payload to the database.
    """
    with _get_connection() as conn:
        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO machines(
                    machine_id
                )
                VALUES
                    (%s)
                ON CONFLICT DO NOTHING;
                """,
                (machine_id,),
            )
            cursor.execute(
                """
                INSERT INTO units(
                    machine_id, unit_id, is_defective, created_at
                )
                VALUES
                    (%s, %s, %s, %s)
                ON CONFLICT DO NOTHING;
                """,
                (machine_id, unit_id, is_defective, created_at),
            )
            cursor.execute(
                """
                INSERT INTO measurements(
                    machine_id, temperature, pressure, created_at
                )
                VALUES
                    (%s, %s, %s, %s)
                ON CONFLICT DO NOTHING;
                """,
                (machine_id, machine_temperature, machine_pressure, created_at),
            )
            cursor.close()
            conn.commit()
        except:
            conn.rollback()


def get_averages(machine_id, timestamp):
    """
    Fetch averages for all 3 metrics.
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
            result += cursor.fetchone()
            cursor.close()
            conn.commit()
            return result
        except:
            conn.rollback()
