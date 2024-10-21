from contextlib import contextmanager
import sqlite3


@contextmanager
def __database_context():
  connection = sqlite3.connect("database.sqlite")
  connection.row_factory = row_factory

  try:
    yield connection
  finally:
    connection.commit()
    connection.close()


def row_factory(cursor: sqlite3.Cursor, row) -> dict:
  fields = [column[0] for column in cursor.description]
  return {key: value for key, value in zip(fields, row)}


def query_get_admins() -> list[int]:
  with __database_context() as connection:
    query_result = connection.execute(
      "SELECT user_id FROM admin",
    ).fetchall()

    return [result["user_id"] for result in query_result]


def query_get_audio(generated_id: str) -> dict:
  with __database_context() as connection:
    query_result = connection.execute(
      "SELECT generated_id, telegram_file_id FROM audio WHERE generated_id = ?",
      [generated_id],
    ).fetchone()

    return query_result


def query_remove_audio(generated_id: str) -> None:
  with __database_context() as connection:
    connection.execute(
      "DELETE FROM audio WHERE generated_id = ?",
      [generated_id],
    )


def query_create_audio(generated_id: str, telegram_file_id: str) -> None:
  with __database_context() as connection:
    connection.execute(
      "INSERT INTO audio (generated_id, telegram_file_id) VALUES (?, ?)",
      [generated_id, telegram_file_id],
    )
