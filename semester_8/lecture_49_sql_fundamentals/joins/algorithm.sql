-- Joins for sql database fundamentals
-- SQL Implementation

-- Example: Joins

-- INNER JOIN
SELECT t1.*, t2.*
FROM table1 t1
INNER JOIN table2 t2 ON t1.id = t2.foreign_id;

-- LEFT JOIN
SELECT t1.*, t2.*
FROM table1 t1
LEFT JOIN table2 t2 ON t1.id = t2.foreign_id;

-- RIGHT JOIN
SELECT t1.*, t2.*
FROM table1 t1
RIGHT JOIN table2 t2 ON t1.id = t2.foreign_id;

-- FULL OUTER JOIN
SELECT t1.*, t2.*
FROM table1 t1
FULL OUTER JOIN table2 t2 ON t1.id = t2.foreign_id;

-- CROSS JOIN
SELECT t1.*, t2.*
FROM table1 t1
CROSS JOIN table2 t2;
