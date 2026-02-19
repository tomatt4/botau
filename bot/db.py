import os
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime, timedelta

DATABASE_URL = os.getenv("DATABASE_URL")


# ───────────── CONEXÃO ─────────────

def get_conn():
    return psycopg2.connect(DATABASE_URL)


# ───────────── INIT DB ─────────────

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

            # 📊 User Stats
            cur.execute("""
            CREATE TABLE IF NOT EXISTS user_stats (
                user_id BIGINT PRIMARY KEY,
                mensagens BIGINT DEFAULT 0,
                tempo_call BIGINT DEFAULT 0
            );
            """)

            # 📬 Tellonym (público, anônimo, com cooldown)
            cur.execute("""
            CREATE TABLE IF NOT EXISTS tellonym (
                id SERIAL PRIMARY KEY,
                user_id BIGINT NOT NULL,
                message TEXT NOT NULL,
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
                """
                INSERT INTO user_stats (user_id)
                VALUES (%s)
                ON CONFLICT (user_id) DO NOTHING;
                """,
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
            """
            SELECT mensagens, tempo_call
            FROM user_stats
            WHERE user_id = %s;
            """,
            (user_id,)
        )
        data = cur.fetchone()
    conn.close()
    return data


# ───────────── TELLONYM ─────────────

def pode_enviar_tellonym(user_id: int) -> bool:
    """
    Retorna True se o usuário puder enviar outro Tellonym
    (cooldown de 1 hora).
    """
    conn = get_conn()
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(
            """
            SELECT created_at
            FROM tellonym
            WHERE user_id = %s
            ORDER BY created_at DESC
            LIMIT 1;
            """,
            (user_id,)
        )
        last = cur.fetchone()
    conn.close()

    # nunca enviou
    if not last:
        return True

    agora = datetime.utcnow()
    ultima = last["created_at"]

    return (agora - ultima) >= timedelta(hours=1)


def add_tellonym(user_id: int, message: str) -> int:
    conn = get_conn()
    with conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO tellonym (user_id, message)
                VALUES (%s, %s)
                RETURNING id;
                """,
                (user_id, message)
            )
            tellonym_id = cur.fetchone()[0]
    conn.close()
    return tellonym_id

def get_tellonyms(limit: int = 10):
    conn = get_conn()
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(
            """
            SELECT id, message, created_at
            FROM tellonym
            ORDER BY created_at DESC
            LIMIT %s;
            """,
            (limit,)
        )
        data = cur.fetchall()
    conn.close()
    return data
