#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Update README files with actual framework code examples.
Uses real code samples from Spring, J2EE, .NET, Docker, Kubernetes, Kafka.
"""

import re
from pathlib import Path
from typing import Dict, List, Optional


# Real framework code examples by pattern/algorithm type
FRAMEWORK_EXAMPLES = {
    "singleton": {
        "spring": """// Spring Singleton Bean (default scope)
@Component
public class DatabaseConnection {
    @Autowired
    private DataSource dataSource;
    
    // Spring container manages singleton instance
    public Connection getConnection() {
        return dataSource.getConnection();
    }
}""",
        "j2ee": """// J2EE Singleton EJB
@Singleton
@Startup
public class CacheManager {
    private Map<String, Object> cache = new ConcurrentHashMap<>();
    
    @PostConstruct
    public void init() {
        // Initialize cache
    }
}""",
    },
    "factory": {
        "spring": """// Spring Factory Pattern
@Component
public class PaymentProcessorFactory {
    @Autowired
    private List<PaymentProcessor> processors;
    
    public PaymentProcessor getProcessor(String type) {
        return processors.stream()
            .filter(p -> p.supports(type))
            .findFirst()
            .orElseThrow();
    }
}""",
        ".net": """// .NET Factory Pattern
public class PaymentProcessorFactory {
    public IPaymentProcessor Create(string type) {
        return type switch {
            "credit" => new CreditCardProcessor(),
            "paypal" => new PayPalProcessor(),
            _ => throw new ArgumentException()
        };
    }
}""",
    },
    "observer": {
        "spring": """// Spring Event Listener (Observer Pattern)
@Component
public class OrderEventListener {
    @EventListener
    public void handleOrderCreated(OrderCreatedEvent event) {
        // Handle order creation
        sendNotification(event.getOrder());
    }
}""",
        ".net": """// .NET Event Handler (Observer Pattern)
public class OrderService {
    public event EventHandler<OrderCreatedEventArgs> OrderCreated;
    
    public void CreateOrder(Order order) {
        // Create order logic
        OrderCreated?.Invoke(this, new OrderCreatedEventArgs(order));
    }
}""",
    },
    "strategy": {
        "spring": """// Spring Strategy Pattern
public interface PaymentStrategy {
    void pay(BigDecimal amount);
}

@Component("creditCard")
public class CreditCardStrategy implements PaymentStrategy {
    public void pay(BigDecimal amount) {
        // Credit card payment logic
    }
}""",
        ".net": """// .NET Strategy Pattern
public interface IPaymentStrategy {
    void ProcessPayment(decimal amount);
}

public class CreditCardStrategy : IPaymentStrategy {
    public void ProcessPayment(decimal amount) {
        // Credit card payment logic
    }
}""",
    },
    "repository": {
        "spring": """// Spring Data Repository
public interface UserRepository extends JpaRepository<User, Long> {
    List<User> findByEmail(String email);
    
    @Query("SELECT u FROM User u WHERE u.active = true")
    List<User> findActiveUsers();
}""",
        ".net": """// .NET Repository Pattern
public interface IUserRepository {
    Task<User> GetByIdAsync(int id);
    Task<IEnumerable<User>> GetAllAsync();
    Task AddAsync(User user);
}

public class UserRepository : IUserRepository {
    private readonly DbContext _context;
    // Implementation
}""",
    },
    "adapter": {
        "spring": """// Spring Adapter Pattern
@Component
public class LegacyPaymentAdapter implements PaymentService {
    private LegacyPaymentSystem legacySystem;
    
    public void processPayment(PaymentRequest request) {
        LegacyPayment legacy = convert(request);
        legacySystem.process(legacy);
    }
}""",
    },
    "decorator": {
        "spring": """// Spring AOP Decorator
@Aspect
@Component
public class LoggingAspect {
    @Around("@annotation(Loggable)")
    public Object log(ProceedingJoinPoint joinPoint) {
        // Logging decorator logic
        return joinPoint.proceed();
    }
}""",
        ".net": """// .NET Decorator Pattern
public class LoggingDecorator : IDataService {
    private readonly IDataService _service;
    
    public async Task<string> GetDataAsync() {
        _logger.LogInformation("Getting data");
        return await _service.GetDataAsync();
    }
}""",
    },
    "facade": {
        "spring": """// Spring Facade Pattern
@Service
public class OrderFacade {
    @Autowired private PaymentService paymentService;
    @Autowired private InventoryService inventoryService;
    @Autowired private ShippingService shippingService;
    
    public void placeOrder(Order order) {
        inventoryService.reserve(order.getItems());
        paymentService.process(order.getTotal());
        shippingService.schedule(order);
    }
}""",
    },
    "proxy": {
        "spring": """// Spring Proxy Pattern
@Service
@Transactional
public class UserService {
    // Spring creates proxy for transaction management
    public User saveUser(User user) {
        return userRepository.save(user);
    }
}""",
        "j2ee": """// J2EE Proxy Pattern
