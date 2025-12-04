import sqlite3
from typing import List, Tuple

from models import Subdivision, Link


def connect_db(db_path: str) -> sqlite3.Connection:
    """Подключение к БД SQLite."""
    return sqlite3.connect(db_path)


def load_data(conn: sqlite3.Connection, company_id: int) -> Tuple[List[Subdivision], List[Link]]:
    """Загрузка подразделений и связей из БД SQLite."""
    cur = conn.cursor()

    cur.execute("""
        SELECT id, name, resources, kpi, state
        FROM subdivision
        WHERE company_id = ?
        ORDER BY id
    """, (company_id,))
    subs = [Subdivision(*row) for row in cur.fetchall()]

    cur.execute("""
        SELECT id, from_sub_id, to_sub_id, importance, delay_hours
        FROM link
        WHERE company_id = ?
        ORDER BY id
    """, (company_id,))
    links = [Link(*row) for row in cur.fetchall()]

    return subs, links
