-- Algorithm Course Database Schema
-- Tracks algorithms, their metadata, usage, tests, performance, and framework usage

CREATE TABLE IF NOT EXISTS algorithms (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    display_name TEXT NOT NULL,
    folder_path TEXT NOT NULL,
    semester_number INTEGER,
    lecture_name TEXT,
    category TEXT,
    description TEXT,
    short_description TEXT,
    time_complexity TEXT,
    space_complexity TEXT,
    stability TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS algorithm_files (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    algorithm_id INTEGER NOT NULL,
    file_type TEXT NOT NULL,  -- 'python', 'java', 'sql', 'readme', 'test'
    file_path TEXT NOT NULL,
    file_name TEXT NOT NULL,
    file_size INTEGER,
    last_modified TIMESTAMP,
    FOREIGN KEY (algorithm_id) REFERENCES algorithms(id) ON DELETE CASCADE,
    UNIQUE(algorithm_id, file_type)
);

CREATE TABLE IF NOT EXISTS test_files (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    algorithm_id INTEGER NOT NULL,
    test_file_path TEXT NOT NULL,
    test_count INTEGER DEFAULT 0,
    coverage_percentage REAL DEFAULT 0.0,
    last_run TIMESTAMP,
    status TEXT,  -- 'passing', 'failing', 'not_run'
    FOREIGN KEY (algorithm_id) REFERENCES algorithms(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS performance_metrics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    algorithm_id INTEGER NOT NULL,
    input_size INTEGER NOT NULL,
    execution_time_ms REAL,
    memory_usage_mb REAL,
    operations_per_sec REAL,
    language TEXT,  -- 'python', 'java', 'sql'
    test_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (algorithm_id) REFERENCES algorithms(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS framework_usage (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    algorithm_id INTEGER NOT NULL,
    framework_name TEXT NOT NULL,  -- 'Spring', '.NET', 'Docker', 'Kubernetes', etc.
    framework_type TEXT,  -- 'java', 'csharp', 'yaml', 'python'
    example_code TEXT,
    purpose TEXT,
    FOREIGN KEY (algorithm_id) REFERENCES algorithms(id) ON DELETE CASCADE,
    UNIQUE(algorithm_id, framework_name)
);

CREATE TABLE IF NOT EXISTS algorithm_usage (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    algorithm_id INTEGER NOT NULL,
    usage_count INTEGER DEFAULT 0,
    last_used TIMESTAMP,
    usage_context TEXT,  -- 'educational', 'production', 'research'
    FOREIGN KEY (algorithm_id) REFERENCES algorithms(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS algorithm_advantages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    algorithm_id INTEGER NOT NULL,
    advantage TEXT NOT NULL,
    FOREIGN KEY (algorithm_id) REFERENCES algorithms(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS algorithm_shortcomings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    algorithm_id INTEGER NOT NULL,
    shortcoming TEXT NOT NULL,
    FOREIGN KEY (algorithm_id) REFERENCES algorithms(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS related_algorithms (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    algorithm_id INTEGER NOT NULL,
    related_algorithm_id INTEGER NOT NULL,
    relationship_type TEXT,  -- 'often_used_with', 'do_not_confuse_with', 'alternative'
    FOREIGN KEY (algorithm_id) REFERENCES algorithms(id) ON DELETE CASCADE,
    FOREIGN KEY (related_algorithm_id) REFERENCES algorithms(id) ON DELETE CASCADE,
    UNIQUE(algorithm_id, related_algorithm_id, relationship_type)
);

CREATE TABLE IF NOT EXISTS learning_objectives (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    algorithm_id INTEGER NOT NULL,
    objective_text TEXT NOT NULL,
    objective_order INTEGER,
    FOREIGN KEY (algorithm_id) REFERENCES algorithms(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS prerequisites (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    algorithm_id INTEGER NOT NULL,
    prerequisite_text TEXT NOT NULL,
    FOREIGN KEY (algorithm_id) REFERENCES algorithms(id) ON DELETE CASCADE
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_algorithms_name ON algorithms(name);
CREATE INDEX IF NOT EXISTS idx_algorithms_semester ON algorithms(semester_number);
CREATE INDEX IF NOT EXISTS idx_algorithms_category ON algorithms(category);
CREATE INDEX IF NOT EXISTS idx_files_algorithm ON algorithm_files(algorithm_id);
CREATE INDEX IF NOT EXISTS idx_tests_algorithm ON test_files(algorithm_id);
CREATE INDEX IF NOT EXISTS idx_performance_algorithm ON performance_metrics(algorithm_id);
CREATE INDEX IF NOT EXISTS idx_framework_algorithm ON framework_usage(algorithm_id);

-- Views for common queries
CREATE VIEW IF NOT EXISTS algorithm_summary AS
SELECT 
    a.id,
    a.name,
    a.display_name,
    a.semester_number,
    a.lecture_name,
    a.category,
    a.time_complexity,
    a.space_complexity,
    COUNT(DISTINCT af.id) as file_count,
    COUNT(DISTINCT tf.id) as test_count,
    COUNT(DISTINCT fw.id) as framework_count,
    MAX(pm.test_date) as last_performance_test
FROM algorithms a
LEFT JOIN algorithm_files af ON a.id = af.algorithm_id
LEFT JOIN test_files tf ON a.id = tf.algorithm_id
LEFT JOIN framework_usage fw ON a.id = fw.algorithm_id
LEFT JOIN performance_metrics pm ON a.id = pm.algorithm_id
GROUP BY a.id;

CREATE VIEW IF NOT EXISTS algorithm_statistics AS
SELECT 
    COUNT(DISTINCT a.id) as total_algorithms,
    COUNT(DISTINCT a.semester_number) as total_semesters,
    COUNT(DISTINCT a.category) as total_categories,
    COUNT(DISTINCT af.id) FILTER (WHERE af.file_type = 'python') as python_files,
    COUNT(DISTINCT af.id) FILTER (WHERE af.file_type = 'java') as java_files,
    COUNT(DISTINCT af.id) FILTER (WHERE af.file_type = 'sql') as sql_files,
    COUNT(DISTINCT tf.id) as total_tests,
    COUNT(DISTINCT fw.id) as total_framework_examples
FROM algorithms a
LEFT JOIN algorithm_files af ON a.id = af.algorithm_id
LEFT JOIN test_files tf ON a.id = tf.algorithm_id
LEFT JOIN framework_usage fw ON a.id = fw.algorithm_id;