@Stateless
@Remote
public class UserServiceBean implements UserService {
    // EJB container creates proxy for remote access
    public User findUser(Long id) {
        return em.find(User.class, id);
    }
}""",
    },
    "command": {
        "spring": """// Spring Command Pattern
@Component
public class CommandHandler {
    @Autowired
    private Map<String, Command> commands;
    
    public void execute(String commandType, Object data) {
        commands.get(commandType).execute(data);
    }
}""",
    },
    "template_method": {
        "spring": """// Spring Template Method
public abstract class DataProcessor {
    public final void process() {
        readData();
        processData();
        saveData();
    }
    
    protected abstract void processData();
}""",
    },
    "mvc": {
        "spring": """// Spring MVC Pattern
@RestController
@RequestMapping("/api/users")
public class UserController {
    @Autowired
    private UserService userService;
    
    @GetMapping("/{id}")
    public ResponseEntity<User> getUser(@PathVariable Long id) {
        return ResponseEntity.ok(userService.findById(id));
    }
}""",
        ".net": """// .NET MVC Pattern
[ApiController]
[Route("api/[controller]")]
public class UsersController : ControllerBase {
    [HttpGet("{id}")]
    public async Task<ActionResult<User>> GetUser(int id) {
        var user = await _userService.GetByIdAsync(id);
        return Ok(user);
    }
}""",
    },
    "dependency_injection": {
        "spring": """// Spring Dependency Injection
@Service
public class OrderService {
    private final PaymentService paymentService;
    
    @Autowired
    public OrderService(PaymentService paymentService) {
        this.paymentService = paymentService;
    }
}""",
        ".net": """// .NET Dependency Injection
public class OrderService {
    private readonly IPaymentService _paymentService;
    
    public OrderService(IPaymentService paymentService) {
        _paymentService = paymentService;
    }
}""",
    },
    "message_queue": {
        "kafka": """// Kafka Producer
@Autowired
private KafkaTemplate<String, String> kafkaTemplate;

public void sendMessage(String topic, String message) {
    kafkaTemplate.send(topic, message);
}

// Kafka Consumer
@KafkaListener(topics = "orders")
public void consume(String message) {
    // Process message
}""",
        "spring": """// Spring JMS Message Queue
@JmsListener(destination = "orders.queue")
public void receiveMessage(Order order) {
    orderService.process(order);
}""",
    },
    "publish_subscribe": {
        "kafka": """// Kafka Pub/Sub
// Publisher
kafkaTemplate.send("events", event);

// Subscriber
@KafkaListener(topics = "events", groupId = "group1")
public void handleEvent(Event event) {
    // Handle event
}""",
        "spring": """// Spring Event Pub/Sub
// Publisher
applicationEventPublisher.publishEvent(new OrderCreatedEvent(order));

// Subscriber
@EventListener
public void handleOrderCreated(OrderCreatedEvent event) {
    // Handle event
}""",
    },
    "circuit_breaker": {
        "spring": """// Spring Cloud Circuit Breaker
@CircuitBreaker(name = "payment-service", fallbackMethod = "fallback")
public PaymentResult processPayment(PaymentRequest request) {
    return paymentClient.process(request);
}

public PaymentResult fallback(PaymentRequest request, Exception e) {
    return PaymentResult.failed("Service unavailable");
}""",
    },
    "retry": {
        "spring": """// Spring Retry
@Retryable(value = {Exception.class}, maxAttempts = 3)
public void processData() {
    // Operation that may fail
}

@Recover
public void recover(Exception e) {
    // Recovery logic
}""",
    },
    "docker": {
        "docker": """# Dockerfile
FROM openjdk:11-jre-slim
COPY target/app.jar app.jar
EXPOSE 8080
ENTRYPOINT ["java", "-jar", "app.jar"]""",
    },
    "kubernetes": {
        "kubernetes": """# Kubernetes Deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app-deployment
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
      - name: app
        image: myapp:latest
        ports:
        - containerPort: 8080""",
    },
    "caching": {
        "spring": """// Spring Cache
@Cacheable(value = "users", key = "#id")
public User findUser(Long id) {
    return userRepository.findById(id);
}

@CacheEvict(value = "users", key = "#id")
public void deleteUser(Long id) {
    userRepository.deleteById(id);
}""",
    },
    "authentication": {
        "spring": """// Spring Security Authentication
@Configuration
public class SecurityConfig {
    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) {
        http.authorizeHttpRequests(auth -> auth
            .requestMatchers("/public/**").permitAll()
            .anyRequest().authenticated()
        );
        return http.build();
    }
}""",
    },
    "jwt": {
        "spring": """// Spring JWT
