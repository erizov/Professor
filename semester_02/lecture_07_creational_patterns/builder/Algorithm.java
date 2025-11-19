import java.util.*;

/**
 * Builder Design Pattern.
 * 
 * Constructs complex objects step by step.
 */
import java.util.logging.Logger;
public class Algorithm {
    private static final Logger logger = Logger.getLogger(Algorithm.class.getName());

    
    // Product
    static class Computer {
        private String cpu;
        private String ram;
        private String storage;
        private String gpu;
        private String motherboard;
        private String powerSupply;
        
        public String toString() {
            List<String> parts = new ArrayList<>();
            if (cpu != null) parts.add("CPU: " + cpu);
            if (ram != null) parts.add("RAM: " + ram);
            if (storage != null) parts.add("Storage: " + storage);
            if (gpu != null) parts.add("GPU: " + gpu);
            if (motherboard != null) parts.add("Motherboard: " + motherboard);
            if (powerSupply != null) parts.add("Power Supply: " + powerSupply);
            return "Computer(" + String.join(", ", parts) + ")";
        }
        
        // Setters
        void setCpu(String cpu) { this.cpu = cpu; }
        void setRam(String ram) { this.ram = ram; }
        void setStorage(String storage) { this.storage = storage; }
        void setGpu(String gpu) { this.gpu = gpu; }
        void setMotherboard(String motherboard) { this.motherboard = motherboard; }
        void setPowerSupply(String powerSupply) { this.powerSupply = powerSupply; }
    }
    
    // Builder Interface
    abstract static class ComputerBuilder {
        protected Computer computer;
        
        ComputerBuilder() {
            this.computer = new Computer();
        }
        
        abstract ComputerBuilder buildCpu(String cpu);
        abstract ComputerBuilder buildRam(String ram);
        abstract ComputerBuilder buildStorage(String storage);
        abstract ComputerBuilder buildGpu(String gpu);
        
        ComputerBuilder buildMotherboard(String motherboard) {
            computer.setMotherboard(motherboard);
            return this;
        }
        
        ComputerBuilder buildPowerSupply(String powerSupply) {
            computer.setPowerSupply(powerSupply);
            return this;
        }
        
        Computer getComputer() {
            return computer;
        }
    }
    
    // Concrete Builders
    static class GamingComputerBuilder extends ComputerBuilder {
        public ComputerBuilder buildCpu(String cpu) {
            computer.setCpu(cpu != null ? cpu : "Intel i9-13900K");
            return this;
        }
        
        public ComputerBuilder buildRam(String ram) {
            computer.setRam(ram != null ? ram : "32GB DDR5");
            return this;
        }
        
        public ComputerBuilder buildStorage(String storage) {
            computer.setStorage(storage != null ? storage : "2TB NVMe SSD");
            return this;
        }
        
        public ComputerBuilder buildGpu(String gpu) {
            computer.setGpu(gpu != null ? gpu : "NVIDIA RTX 4090");
            return this;
        }
    }
    
    static class OfficeComputerBuilder extends ComputerBuilder {
        public ComputerBuilder buildCpu(String cpu) {
            computer.setCpu(cpu != null ? cpu : "Intel i5-13400");
            return this;
        }
        
        public ComputerBuilder buildRam(String ram) {
            computer.setRam(ram != null ? ram : "16GB DDR4");
            return this;
        }
        
        public ComputerBuilder buildStorage(String storage) {
            computer.setStorage(storage != null ? storage : "512GB SSD");
            return this;
        }
        
        public ComputerBuilder buildGpu(String gpu) {
            computer.setGpu(gpu != null ? gpu : "Integrated Graphics");
            return this;
        }
    }
    
    // Director
    static class ComputerDirector {
        private ComputerBuilder builder;
        
        ComputerDirector(ComputerBuilder builder) {
            this.builder = builder;
        }
        
        Computer buildGamingPc() {
            return builder
                .buildCpu("Intel i9-13900K")
                .buildRam("32GB DDR5")
                .buildStorage("2TB NVMe SSD")
                .buildGpu("NVIDIA RTX 4090")
                .buildMotherboard("ASUS ROG Strix Z790")
                .buildPowerSupply("1000W 80+ Gold")
                .getComputer();
        }
        
        Computer buildOfficePc() {
            return builder
                .buildCpu("Intel i5-13400")
                .buildRam("16GB DDR4")
                .buildStorage("512GB SSD")
                .buildGpu("Integrated Graphics")
                .buildMotherboard("ASUS Prime B760")
                .buildPowerSupply("500W 80+ Bronze")
                .getComputer();
        }
    }
    
    // Fluent Builder Example: Pizza
    static class Pizza {
        private String size;
        private String crust;
        private boolean cheese;
        private boolean pepperoni;
        private boolean bacon;
        private boolean mushrooms;
        private boolean onions;
        private boolean peppers;
        
