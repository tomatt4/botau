import psycopg2

# conexão direta
def get_conn():
    return psycopg2.connect(
        host="localhost",
        database="angel's",
        user="postgres",
        password="senhadosalva"
    )


def init_db():
    conn = get_conn()

    with conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS tickets (
                    id SERIAL PRIMARY KEY,
                    user_id TEXT,
                    channel_id TEXT,
                    type TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

    conn.close()
