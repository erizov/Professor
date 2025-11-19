/**
 * Facade Design Pattern.
 * 
 * Provides unified interface to subsystem.
 */
import java.util.logging.Logger;
public class Algorithm {
    private static final Logger logger = Logger.getLogger(Algorithm.class.getName());

    
    static class CPU {
        void freeze() { logger.info("CPU: Freezing..."); }
        void jump(int pos) { logger.info("CPU: Jumping to " + pos); }
        void execute() { logger.info("CPU: Executing..."); }
    }
    
    static class Memory {
        void load(int pos, String data) {
            logger.info("Memory: Loading '" + data + "' at " + pos);
        }
    }
    
    static class HardDrive {
        String read(int lba, int size) {
            logger.info("HardDrive: Reading " + size + " bytes from LBA " + lba);
            return "Data from LBA " + lba;
        }
    }
    
    static class ComputerFacade {
        private CPU cpu;
        private Memory memory;
        private HardDrive hardDrive;
        private int BOOT_ADDRESS = 0x7C00;
        
        ComputerFacade() {
            cpu = new CPU();
            memory = new Memory();
            hardDrive = new HardDrive();
        }
        
        void start() {
            logger.info("Starting computer...");
            cpu.freeze();
            String bootData = hardDrive.read(0, 512);
            memory.load(BOOT_ADDRESS, bootData);
            cpu.jump(BOOT_ADDRESS);
            cpu.execute();
            logger.info("Computer started!");
        }
    }
    
    public static void main(String[] args) {
        String separator = "=".repeat(70);
        String dash = "-".repeat(70);
        logger.info(separator);
        logger.info("FACADE DESIGN PATTERN");
        logger.info(separator);
        logger.info("");
        
        ComputerFacade computer = new ComputerFacade();
        computer.start();
        logger.info("");
        
        logger.info(separator);
        logger.info("\nPattern: Provides unified interface to subsystem");
        logger.info(separator);
    }
}