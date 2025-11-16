/**
 * Interface Segregation Principle (ISP) implementation.
 * 
 * Clients should not be forced to depend on interfaces they do not use.
 * Many client-specific interfaces are better than one general-purpose interface.
 */
interface Workable {
    void work();
}

interface Eatable {
    void eat();
}

interface Sleepable {
    void sleep();
}

import java.util.logging.Logger;
class HumanWorker implements Workable, Eatable, Sleepable {
    public void work() {
        logger.info("Human working...");
    }
    
    public void eat() {
        logger.info("Human eating...");
    }
    
    public void sleep() {
        logger.info("Human sleeping...");
    }
}

class RobotWorker implements Workable {
    public void work() {
        logger.info("Robot working...");
    }
}

public class Algorithm {
    private static final Logger logger = Logger.getLogger(Algorithm.class.getName());

    public static void main(String[] args) {
        logger.info("=".repeat(70));
        logger.info("INTERFACE SEGREGATION PRINCIPLE DEMONSTRATION");
        logger.info("=".repeat(70));
        logger.info();
        
        // Example 1: Human Worker
        logger.info("Example 1: Human Worker");
        logger.info("-".repeat(70));
        HumanWorker human = new HumanWorker();
        human.work();
        human.eat();
        human.sleep();
        logger.info();
        
        // Example 2: Robot Worker
        logger.info("Example 2: Robot Worker");
        logger.info("-".repeat(70));
        RobotWorker robot = new RobotWorker();
        robot.work();
        logger.info();
        
        logger.info("=".repeat(70));
        logger.info("\nPrinciple Summary:");
        logger.info("\nIntent:");
        logger.info("  Clients should not be forced to depend on");
        logger.info("  interfaces they do not use.");
        logger.info("\nKey Benefits:");
        logger.info("  - No unused method implementations");
        logger.info("  - Better cohesion");
        logger.info("  - Easier to maintain");
        logger.info("  - Clearer interfaces");
        logger.info("=".repeat(70));
    }
}