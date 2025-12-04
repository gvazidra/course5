from typing import List, Dict, Tuple

from models import Subdivision, Link
from config import ALPHA, BETA, GAMMA


def build_index(subs: List[Subdivision]) -> Dict[int, Subdivision]:
    """Словарь id -> подразделение."""
    return {s.id: s for s in subs}


def compute_metrics(subs: List[Subdivision],
                    links: List[Link]) -> Tuple[Dict[int, float], Dict[int, float], Dict[int, float]]:
    """
    Вычисление C_i, D_i и I_i для каждого подразделения.

    C_i — центральность (сумма важностей исходящих связей, нормированная на n-1).
    D_i — суммарная задержка исходящих связей.
    I_i — интегральный индекс.
    """
    n = len(subs)
    if n <= 1:
        raise ValueError("Недостаточно подразделений для анализа")

    C: Dict[int, float] = {s.id: 0.0 for s in subs}  # центральность
    D: Dict[int, float] = {s.id: 0.0 for s in subs}  # суммарная задержка

    # суммируем важность и задержки исходящих связей
    for link in links:
        C[link.from_id] += link.importance
        D[link.from_id] += link.delay

    # нормируем центральность
    for sid in C:
        C[sid] = C[sid] / (n - 1)

    # считаем интегральный индекс
    I: Dict[int, float] = {}
    for s in subs:
        sid = s.id
        I[sid] = ALPHA * C[sid] - BETA * D[sid] - GAMMA * s.state

    return C, D, I
