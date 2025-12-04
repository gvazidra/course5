import sqlite3
from typing import List, Optional

from models import Subdivision, Link
from db import load_data
from metrics import compute_metrics, build_index
from report import print_report
from config import (
    RESOURCES_MIN, RESOURCES_MAX,
    KPI_MIN, KPI_MAX,
    STATE_MIN, STATE_MAX,
    IMPORTANCE_MIN, IMPORTANCE_MAX,
    DELAY_MIN, DELAY_MAX,
)


# вспомогательные функции

def list_subdivisions(conn: sqlite3.Connection, company_id: int) -> List[Subdivision]:
    subs, _ = load_data(conn, company_id)
    if not subs:
        print("Подразделения не найдены.")
        return []
    print("\nПодразделения компании:")
    for s in subs:
        print(f"  ID={s.id}: {s.name}, R={s.resources}, KPI={s.kpi}, S={s.state}")
    print()
    return subs


def list_links(conn: sqlite3.Connection, company_id: int) -> List[Link]:
    subs, links = load_data(conn, company_id)
    if not links:
        print("Связи не найдены.")
        return []
    sub_index = build_index(subs)
    print("\nСвязи между подразделениями:")
    for l in links:
        from_name = sub_index.get(l.from_id).name if l.from_id in sub_index else f"ID{l.from_id}"
        to_name = sub_index.get(l.to_id).name if l.to_id in sub_index else f"ID{l.to_id}"
        print(f"  ID={l.id}: {from_name} → {to_name}, W={l.importance}, Δt={l.delay} ч")
    print()
    return links


def input_float(
    prompt: str,
    default: Optional[float] = None,
    min_value: Optional[float] = None,
    max_value: Optional[float] = None,
) -> float:
    """Ввод числа с поддержкой значения по умолчанию и проверкой диапазона."""
    while True:
        s = input(prompt)
        if not s and default is not None:
            # значение по умолчанию считаем корректным
            return default
        try:
            value = float(s.replace(",", "."))
        except ValueError:
            print("Введите число.")
            continue

        # проверка диапазона
        if min_value is not None and value < min_value:
            if max_value is not None:
                print(f"Значение должно быть в диапазоне [{min_value}; {max_value}].")
            else:
                print(f"Значение должно быть не меньше {min_value}.")
            continue
        if max_value is not None and value > max_value:
            if min_value is not None:
                print(f"Значение должно быть в диапазоне [{min_value}; {max_value}].")
            else:
                print(f"Значение должно быть не больше {max_value}.")
            continue

        return value


# операции над подразделениями

def add_subdivision(conn: sqlite3.Connection, company_id: int) -> None:
    print("\n=== Добавление подразделения ===")
    name = input("Название: ").strip()
    resources = input_float(
        f"Ресурсы (R_i, {RESOURCES_MIN}–{int(RESOURCES_MAX)}): ",
        min_value=RESOURCES_MIN,
        max_value=RESOURCES_MAX,
    )
    kpi = input_float(
        f"KPI ({KPI_MIN}–{KPI_MAX}): ",
        min_value=KPI_MIN,
        max_value=KPI_MAX,
    )
    state = input_float(
        f"Состояние (S_i, {STATE_MIN}–{STATE_MAX}): ",
        min_value=STATE_MIN,
        max_value=STATE_MAX,
    )

    cur = conn.cursor()
    cur.execute("""
        INSERT INTO subdivision (company_id, name, resources, kpi, state)
        VALUES (?, ?, ?, ?, ?)
    """, (company_id, name, resources, kpi, state))
    conn.commit()
    print("Подразделение добавлено.\n")


def edit_subdivision(conn: sqlite3.Connection, company_id: int) -> None:
    subs = list_subdivisions(conn, company_id)
    if not subs:
        return
    try:
        sid = int(input("Введите ID подразделения для изменения: "))
    except ValueError:
        print("Некорректный ID.\n")
        return

    cur = conn.cursor()
    cur.execute("""
        SELECT id, name, resources, kpi, state
        FROM subdivision
        WHERE company_id = ? AND id = ?
    """, (company_id, sid))
    row = cur.fetchone()
    if not row:
        print("Подразделение не найдено.\n")
        return

    s = Subdivision(*row)
    print(f"Изменение подразделения: {s.name} (ID={s.id})")
    new_name = input(f"Новое название [{s.name}]: ").strip() or s.name
    new_resources = input_float(
        f"Ресурсы [{s.resources}] (диапазон {RESOURCES_MIN}–{int(RESOURCES_MAX)}): ",
        default=s.resources,
        min_value=RESOURCES_MIN,
        max_value=RESOURCES_MAX,
    )
    new_kpi = input_float(
        f"KPI [{s.kpi}] (диапазон {KPI_MIN}–{KPI_MAX}): ",
        default=s.kpi,
        min_value=KPI_MIN,
        max_value=KPI_MAX,
    )
    new_state = input_float(
        f"S_i [{s.state}] (диапазон {STATE_MIN}–{STATE_MAX}): ",
        default=s.state,
        min_value=STATE_MIN,
        max_value=STATE_MAX,
    )

    cur.execute("""
        UPDATE subdivision
        SET name = ?, resources = ?, kpi = ?, state = ?
        WHERE id = ? AND company_id = ?
    """, (new_name, new_resources, new_kpi, new_state, sid, company_id))
    conn.commit()
    print("Подразделение обновлено.\n")