        public String toString() {
            List<String> toppings = new ArrayList<>();
            if (cheese) toppings.add("cheese");
            if (pepperoni) toppings.add("pepperoni");
            if (bacon) toppings.add("bacon");
            if (mushrooms) toppings.add("mushrooms");
            if (onions) toppings.add("onions");
            if (peppers) toppings.add("peppers");
            
            return String.format("Pizza(size=%s, crust=%s, toppings=[%s])",
                               size, crust, String.join(", ", toppings));
        }
        
        // Setters
        void setSize(String size) { this.size = size; }
        void setCrust(String crust) { this.crust = crust; }
        void setCheese(boolean cheese) { this.cheese = cheese; }
        void setPepperoni(boolean pepperoni) { this.pepperoni = pepperoni; }
        void setBacon(boolean bacon) { this.bacon = bacon; }
        void setMushrooms(boolean mushrooms) { this.mushrooms = mushrooms; }
        void setOnions(boolean onions) { this.onions = onions; }
        void setPeppers(boolean peppers) { this.peppers = peppers; }
    }
    
    static class PizzaBuilder {
        private Pizza pizza;
        
        PizzaBuilder() {
            this.pizza = new Pizza();
        }
        
        PizzaBuilder size(String size) {
            pizza.setSize(size);
            return this;
        }
        
        PizzaBuilder crust(String crust) {
            pizza.setCrust(crust);
            return this;
        }
        
        PizzaBuilder addCheese() {
            pizza.setCheese(true);
            return this;
        }
        
        PizzaBuilder addPepperoni() {
            pizza.setPepperoni(true);
            return this;
        }
        
        PizzaBuilder addBacon() {
            pizza.setBacon(true);
            return this;
        }
        
        PizzaBuilder addMushrooms() {
            pizza.setMushrooms(true);
            return this;
        }
        
        PizzaBuilder addOnions() {
            pizza.setOnions(true);
            return this;
        }
        
        PizzaBuilder addPeppers() {
            pizza.setPeppers(true);
            return this;
        }
        
        Pizza build() {
            return pizza;
        }
    }
    
    public static void main(String[] args) {
        String separator = "=".repeat(70);
        String dash = "-".repeat(70);
        long startTime = System.nanoTime();
        
        logger.info(separator);
        logger.info("BUILDER DESIGN PATTERN DEMONSTRATION");
        logger.info(separator);
        logger.info("");
        
        // Example 1: Computer Builder
        logger.info("Example 1: Computer Builder");
        logger.info(dash);
        
        GamingComputerBuilder gamingBuilder = new GamingComputerBuilder();
        Computer gamingPc = gamingBuilder
            .buildCpu("Intel i9-13900K")
            .buildRam("32GB DDR5")
            .buildStorage("2TB NVMe SSD")
            .buildGpu("NVIDIA RTX 4090")
            .buildMotherboard("ASUS ROG Strix Z790")
            .getComputer();
        
        logger.info("Gaming PC: " + gamingPc);
        
        OfficeComputerBuilder officeBuilder = new OfficeComputerBuilder();
        Computer officePc = officeBuilder
            .buildCpu("Intel i5-13400")
            .buildRam("16GB DDR4")
            .buildStorage("512GB SSD")
            .buildGpu("Integrated Graphics")
            .getComputer();
        
        logger.info("Office PC: " + officePc);
        logger.info("");
        
        // Example 2: Using Director
        logger.info("Example 2: Using Director");
        logger.info(dash);
        
        ComputerDirector director = new ComputerDirector(new GamingComputerBuilder());
        Computer pc1 = director.buildGamingPc();
        logger.info("Director-built Gaming PC: " + pc1);
        logger.info("");
        
        // Example 3: Fluent Pizza Builder
        logger.info("Example 3: Fluent Pizza Builder");
        logger.info(dash);
        
        Pizza pizza1 = new PizzaBuilder()
            .size("Large")
            .crust("Thin")
            .addCheese()
            .addPepperoni()
            .addMushrooms()
            .build();
        
        logger.info("Pizza 1: " + pizza1);
        
        Pizza pizza2 = new PizzaBuilder()
            .size("Medium")
            .crust("Thick")
            .addCheese()
            .addBacon()
            .addOnions()
            .addPeppers()
            .build();
        
        logger.info("Pizza 2: " + pizza2);
        logger.info("");
        
        long endTime = System.nanoTime();
        
        logger.info(separator);
        logger.info("\nPattern Summary:");
        logger.info("\nKey Advantages:");
        logger.info("  - Step-by-step construction");
        logger.info("  - Reusable construction code");
        logger.info("  - Fluent interface");
        logger.info("\nWhen to Use:");
        logger.info("  - Complex object construction");
        logger.info("  - Many optional parameters");
        logger.info(separator);
        System.out.printf("\nTotal time: %.3f ms%n",
                        (endTime - startTime) / 1_000_000.0);
    }
}