@Component
public class JwtTokenProvider {
    public String generateToken(UserDetails userDetails) {
        return Jwts.builder()
            .setSubject(userDetails.getUsername())
            .setExpiration(new Date(System.currentTimeMillis() + 86400000))
            .signWith(SignatureAlgorithm.HS512, secret)
            .compact();
    }
}""",
    },
}


def get_algorithm_type(algorithm_name: str, lecture_path: str) -> str:
    """Determine algorithm type for framework examples."""
    name_lower = algorithm_name.lower()
    lecture_lower = lecture_path.lower()
    
    # Pattern matching
    if "singleton" in name_lower:
        return "singleton"
    elif "factory" in name_lower:
        return "factory"
    elif "observer" in name_lower or "pub_sub" in name_lower:
        return "observer" if "observer" in name_lower else "publish_subscribe"
    elif "strategy" in name_lower:
        return "strategy"
    elif "repository" in lecture_lower:
        return "repository"
    elif "adapter" in name_lower:
        return "adapter"
    elif "decorator" in name_lower:
        return "decorator"
    elif "facade" in name_lower:
        return "facade"
    elif "proxy" in name_lower:
        return "proxy"
    elif "command" in name_lower:
        return "command"
    elif "template" in name_lower:
        return "template_method"
    elif "mvc" in name_lower or "mvvm" in name_lower:
        return "mvc"
    elif "dependency" in name_lower or "inversion" in name_lower:
        return "dependency_injection"
    elif "message_queue" in name_lower or "queue" in name_lower:
        return "message_queue"
    elif "circuit" in name_lower:
        return "circuit_breaker"
    elif "retry" in name_lower:
        return "retry"
    elif "cache" in name_lower:
        return "caching"
    elif "auth" in name_lower:
        return "authentication"
    elif "jwt" in name_lower:
        return "jwt"
    elif "docker" in lecture_lower or "container" in lecture_lower:
        return "docker"
    elif "kubernetes" in lecture_lower or "k8s" in lecture_lower:
        return "kubernetes"
    
    return None


def generate_framework_examples_section(algorithm_name: str, lecture_path: str) -> str:
    """Generate framework examples section with real code."""
    alg_type = get_algorithm_type(algorithm_name, lecture_path)
    
    if not alg_type or alg_type not in FRAMEWORK_EXAMPLES:
        return """## Examples of Implementation

This algorithm/pattern is implemented in various frameworks and technologies.

*Note: Framework-specific examples will be added based on actual implementations.*
"""
    
    examples = FRAMEWORK_EXAMPLES[alg_type]
    section = "## Examples of Implementation\n\n"
    section += "This algorithm/pattern is implemented in the following frameworks:\n\n"
    
    if "spring" in examples:
        section += "### Spring Framework\n\n"
        section += "```java\n"
        section += examples["spring"]
        section += "\n```\n\n"
    
    if "j2ee" in examples:
        section += "### J2EE (Java Enterprise Edition)\n\n"
        section += "```java\n"
        section += examples["j2ee"]
        section += "\n```\n\n"
    
    if ".net" in examples:
        section += "### .NET Framework\n\n"
        section += "```csharp\n"
        section += examples[".net"]
        section += "\n```\n\n"
    
    if "kafka" in examples:
        section += "### Apache Kafka\n\n"
        section += "```java\n"
        section += examples["kafka"]
        section += "\n```\n\n"
    
    if "docker" in examples:
        section += "### Docker\n\n"
        section += "```dockerfile\n"
        section += examples["docker"]
        section += "\n```\n\n"
    
    if "kubernetes" in examples:
        section += "### Kubernetes\n\n"
        section += "```yaml\n"
        section += examples["kubernetes"]
        section += "\n```\n\n"
    
    return section


def update_readme(readme_path: Path, algorithm_name: str, lecture_path: str) -> None:
    """Update README with real framework examples."""
    try:
        with open(readme_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find and replace "Examples of Implementation" section
        pattern = r'## Examples of Implementation.*?(?=\n## |\Z)'
        
        new_section = generate_framework_examples_section(algorithm_name, lecture_path)
        
        if re.search(pattern, content, re.DOTALL):
            content = re.sub(pattern, new_section.rstrip(), content, flags=re.DOTALL)
        else:
            # Append if not found
            content += "\n\n" + new_section
        
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"Updated: {readme_path}")
    
    except Exception as e:
        print(f"Error updating {readme_path}: {e}")


def main():
    """Main function."""
    base_path = Path(__file__).resolve().parents[1]
    
    # Find all README files
    readme_files = list(base_path.rglob("README.md"))
    
    # Filter to algorithm READMEs (in algorithm directories)
    algorithm_readmes = []
    for readme in readme_files:
        parent = readme.parent
        if (parent / "algorithm.py").exists() or (parent / "Algorithm.java").exists():
            algorithm_readmes.append(readme)
    
    print(f"Found {len(algorithm_readmes)} algorithm README files")
    print("Updating with real framework examples...\n")
    
    for readme in algorithm_readmes:
        algorithm_name = readme.parent.name
        lecture_path = str(readme.parent.parent)
        
        update_readme(readme, algorithm_name, lecture_path)
    
    print(f"\nUpdated {len(algorithm_readmes)} README files")


if __name__ == "__main__":
    main()

