from contextlib import contextmanager

import logging
import sqlite3


@contextmanager
def __database_context():
    connection = sqlite3.connect("database.sqlite")
    connection.row_factory = sqlite3.Row
    try:
        yield connection
        connection.commit()
    except sqlite3.Error as e:
        logging.error(e)
    finally:
        connection.close()


def query_get_admins() -> list[int] | None:
    with __database_context() as connection:
        query_result = connection.execute("SELECT user_id FROM admin").fetchall()
        return [result["user_id"] for result in query_result]


def query_get_audio(generated_id: str) -> dict | None:
    with __database_context() as connection:
        query_result = connection.execute(
            "SELECT generated_id, telegram_file_id FROM audio WHERE generated_id = ?",
            [generated_id],
        ).fetchone()
        return query_result


def query_remove_audio(generated_id: str) -> bool | None:
    with __database_context() as connection:
        query_result = connection.execute(
            "DELETE FROM audio WHERE generated_id = ?", [generated_id]
        )
        return query_result.rowcount > 0


def query_create_audio(generated_id: str, telegram_file_id: str) -> bool | None:
    with __database_context() as connection:
        connection.execute(
            "INSERT INTO audio (generated_id, telegram_file_id) VALUES (?, ?)",
            [generated_id, telegram_file_id],
        )
        return True
