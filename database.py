from contextlib import contextmanager
import sqlite3


@contextmanager
def __database_context():
  connection = sqlite3.connect("database.sqlite")
  connection.row_factory = sqlite3.Row

  try:
    yield connection
  finally:
    connection.commit()
    connection.close()


def query_get_audio(generated_id: str):
  with __database_context() as connection:
    query_result = connection.execute(
      "SELECT generated_id, telegram_file_id FROM audio WHERE generated_id = ?",
      [generated_id],
    ).fetchone()

    return query_result


def query_remove_audio(generated_id: str):
  with __database_context() as connection:
    connection.execute(
      "DELETE FROM audio WHERE generated_id = ?",
      [generated_id],
    )


def query_create_audio(generated_id: str, telegram_file_id: str):
  with __database_context() as connection:
    connection.execute(
      "INSERT INTO audio (generated_id, telegram_file_id) VALUES (?, ?)",
      [generated_id, telegram_file_id],
    )
