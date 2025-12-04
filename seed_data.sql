INSERT INTO company (name) VALUES ('ООО "Распределённая Компания"');

INSERT INTO subdivision (company_id, name, resources, kpi, state)
VALUES
(1, 'Центральный офис',  100.0, 90.0, 0.2),
(1, 'Филиал A',          50.0,  70.0, 0.5),
(1, 'Филиал B',          40.0,  60.0, 0.7);

INSERT INTO link (company_id, from_sub_id, to_sub_id, importance, delay_hours)
VALUES
(1, 1, 2, 5.0, 2.0),   -- Центр -> Филиал A
(1, 1, 3, 4.0, 1.0),   -- Центр -> Филиал B
(1, 2, 3, 3.0, 3.0),   -- A -> B
(1, 2, 1, 2.0, 4.0),   -- A -> Центр
(1, 3, 1, 2.0, 2.0);   -- B -> Центр
