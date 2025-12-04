from dataclasses import dataclass


@dataclass
class Subdivision:
    id: int
    name: str
    resources: float
    kpi: float
    state: float  # S_i


@dataclass
class Link:
    id: int
    from_id: int
    to_id: int
    importance: float  # W_ij
    delay: float       # Δt_ij
