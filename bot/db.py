import os
import psycopg2
from psycopg2.extras import RealDictCursor

DATABASE_URL = os.getenv("DATABASE_URL")


def get_conn():
    return psycopg2.connect(DATABASE_URL)


def init_db():
    conn = get_conn()
    with conn:
        with conn.cursor() as cur:

            # 🎂 Birthdays
            cur.execute("""
            CREATE TABLE IF NOT EXISTS birthdays (
                user_id BIGINT PRIMARY KEY,
                day INT NOT NULL,
                month INT NOT NULL
            );
            """)

            # 🎫 Tickets
            cur.execute("""
            CREATE TABLE IF NOT EXISTS tickets (
                id SERIAL PRIMARY KEY,
                user_id TEXT NOT NULL,
                channel_id TEXT NOT NULL UNIQUE,
                type TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """)

            # ⚠️ Warns
            cur.execute("""
            CREATE TABLE IF NOT EXISTS warns (
                id SERIAL PRIMARY KEY,
                user_id TEXT NOT NULL,
                moderator_id TEXT NOT NULL,
                reason TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """)

            # 📊 User Stats (mensagens + call)
            cur.execute("""
            CREATE TABLE IF NOT EXISTS user_stats (
                user_id BIGINT PRIMARY KEY,
                mensagens BIGINT DEFAULT 0,
                tempo_call BIGINT DEFAULT 0
            );
            """)
            # 📬 Tellonym
            cur.execute("""
            CREATE TABLE IF NOT EXISTS tellonym (
            id SERIAL PRIMARY KEY,
            message TEXT NOT NULL,
            replied BOOLEAN DEFAULT FALSE,
            reply TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """)

    conn.close()

# ───────────── STATS ─────────────

def garantir_usuario_stats(user_id: int):
    conn = get_conn()
    with conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO user_stats (user_id) VALUES (%s) "
                "ON CONFLICT (user_id) DO NOTHING;",
                (user_id,)
            )
    conn.close()


def add_mensagem(user_id: int):
    conn = get_conn()
    with conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO user_stats (user_id, mensagens)
                VALUES (%s, 1)
                ON CONFLICT (user_id)
                DO UPDATE SET mensagens = user_stats.mensagens + 1;
                """,
                (user_id,)
            )
    conn.close()


def add_tempo_call(user_id: int, segundos: int):
    conn = get_conn()
    with conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO user_stats (user_id, tempo_call)
                VALUES (%s, %s)
                ON CONFLICT (user_id)
                DO UPDATE SET tempo_call = user_stats.tempo_call + %s;
                """,
                (user_id, segundos, segundos)
            )
    conn.close()


def get_stats(user_id: int):
    conn = get_conn()
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(
            "SELECT mensagens, tempo_call FROM user_stats WHERE user_id = %s;",
            (user_id,)
        )
        data = cur.fetchone()
    conn.close()
    return data
