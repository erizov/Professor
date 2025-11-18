-- Distributed Transactions
-- SQL Implementation

-- Example: Distributed Transactions

-- Transaction Example
BEGIN TRANSACTION;

UPDATE accounts SET balance = balance - 100 WHERE id = 1;
UPDATE accounts SET balance = balance + 100 WHERE id = 2;

COMMIT;
-- Or ROLLBACK; on error
