import java.util.*;

/**
 * Command Design Pattern.
 * 
 * Encapsulates requests as objects.
 */
import java.util.logging.Logger;
public class Algorithm {
    private static final Logger logger = Logger.getLogger(Algorithm.class.getName());

    
    interface Command {
        void execute();
        void undo();
    }
    
    static class Light {
        private String location;
        private boolean isOn;
        
        Light(String location) {
            this.location = location;
            this.isOn = false;
        }
        
        void on() {
            isOn = true;
            logger.info(location + " light is ON");
        }
        
        void off() {
            isOn = false;
            logger.info(location + " light is OFF");
        }
    }
    
    static class LightOnCommand implements Command {
        private Light light;
        
        LightOnCommand(Light light) {
            this.light = light;
        }
        
        public void execute() {
            light.on();
        }
        
        public void undo() {
            light.off();
        }
    }
    
    static class LightOffCommand implements Command {
        private Light light;
        
        LightOffCommand(Light light) {
            this.light = light;
        }
        
        public void execute() {
            light.off();
        }
        
        public void undo() {
            light.on();
        }
    }
    
    public static void main(String[] args) {
        logger.info("=".repeat(70));
        logger.info("COMMAND DESIGN PATTERN");
        logger.info("=".repeat(70));
        logger.info();
        
        Light light = new Light("Living Room");
        Command onCommand = new LightOnCommand(light);
        Command offCommand = new LightOffCommand(light);
        
        onCommand.execute();
        offCommand.execute();
        onCommand.undo();
        logger.info();
        
        logger.info("=".repeat(70));
        logger.info("\nPattern: Encapsulates requests as objects");
        logger.info("=".repeat(70));
    }
}