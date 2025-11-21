package semester_08.lecture_50_sql_advanced.partitioning;

import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.logging.Logger;

/**
 * Partitioning implementation.
 */
public class Algorithm {
    private static final Logger logger = Logger.getLogger(Algorithm.class.getName());

    public Algorithm() {
        // Initialize
    }

    /**
     * Partition data by range.
     */
    public Map<String, List<Integer>> partition_by_range(List<Integer> data, List<Integer> ranges) {
        logger.info("Executing partition_by_range");
        Map<String, List<Integer>> buckets = new LinkedHashMap<>();
        if (data == null) {
            return buckets;
        }

        if (ranges == null || ranges.isEmpty()) {
            buckets.put("all", new ArrayList<>(data));
            return buckets;
        }

        for (int i = 0; i < ranges.size(); i++) {
            buckets.put("range_" + (i + 1), new ArrayList<>());
        }
        buckets.put("overflow", new ArrayList<>());

        for (Integer value : data) {
            boolean placed = false;
            for (int i = 0; i < ranges.size(); i++) {
                if (value <= ranges.get(i)) {
                    buckets.get("range_" + (i + 1)).add(value);
                    placed = true;
                    break;
                }
            }
            if (!placed) {
                buckets.get("overflow").add(value);
            }
        }
        return buckets;
    }

    /**
     * Partition data by hash.
     */
    public Map<Integer, List<Integer>> partition_by_hash(List<Integer> data, int numPartitions) {
        logger.info("Executing partition_by_hash");
        Map<Integer, List<Integer>> buckets = new LinkedHashMap<>();
        if (numPartitions <= 0) {
            return buckets;
        }
        for (int i = 0; i < numPartitions; i++) {
            buckets.put(i, new ArrayList<>());
        }

        if (data == null) {
            return buckets;
        }

        for (Integer value : data) {
            int bucketIndex = Math.floorMod(value.hashCode(), numPartitions);
            buckets.get(bucketIndex).add(value);
        }
        return buckets;
    }

    public static Algorithm create() {
        return new Algorithm();
    }

    public static void main(String[] args) {
        System.out.println("=".repeat(70));
        System.out.println("Partitioning");
        System.out.println("=".repeat(70));
        
        Algorithm algo = Algorithm.create();
        List<Integer> sampleData = List.of(5, 12, 27, 31, 45, 51);
        Map<String, List<Integer>> rangePartitions = algo.partition_by_range(sampleData, List.of(20, 40));
        System.out.println("Range partitions: " + rangePartitions);
        Map<Integer, List<Integer>> hashPartitions = algo.partition_by_hash(sampleData, 3);
        System.out.println("Hash partitions: " + hashPartitions);
        System.out.println("=".repeat(70));
    }
}
