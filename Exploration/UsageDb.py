import sqlite3


def initializeDb(clear=False, drop=False):
    connection = sqlite3.connect("usage.db")
    cursor = connection.cursor()

    if drop:
        cursor.execute("""DROP TABLE IF EXISTS usage""")
    elif clear:
        cursor.execute("""DELETE FROM usage""")

    cursor.execute(
        """CREATE TABLE IF NOT EXISTS usage (created_at TEXT, team_id INTEGER, method TEXT, response_status INTEGER, path TEXT, input_tokens INTEGER, output_tokens INTEGER, finetune_tokens INTEGER, price_of_request_in_cents INTEGER)"""
    )

    connection.commit()
    connection.close()


def insertData(response):
    connection = sqlite3.connect("usage.db")
    cursor = connection.cursor()

    for entry in response:
        cursor.execute(
            """SELECT count(*) FROM usage WHERE created_at = ?""", (entry["created_at"])
        )
        count = cursor.fetchone()[0]

        if count == 0:
            cursor.execute(
                """INSERT INTO usage (created_at, team_id, method, response_status, path, input_tokens, output_tokens, finetune_tokens, price_of_request_in_cents) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    entry["created_at"],
                    entry["team_id"],
                    entry["method"],
                    entry["response_status"],
                    entry["path"],
                    entry["input_tokens"],
                    entry["output_tokens"],
                    entry["finetune_tokens"],
                    entry["price_of_request_in_cents"],
                ),
            )

    connection.commit()
    connection.close()


def fetchLastTimestamp():
    connection = sqlite3.connect("usage.db")
    cursor = connection.cursor()

    cursor.execute("""SELECT created_at FROM usage ORDER BY created_at DESC LIMIT 1""")
    lastTimestamp = cursor.fetchone()

    connection.close()

    if lastTimestamp:
        return lastTimestamp[0]
    return None


def readData():
    connection = sqlite3.connect("usage.db")
    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM usage")
    calls = cursor.fetchone()[0]

    cursor.execute(
        """SELECT SUM(COALESCE(input_tokens, 0) + COALESCE(output_tokens, 0)) AS total_tokens, SUM(price_of_request_in_cents) / 100.0 AS total_spent FROM usage"""
    )
    tokens, spent = cursor.fetchone()

    connection.close()

    return calls, tokens, spent
