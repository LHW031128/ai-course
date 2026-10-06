import sqlite3
from contextlib import closing
from datetime import datetime


def _connect(path):
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(path):
    """할 일 테이블이 없으면 만든다."""
    with closing(_connect(path)) as conn, conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS todos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                done INTEGER NOT NULL DEFAULT 0,
                created_at TEXT NOT NULL
            )
            """
        )


def list_todos(path):
    """미완료를 먼저, 완료를 아래쪽에 두고 각각 추가한 순서로 돌려준다."""
    with closing(_connect(path)) as conn:
        return conn.execute("SELECT * FROM todos ORDER BY done, id").fetchall()


def add_todo(path, title):
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with closing(_connect(path)) as conn, conn:
        conn.execute(
            "INSERT INTO todos (title, done, created_at) VALUES (?, 0, ?)",
            (title, created_at),
        )


def toggle_todo(path, todo_id):
    """완료 여부를 뒤집는다. 해당 번호가 없으면 False를 돌려준다."""
    with closing(_connect(path)) as conn, conn:
        cur = conn.execute("UPDATE todos SET done = 1 - done WHERE id = ?", (todo_id,))
        return cur.rowcount > 0


def delete_todo(path, todo_id):
    """할 일을 지운다. 해당 번호가 없으면 False를 돌려준다."""
    with closing(_connect(path)) as conn, conn:
        cur = conn.execute("DELETE FROM todos WHERE id = ?", (todo_id,))
        return cur.rowcount > 0
