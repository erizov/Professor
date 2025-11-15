import java.util.*;

/**
 * Command Design Pattern.
 * 
 * Encapsulates requests as objects.
 */
public class Algorithm {
    
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
            System.out.println(location + " light is ON");
        }
        
        void off() {
            isOn = false;
            System.out.println(location + " light is OFF");
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
        System.out.println("=".repeat(70));
        System.out.println("COMMAND DESIGN PATTERN");
        System.out.println("=".repeat(70));
        System.out.println();
        
        Light light = new Light("Living Room");
        Command onCommand = new LightOnCommand(light);
        Command offCommand = new LightOffCommand(light);
        
        onCommand.execute();
        offCommand.execute();
        onCommand.undo();
        System.out.println();
        
        System.out.println("=".repeat(70));
        System.out.println("\nPattern: Encapsulates requests as objects");
        System.out.println("=".repeat(70));
    }
}
