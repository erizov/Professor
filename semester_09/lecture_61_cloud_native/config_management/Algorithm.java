// package semester_09.lecture_61_cloud_native.config_management;

import java.util.HashMap;
import java.util.Map;
import java.util.logging.Logger;

/**
 * Config Management implementation.
 */
public class Algorithm {
    private static final Logger logger = Logger.getLogger(Algorithm.class.getName());
    
    public static Object getConfig(String key, String environment, Object defaultValue) {
        Map<String, Object> config = new HashMap<>();
        config.put("key", key);
        config.put("environment", environment);
        config.put("value", defaultValue);
        return config;
    }
    
    public static void main(String[] args) {
        logger.info("Config Management");
        logger.info("==================================================");
        
        Object config = getConfig("db_url", "production", "localhost");
        logger.info("Config: " + config);
    }
}