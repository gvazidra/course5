"""
Глобальные настройки и коэффициенты для системы анализа.
"""

# коэффициенты для интегрального индекса

ALPHA = 1.0
BETA = 0.5
GAMMA = 1.0

# пороги для рекомендаций

KPI_LOW = 60.0
STATE_HIGH = 0.6
DELAY_CRIT = 3.0
DELAY_WARN = 1.0

# диапазоны вводимых значений (для валидации)

# ресурсы подразделения
RESOURCES_MIN = 0.0
RESOURCES_MAX = 1_000_000.0

# KPI в процентах
KPI_MIN = 0.0
KPI_MAX = 100.0

# состояние S_i
STATE_MIN = 0.0
STATE_MAX = 1.0

# важность связи W_ij
IMPORTANCE_MIN = 0.0
IMPORTANCE_MAX = 10.0

# задержка связи в часах
DELAY_MIN = 0.0
DELAY_MAX = 72.0