def delete_subdivision(conn: sqlite3.Connection, company_id: int) -> None:
    """Удаление подразделения с показом связанных связей и подтверждением."""
    subs, links = load_data(conn, company_id)
    if not subs:
        print("Подразделения не найдены.\n")
        return

    print("\nТекущий список подразделений:")
    for s in subs:
        print(f"  ID={s.id}: {s.name}, R={s.resources}, KPI={s.kpi}, S={s.state}")
    print()

    try:
        sid = int(input("Введите ID подразделения для удаления: "))
    except ValueError:
        print("Некорректный ID.\n")
        return

    # ищем выбранное подразделение
    sub = next((s for s in subs if s.id == sid), None)
    if not sub:
        print("Подразделение не найдено.\n")
        return

    # находим все связи, где участвует это подразделение
    related_links = [l for l in links if l.from_id == sid or l.to_id == sid]
    sub_index = build_index(subs)

    print(f"\nВы выбрали подразделение: {sub.name} (ID={sub.id})")

    if related_links:
        print("Это подразделение участвует в следующих связях:")
        for l in related_links:
            from_name = sub_index.get(l.from_id).name if l.from_id in sub_index else f"ID{l.from_id}"
            to_name = sub_index.get(l.to_id).name if l.to_id in sub_index else f"ID{l.to_id}"
            print(f"  Связь ID={l.id}: {from_name} → {to_name}, W={l.importance}, Δt={l.delay} ч")

        print("\nЕсли вы удалите это подразделение, ВСЕ перечисленные связи")
        print("будут автоматически удалены вместе с ним.")
    else:
        print("Связей с этим подразделением не найдено.")

    confirm = input("\nВы действительно хотите удалить это подразделение? (y/n, д/н): ").strip().lower()
    if confirm not in ("y", "yes", "д", "да"):
        print("Удаление отменено.\n")
        return

    cur = conn.cursor()

    # сначала удаляем связи
    cur.execute("""
        DELETE FROM link
        WHERE company_id = ? AND (from_sub_id = ? OR to_sub_id = ?)
    """, (company_id, sid, sid))
    links_deleted = cur.rowcount

    # затем подразделение
    cur.execute("""
        DELETE FROM subdivision
        WHERE company_id = ? AND id = ?
    """, (company_id, sid))
    subs_deleted = cur.rowcount

    conn.commit()

    print(f"\nУдалено подразделений: {subs_deleted}, связанных связей: {links_deleted}.\n")


# операции над связями

def add_link(conn: sqlite3.Connection, company_id: int) -> None:
    print("\n=== Добавление связи ===")
    subs = list_subdivisions(conn, company_id)
    if not subs:
        return
    try:
        from_id = int(input("ID исходящего подразделения: "))
        to_id = int(input("ID принимающего подразделения: "))
    except ValueError:
        print("Некорректный ID.\n")
        return

    importance = input_float(
        f"Важность связи (W_ij, {IMPORTANCE_MIN}–{IMPORTANCE_MAX}): ",
        min_value=IMPORTANCE_MIN,
        max_value=IMPORTANCE_MAX,
    )
    delay = input_float(
        f"Задержка (часы, Δt_ij, {DELAY_MIN}–{DELAY_MAX}): ",
        min_value=DELAY_MIN,
        max_value=DELAY_MAX,
    )

    cur = conn.cursor()
    cur.execute("""
        INSERT INTO link (company_id, from_sub_id, to_sub_id, importance, delay_hours)
        VALUES (?, ?, ?, ?, ?)
    """, (company_id, from_id, to_id, importance, delay))
    conn.commit()
    print("Связь добавлена.\n")


def delete_link(conn: sqlite3.Connection, company_id: int) -> None:
    links = list_links(conn, company_id)
    if not links:
        return
    try:
        lid = int(input("Введите ID связи для удаления: "))
    except ValueError:
        print("Некорректный ID.\n")
        return

    cur = conn.cursor()
    cur.execute("""
        DELETE FROM link
        WHERE company_id = ? AND id = ?
    """, (company_id, lid))
    conn.commit()
    print("Связь удалена.\n")


def edit_link(conn: sqlite3.Connection, company_id: int) -> None:
    """Изменение параметров связи (важность и задержка)."""
    links = list_links(conn, company_id)
    if not links:
        return
    try:
        lid = int(input("Введите ID связи для изменения: "))
    except ValueError:
        print("Некорректный ID.\n")
        return

    cur = conn.cursor()
    cur.execute("""
        SELECT id, from_sub_id, to_sub_id, importance, delay_hours
        FROM link
        WHERE company_id = ? AND id = ?
    """, (company_id, lid))
    row = cur.fetchone()
    if not row:
        print("Связь не найдена.\n")
        return

    # row: id, from_sub_id, to_sub_id, importance, delay_hours
    l = Link(*row)
    print(f"Изменение связи: ID={l.id}")
    print(f"  От подразделения ID={l.from_id} к ID={l.to_id}")

    new_importance = input_float(
        f"Важность связи W_ij [{l.importance}] (диапазон {IMPORTANCE_MIN}–{IMPORTANCE_MAX}): ",
        default=l.importance,
        min_value=IMPORTANCE_MIN,
        max_value=IMPORTANCE_MAX,
    )
    new_delay = input_float(
        f"Задержка Δt_ij [{l.delay}] (диапазон {DELAY_MIN}–{DELAY_MAX} ч): ",
        default=l.delay,
        min_value=DELAY_MIN,
        max_value=DELAY_MAX,
    )

    cur.execute("""
        UPDATE link
        SET importance = ?, delay_hours = ?
        WHERE company_id = ? AND id = ?
    """, (new_importance, new_delay, company_id, lid))
    conn.commit()
    print("Связь обновлена.\n")


# анализ

def run_analysis(conn: sqlite3.Connection, company_id: int) -> None:
    subs, links = load_data(conn, company_id)
    if not subs:
        print("Нет данных для анализа (нет подразделений).\n")
        return
    C, D, I = compute_metrics(subs, links)
    print_report(subs, links, C, D, I)
