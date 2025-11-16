-- Index Strategies
-- SQL Implementation

-- Example: Index Strategies

-- Create Index
CREATE INDEX idx_column_name ON table_name(column_name);

-- Create Unique Index
CREATE UNIQUE INDEX idx_unique_column ON table_name(column_name);

-- Create Composite Index
CREATE INDEX idx_composite ON table_name(column1, column2);

-- Drop Index
DROP INDEX idx_column_name;
