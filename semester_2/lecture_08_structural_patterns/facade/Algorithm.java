/**
 * Facade Design Pattern.
 * 
 * Provides unified interface to subsystem.
 */
public class Algorithm {
    
    static class CPU {
        void freeze() { System.out.println("CPU: Freezing..."); }
        void jump(int pos) { System.out.println("CPU: Jumping to " + pos); }
        void execute() { System.out.println("CPU: Executing..."); }
    }
    
    static class Memory {
        void load(int pos, String data) {
            System.out.println("Memory: Loading '" + data + "' at " + pos);
        }
    }
    
    static class HardDrive {
        String read(int lba, int size) {
            System.out.println("HardDrive: Reading " + size + " bytes from LBA " + lba);
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
            System.out.println("Starting computer...");
            cpu.freeze();
            String bootData = hardDrive.read(0, 512);
            memory.load(BOOT_ADDRESS, bootData);
            cpu.jump(BOOT_ADDRESS);
            cpu.execute();
            System.out.println("Computer started!");
        }
    }
    
    public static void main(String[] args) {
        System.out.println("=".repeat(70));
        System.out.println("FACADE DESIGN PATTERN");
        System.out.println("=".repeat(70));
        System.out.println();
        
        ComputerFacade computer = new ComputerFacade();
        computer.start();
        System.out.println();
        
        System.out.println("=".repeat(70));
        System.out.println("\nPattern: Provides unified interface to subsystem");
        System.out.println("=".repeat(70));
    }
}
