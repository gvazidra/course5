CREATE TABLE company (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    name        TEXT NOT NULL
);

CREATE TABLE subdivision (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id  INTEGER NOT NULL,
    name        TEXT NOT NULL,
    resources   REAL NOT NULL,   -- R_i
    kpi         REAL NOT NULL,   -- KPI
    state       REAL NOT NULL,   -- S_i
    FOREIGN KEY (company_id) REFERENCES company(id)
);

CREATE TABLE link (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id      INTEGER NOT NULL,
    from_sub_id     INTEGER NOT NULL,
    to_sub_id       INTEGER NOT NULL,
    importance      REAL NOT NULL,  -- W_ij
    delay_hours     REAL NOT NULL,  -- Δt_ij в часах
    FOREIGN KEY (company_id) REFERENCES company(id),
    FOREIGN KEY (from_sub_id) REFERENCES subdivision(id),
    FOREIGN KEY (to_sub_id) REFERENCES subdivision(id)
);
