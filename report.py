from typing import List, Dict

from models import Subdivision, Link
from metrics import build_index
from config import KPI_LOW, STATE_HIGH, DELAY_CRIT, DELAY_WARN


def print_report(subs: List[Subdivision],
                 links: List[Link],
                 C: Dict[int, float],
                 D: Dict[int, float],
                 I: Dict[int, float]) -> None:
    """Печать результатов анализа и простых рекомендаций."""
    print("\n==================== РЕЗУЛЬТАТЫ АНАЛИЗА ====================\n")

    sorted_ids = sorted(I.keys(), key=lambda sid: I[sid])
    sub_index = build_index(subs)

    for sid in sorted_ids:
        s = sub_index[sid]

        print(f"Подразделение: {s.name} (ID={s.id})")
        print(f"  Центральность C_i       = {C[sid]:.2f}")
        print(f"  Суммарная задержка D_i  = {D[sid]:.2f}")
        print(f"  KPI                     = {s.kpi:.2f}")
        print(f"  Состояние S_i           = {s.state:.2f}")
        print(f"  Интегральный индекс I_i = {I[sid]:.2f}")

        problems: List[str] = []

        # 1. KPI
        if s.kpi < KPI_LOW:
            problems.append(
                f"- Низкий KPI ({s.kpi:.1f} < {KPI_LOW}): эффективность подразделения снижена."
            )

        # 2. состояние
        if s.state > STATE_HIGH:
            problems.append(
                f"- Высокое значение S_i ({s.state:.2f} > {STATE_HIGH}): перегруз или повышенный риск."
            )

        # 3. задержки исходящих связей
        for link in links:
            if link.from_id == sid:
                to_name = sub_index.get(link.to_id).name if link.to_id in sub_index else f"ID{link.to_id}"
                if link.delay > DELAY_CRIT:
                    problems.append(
                        f"- Критическая задержка связи {s.name} → {to_name} "
                        f"({link.delay:.1f} ч > {DELAY_CRIT} ч)."
                    )
                elif link.delay > DELAY_WARN:
                    problems.append(
                        f"- Повышенная задержка связи {s.name} → {to_name} "
                        f"({link.delay:.1f} ч > {DELAY_WARN} ч)."
                    )

        if problems:
            print("  Выявленные проблемы:")
            for p in problems:
                print("   ", p)
            print("  Возможные меры:")
            print("    * анализ причин низкой эффективности;")
            print("    * перераспределение нагрузки и ресурсов;")
            print("    * оптимизация процессов и каналов обмена данными.")
        else:
            print("  Показатели в норме. Существенных проблем не выявлено.")

        print()

    worst_id = sorted_ids[0]
    worst = sub_index[worst_id]
    print("Подразделение с наихудшим интегральным индексом:")
    print(f"  {worst.name} (ID={worst.id}, I = {I[worst_id]:.2f})")
    print("\n============================================================\n")
