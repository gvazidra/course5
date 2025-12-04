PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS link;
DROP TABLE IF EXISTS subdivision;
DROP TABLE IF EXISTS company;

-- Таблица компаний
CREATE TABLE company (
    id   INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);

-- Таблица подразделений
CREATE TABLE subdivision (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id INTEGER NOT NULL,
    name       TEXT NOT NULL,
    resources  REAL NOT NULL,  -- R_i
    kpi        REAL NOT NULL,  -- KPI
    state      REAL NOT NULL,  -- S_i
    FOREIGN KEY (company_id) REFERENCES company(id)
);

-- Таблица связей
CREATE TABLE link (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id INTEGER NOT NULL,
    from_sub_id INTEGER NOT NULL,
    to_sub_id   INTEGER NOT NULL,
    importance  REAL NOT NULL,   -- W_ij
    delay_hours REAL NOT NULL,   -- Δt_ij (часы)
    FOREIGN KEY (company_id) REFERENCES company(id),
    FOREIGN KEY (from_sub_id) REFERENCES subdivision(id),
    FOREIGN KEY (to_sub_id)   REFERENCES subdivision(id)
);

BEGIN TRANSACTION;

-- =========================
-- СЦЕНАРИИ (company)
-- =========================

INSERT INTO company (id, name) VALUES
  (1, 'Сценарий 1: базовая структура'),
  (2, 'Сценарий 2: высокие задержки'),
  (3, 'Сценарий 3: низкие KPI'),
  (4, 'Сценарий 4: высокая нагрузка'),
  (5, 'Сценарий 5: граничные значения');

-- =========================
-- СЦЕНАРИЙ 1: базовая структура (company_id = 1)
-- =========================

INSERT INTO subdivision (id, company_id, name, resources, kpi, state) VALUES
  (1, 1, 'Центральный офис', 120.0, 0.82, 0.20),
  (2, 1, 'Филиал A',          80.0, 0.78, 0.25),
  (3, 1, 'Филиал B',          75.0, 0.76, 0.22);

INSERT INTO link (id, company_id, from_sub_id, to_sub_id, importance, delay_hours) VALUES
  (1, 1, 1, 2, 0.8, 2.0),
  (2, 1, 1, 3, 0.7, 2.5),
  (3, 1, 2, 3, 0.5, 1.5),
  (4, 1, 3, 2, 0.4, 1.7);

-- =========================
-- СЦЕНАРИЙ 2: высокие задержки (company_id = 2)
-- =========================

INSERT INTO subdivision (id, company_id, name, resources, kpi, state) VALUES
  (11, 2, 'Центральный офис', 120.0, 0.82, 0.20),
  (12, 2, 'Филиал A',          80.0, 0.78, 0.25),
  (13, 2, 'Филиал B',          75.0, 0.76, 0.22);

INSERT INTO link (id, company_id, from_sub_id, to_sub_id, importance, delay_hours) VALUES
  (11, 2, 11, 12, 0.8,  8.0),
  (12, 2, 11, 13, 0.7, 10.0),
  (13, 2, 12, 13, 0.5,  9.0),
  (14, 2, 13, 12, 0.4,  7.5);

-- =========================
-- СЦЕНАРИЙ 3: низкие KPI (company_id = 3)
-- =========================

INSERT INTO subdivision (id, company_id, name, resources, kpi, state) VALUES
  (21, 3, 'Центральный офис', 120.0, 0.80, 0.20),
  (22, 3, 'Филиал A',          80.0, 0.35, 0.30),
  (23, 3, 'Филиал B',          70.0, 0.28, 0.32),
  (24, 3, 'Филиал C',          65.0, 0.30, 0.27);

INSERT INTO link (id, company_id, from_sub_id, to_sub_id, importance, delay_hours) VALUES
  (21, 3, 21, 22, 0.8, 2.5),
  (22, 3, 21, 23, 0.7, 3.0),
  (23, 3, 21, 24, 0.6, 3.0),
  (24, 3, 22, 23, 0.5, 1.5),
  (25, 3, 23, 24, 0.4, 1.8);

-- =========================
-- СЦЕНАРИЙ 4: высокая нагрузка (company_id = 4)
-- =========================

INSERT INTO subdivision (id, company_id, name, resources, kpi, state) VALUES
  (31, 4, 'Центральный офис', 130.0, 0.82, 0.30),
  (32, 4, 'Филиал A',          85.0, 0.75, 0.80),
  (33, 4, 'Филиал B',          90.0, 0.77, 0.90),
  (34, 4, 'Филиал C',          60.0, 0.70, 0.70);

INSERT INTO link (id, company_id, from_sub_id, to_sub_id, importance, delay_hours) VALUES
  (31, 4, 31, 32, 0.9, 2.0),
  (32, 4, 31, 33, 0.9, 2.0),
  (33, 4, 31, 34, 0.7, 2.5),
  (34, 4, 32, 33, 0.6, 1.5),
  (35, 4, 33, 34, 0.5, 1.5);

-- =========================
-- СЦЕНАРИЙ 5: граничные значения (company_id = 5)
-- =========================

INSERT INTO subdivision (id, company_id, name, resources, kpi, state) VALUES
  (41, 5, 'Центральный офис', 0.0,  0.00, 0.00),
  (42, 5, 'Филиал A',         0.0,  0.10, 1.00),
  (43, 5, 'Филиал B',         10.0, 0.00, 0.90),
  (44, 5, 'Филиал C',         5.0,  0.05, 0.80);

INSERT INTO link (id, company_id, from_sub_id, to_sub_id, importance, delay_hours) VALUES
  (41, 5, 41, 42, 0.0, 12.0),
  (42, 5, 41, 43, 0.1, 12.0),
  (43, 5, 42, 43, 1.0, 12.0),
  (44, 5, 43, 44, 0.9, 12.0),
  (45, 5, 44, 41, 1.0, 12.0);

COMMIT;
