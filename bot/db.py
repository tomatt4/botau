import os
import psycopg2
from psycopg2.extras import RealDictCursor, DictCursor

DATABASE_URL = os.getenv("DATABASE_URL")

def get_conn():
    return psycopg2.connect(DATABASE_URL)

def init_db():
    conn = get_conn()
    with conn:
        with conn.cursor() as cur:
            cur.execute("""
            CREATE TABLE IF NOT EXISTS birthdays (
                user_id BIGINT PRIMARY KEY,
                day INT NOT NULL,
                month INT NOT NULL
            )
            """)
    conn.close()

def upsert_birthday(user_id, day, month):
    conn = get_conn()
    with conn:
        with conn.cursor() as cur:
            cur.execute("""
            INSERT INTO birthdays (user_id, day, month)
            VALUES (%s, %s, %s)
            ON CONFLICT (user_id)
            DO UPDATE SET day = EXCLUDED.day,
                          month = EXCLUDED.month
            """, (user_id, day, month))
    conn.close()

def get_birthdays_today(day, month):
    conn = get_conn()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                SELECT user_id
                FROM birthdays
                WHERE day = %s AND month = %s
            """, (day, month))
            return cur.fetchall()
    finally:
        conn.close()

def birthday_exists(user_id, day, month):
    conn = get_conn()
    with conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT 1 FROM birthdays WHERE user_id = %s AND day = %s AND month = %s",
                (user_id, day, month)
            )
            exists = cur.fetchone() is not None
    conn.close()
    return exists

def remove_birthday(user_id, day, month):
    conn = get_conn()  # cria a conexão aqui
    with conn:
        with conn.cursor() as cur:
            cur.execute(
                "DELETE FROM birthdays WHERE user_id = %s AND day = %s AND month = %s",
                (user_id, day, month)
            )
    conn.close()

