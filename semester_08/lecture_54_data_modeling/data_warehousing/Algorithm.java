package semester_08.lecture_54_data_modeling.data_warehousing;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.logging.Logger;

/**
 * Data Warehousing implementation.
 */
public class Algorithm {
    private static final Logger logger = Logger.getLogger(Algorithm.class.getName());
    private final Map<String, Map<String, Table>> warehouse = new HashMap<>();

    public Algorithm() {
        // Initialize
    }

    /**
     * Create schema.
     */
    public Map<String, Table> create_schema(String schemaName) {
        logger.info("Executing create_schema");
        return warehouse.computeIfAbsent(schemaName, key -> new HashMap<>());
    }

    /**
     * Create table.
     */
    public Table create_table(String schemaName, String tableName, List<String> columns) {
        logger.info("Executing create_table");
        Map<String, Table> schema = create_schema(schemaName);
        Table table = new Table(columns);
        schema.put(tableName, table);
        return table;
    }

    /**
     * Insert row.
     */
    public void insert(String schemaName, String tableName, Map<String, Object> row) {
        logger.info("Executing insert");
        Table table = getTable(schemaName, tableName);
        table.rows.add(new HashMap<>(row));
    }

    /**
     * Query table.
     */
    public List<Map<String, Object>> query(String schemaName, String tableName) {
        logger.info("Executing query");
        Table table = getTable(schemaName, tableName);
        return new ArrayList<>(table.rows);
    }

    private Table getTable(String schemaName, String tableName) {
        Map<String, Table> schema = warehouse.get(schemaName);
        if (schema == null || !schema.containsKey(tableName)) {
            throw new IllegalStateException("Table not found: " + schemaName + "." + tableName);
        }
        return schema.get(tableName);
    }

    public static Algorithm create() {
        return new Algorithm();
    }

    public static void main(String[] args) {
        System.out.println("=".repeat(70));
        System.out.println("Data Warehousing");
        System.out.println("=".repeat(70));
        
        Algorithm algo = Algorithm.create();
        algo.create_table("sales", "orders", List.of("id", "amount"));
        Map<String, Object> row = new HashMap<>();
        row.put("id", 1);
        row.put("amount", 199.0);
        algo.insert("sales", "orders", row);
        System.out.println("Orders: " + algo.query("sales", "orders"));
        System.out.println("=".repeat(70));
    }

    private static class Table {
        private final List<String> columns;
        private final List<Map<String, Object>> rows = new ArrayList<>();

        Table(List<String> columns) {
            this.columns = new ArrayList<>(columns);
        }
    }
}
