import sqlite3
from core.config import DB_PATH
from core.utils import now_pl_date, now_pl_datetime, days_left_signed, to_pl_date_from_any

#Współtworzone z ai

class DatabaseManager:
    def __init__(self, db_path=None):
        self.db_path = db_path or DB_PATH

    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        self._ensure_table(conn)
        return conn

    def _ensure_table(self, conn):
        conn.execute("""
        CREATE TABLE IF NOT EXISTS tasks(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            area TEXT,
            due_date TEXT,
            status TEXT NOT NULL,
            created_at TEXT NOT NULL,
            finished_at TEXT,
            left_fixed INTEGER
        )""")
        cols = {row[1] for row in conn.execute("PRAGMA table_info(tasks)").fetchall()}
        if "area" not in cols:
            conn.execute("ALTER TABLE tasks ADD COLUMN area TEXT")
        if "finished_at" not in cols:
            conn.execute("ALTER TABLE tasks ADD COLUMN finished_at TEXT")
        if "left_fixed" not in cols:
            conn.execute("ALTER TABLE tasks ADD COLUMN left_fixed INTEGER")
        conn.commit()

    def list_tasks(self, status=None, query="", area=None):
        with self.get_connection() as conn:
            q = """SELECT id, title, description, area, due_date, status, created_at, finished_at, left_fixed
                   FROM tasks WHERE 1=1"""
            params = []
            if status and status != "all":
                q += " AND status = ?"
                params.append(status)
            if area and area != "all":
                q += " AND area = ?"
                params.append(area)
            if query:
                q += " AND (LOWER(title) LIKE ? OR LOWER(description) LIKE ? OR LOWER(area) LIKE ?)"
                like = f"%{query.lower()}%"
                params += [like, like, like]
            q += " ORDER BY id DESC"
            return conn.execute(q, params).fetchall()

    def add_task(self, title, description, area, due_date, status):
        due_pl = to_pl_date_from_any(due_date) if due_date else None
        if status == "Zrobione":
            finished_at = now_pl_date()
            left_val = days_left_signed(due_pl) if due_pl else None
        else:
            finished_at = None
            left_val = None
        
        with self.get_connection() as conn:
            conn.execute(
                "INSERT INTO tasks(title, description, area, due_date, status, created_at, finished_at, left_fixed) VALUES(?,?,?,?,?,?,?,?)",
                (title, description, area or None, due_pl, status, now_pl_datetime(), finished_at, left_val)
            )
            conn.commit()

    def add_task_raw(self, title, description, area, due_pl, status, created_at, finished_at, left_fixed):
        with self.get_connection() as conn:
            conn.execute(
                "INSERT INTO tasks(title, description, area, due_date, status, created_at, finished_at, left_fixed) VALUES(?,?,?,?,?,?,?,?)",
                (title, description, area, due_pl, status, created_at, finished_at, left_fixed)
            )
            conn.commit()

    def update_task(self, task_id, title, description, area, due_pl, status, finished_at, left_fixed):
        with self.get_connection() as conn:
            conn.execute(
                "UPDATE tasks SET title=?, description=?, area=?, due_date=?, status=?, finished_at=?, left_fixed=? WHERE id=?",
                (title, description, area or None, due_pl, status, finished_at, left_fixed, task_id)
            )
            conn.commit()

    def delete_task(self, task_id):
        with self.get_connection() as conn:
            conn.execute("DELETE FROM tasks WHERE id=?", (task_id,))
            conn.commit()

    def get_distinct_areas(self):
        with self.get_connection() as conn:
            rows = conn.execute("SELECT DISTINCT area FROM tasks WHERE area IS NOT NULL AND area <> '' ORDER BY area").fetchall()
            return [r[0] for r in rows]

    def get_task_by_id(self, iid):
        with self.get_connection() as conn:
            row = conn.execute(
                "SELECT id, title, description, area, due_date, status, created_at, finished_at, left_fixed FROM tasks WHERE id=?",
                (int(iid),)
            ).fetchone()
            if not row:
                return None
            keys = ("id", "title", "description", "area", "due_date", "status", "created_at", "finished_at", "left_fixed")
            return dict(zip(keys, row))