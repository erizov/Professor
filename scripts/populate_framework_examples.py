#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Populate "Examples of Implementation" sections in README files with specific,
real-world framework examples from Spring, J2EE, .NET, Docker, Kubernetes, Kafka.

Usage:
    python scripts/populate_framework_examples.py
"""

import re
from pathlib import Path
from typing import Dict, Optional, List, Tuple

ROOT = Path(__file__).resolve().parents[1]

# Comprehensive mapping of algorithms to framework implementations
FRAMEWORK_EXAMPLES: Dict[str, Dict[str, str]] = {
    # Sorting Algorithms
    "quick_sort": {
        "spring": """// Spring Data JPA - Sorting query results
public interface UserRepository extends JpaRepository<User, Long> {
    @Query("SELECT u FROM User u ORDER BY u.createdDate DESC")
    List<User> findRecentUsers();
    
    // Uses Quick Sort internally for efficient sorting
    List<User> findAll(Sort sort);
}""",
        "j2ee": """// J2EE Collections.sort() uses optimized Quick Sort
List<Order> orders = entityManager.createQuery(
    "SELECT o FROM Order o", Order.class).getResultList();
Collections.sort(orders, Comparator.comparing(Order::getDate));""",
    },
    
    "merge_sort": {
        "spring": """// Spring Data - Merge Sort for stable sorting
public interface ProductRepository extends JpaRepository<Product, Long> {
    // Spring uses merge sort for stable, predictable ordering
    List<Product> findAllByCategoryOrderByNameAsc(String category);
}""",
        ".net": """// .NET LINQ OrderBy uses stable merge sort
var sortedProducts = products
    .OrderBy(p => p.Category)
    .ThenBy(p => p.Name)
    .ToList();""",
    },
    
    "heap_sort": {
        "kubernetes": """# Kubernetes Priority Queue uses heap sort
apiVersion: scheduling.k8s.io/v1
kind: PriorityClass
metadata:
  name: high-priority
value: 1000
# Pods scheduled using heap-based priority queue""",
    },
    
    # Searching Algorithms
    "binary_search": {
        "spring": """// Spring Data JPA - Binary search on indexed fields
public interface UserRepository extends JpaRepository<User, Long> {
    // Uses binary search on indexed email field
    Optional<User> findByEmail(String email);
    
    // Binary search for range queries
    List<User> findByIdBetween(Long start, Long end);
}""",
        ".net": """// .NET Array.BinarySearch for sorted collections
int[] sortedIds = GetSortedUserIds();
int index = Array.BinarySearch(sortedIds, userId);
if (index >= 0) {
    return users[index];
}""",
    },
    
    # Tree Algorithms
    "binary_search_tree": {
        "spring": """// Spring BeanFactory uses tree structure for dependency resolution
@Component
public class ServiceA {
    @Autowired
    private ServiceB serviceB;  // Tree-based dependency graph
}

// Spring's ApplicationContext maintains bean hierarchy as tree""",
        "j2ee": """// J2EE JNDI uses tree structure for naming
InitialContext ctx = new InitialContext();
// Tree-based naming: java:comp/env/jdbc/MyDB
DataSource ds = (DataSource) ctx.lookup("java:comp/env/jdbc/MyDB");""",
    },
    
    "avl_tree": {
        "kubernetes": """# Kubernetes etcd uses balanced trees (similar to AVL)
# etcd stores cluster state in balanced tree structure
# Ensures O(log n) lookup for configuration data
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  key: value""",
    },
    
    # Graph Algorithms
    "bfs": {
        "kubernetes": """# Kubernetes service discovery uses BFS
# Traverses service graph level by level
apiVersion: v1
kind: Service
metadata:
  name: frontend
spec:
  selector:
    app: frontend
  # BFS used for endpoint discovery""",
        "docker": """# Docker network uses BFS for service discovery
# docker-compose.yml - BFS traverses service dependencies
version: '3'
services:
  web:
    depends_on:
      - db
      - cache""",
    },
    
    "dfs": {
        "spring": """// Spring dependency injection uses DFS
// Traverses dependency graph depth-first
@Component
public class OrderService {
    @Autowired
    private PaymentService paymentService;  // DFS resolves dependencies
}

@Component
public class PaymentService {
    @Autowired
    private NotificationService notificationService;
}""",
    },
    
    "dijkstra": {
        "kubernetes": """# Kubernetes network routing uses Dijkstra's algorithm
# Finds shortest path between pods/services
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-frontend
# Shortest path routing for network policies""",
    },
    
    # Dynamic Programming
    "edit_distance": {
        "kafka": """// Kafka message deduplication uses edit distance
// Detects similar/duplicate messages
Properties props = new Properties();
props.put("enable.idempotence", "true");
// Edit distance used for message similarity detection""",
    },
    
    "knapsack": {
        "kubernetes": """# Kubernetes resource allocation uses knapsack-like optimization
# Maximizes pod placement within node capacity
apiVersion: v1
kind: Pod
spec:
  containers:
  - name: app
    resources:
      requests:
        memory: "256Mi"
        cpu: "100m"
      limits:
        memory: "512Mi"
        cpu: "200m"
# Knapsack algorithm optimizes resource allocation""",
    },
    
    # String Algorithms
    "kmp": {
        "kafka": """// Kafka topic name pattern matching uses KMP
// Efficient pattern search in topic names
KafkaConsumer<String, String> consumer = new KafkaConsumer<>(props);
Pattern pattern = Pattern.compile("user-.*");
// KMP algorithm for efficient pattern matching""",
    },
    
    # Design Patterns
    "singleton": {
        "spring": """// Spring Singleton Bean (default scope)
@Component  // Singleton by default
public class DatabaseConnectionManager {
    @Autowired
    private DataSource dataSource;
    
    // Spring container ensures single instance per application context
    public Connection getConnection() throws SQLException {
        return dataSource.getConnection();
    }
}""",
        "j2ee": """// J2EE Singleton EJB
@Singleton
@Startup
@ConcurrencyManagement(ConcurrencyManagementType.CONTAINER)
public class ApplicationCache {
    private final Map<String, Object> cache = new ConcurrentHashMap<>();
    
    @PostConstruct
    public void init() {
        // Single instance initialized at startup
    }
    
    public void put(String key, Object value) {
        cache.put(key, value);
    }
}""",
        ".net": """// .NET Dependency Injection Singleton
public class CacheService {
    // Registered as singleton in Startup.cs
    public void Add(string key, object value) { }
}

// Startup.cs
services.AddSingleton<CacheService>();""",
    },
    
    "factory": {
        "spring": """// Spring Factory Pattern - BeanFactory
@Component
public class PaymentProcessorFactory {
    private final Map<String, PaymentProcessor> processors;
    
    @Autowired
    public PaymentProcessorFactory(List<PaymentProcessor> processors) {
        this.processors = processors.stream()
            .collect(Collectors.toMap(
                PaymentProcessor::getType,
                Function.identity()
            ));
    }
    
    public PaymentProcessor getProcessor(String type) {
        return processors.get(type);
    }
}""",
        "j2ee": """// J2EE Factory Pattern
@Stateless
public class ConnectionFactory {
    @Resource(lookup = "java:comp/env/jdbc/MyDB")
    private DataSource dataSource;
    
    public Connection createConnection() {
        return dataSource.getConnection();
    }
}""",
        ".net": """// .NET Factory Pattern
public interface IPaymentProcessor {
    void ProcessPayment(decimal amount);
}

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
    
    "abstract_factory": {
        "spring": """// Spring Abstract Factory - Multiple bean factories
@Configuration
public class DatabaseConfig {
    @Bean
    @Primary
    public DataSource primaryDataSource() {
        return new HikariDataSource();
    }
    
    @Bean
    public DataSource secondaryDataSource() {
        return new HikariDataSource();
    }
}

// Factory creates families of related objects""",
        ".net": """// .NET Abstract Factory
public interface IDatabaseFactory {
    IConnection CreateConnection();
    ICommand CreateCommand();
}

public class SqlServerFactory : IDatabaseFactory {
    public IConnection CreateConnection() => new SqlConnection();
    public ICommand CreateCommand() => new SqlCommand();
}""",
    },
    
    "observer": {
        "spring": """// Spring Event Listener (Observer Pattern)
@Component
public class OrderEventListener {
    @EventListener
    @Async
    public void handleOrderCreated(OrderCreatedEvent event) {
        // Observer receives event notification
        sendEmail(event.getOrder());
        updateInventory(event.getOrder());
    }
}

// Publisher
@Service
public class OrderService {
    @Autowired
    private ApplicationEventPublisher eventPublisher;
    
    public void createOrder(Order order) {
        // ... create order
        eventPublisher.publishEvent(new OrderCreatedEvent(order));
    }
}""",
        ".net": """// .NET Event Handler (Observer Pattern)
public class OrderService {
    public event EventHandler<OrderCreatedEventArgs> OrderCreated;
    
    public void CreateOrder(Order order) {
        // Create order logic
        OnOrderCreated(new OrderCreatedEventArgs(order));
    }
    
    protected virtual void OnOrderCreated(OrderCreatedEventArgs e) {
        OrderCreated?.Invoke(this, e);
    }
}

// Observer
public class EmailService {
    public void Subscribe(OrderService orderService) {
        orderService.OrderCreated += HandleOrderCreated;
    }
    
    private void HandleOrderCreated(object sender, OrderCreatedEventArgs e) {
        SendEmail(e.Order);
    }
}""",
    },
    
    "strategy": {
        "spring": """// Spring Strategy Pattern - Multiple implementations
public interface PaymentStrategy {
    void pay(BigDecimal amount);
}

@Component("creditCard")
public class CreditCardStrategy implements PaymentStrategy {
    public void pay(BigDecimal amount) { }
}

@Component("paypal")
public class PayPalStrategy implements PaymentStrategy {
    public void pay(BigDecimal amount) { }
}

@Service
public class PaymentService {
    @Autowired
    private Map<String, PaymentStrategy> strategies;
    
    public void processPayment(String type, BigDecimal amount) {
        strategies.get(type).pay(amount);
    }
}""",
        ".net": """// .NET Strategy Pattern
public interface ISortStrategy {
    void Sort(List<int> data);
}

public class QuickSortStrategy : ISortStrategy {
    public void Sort(List<int> data) { }
}

public class MergeSortStrategy : ISortStrategy {
    public void Sort(List<int> data) { }
}

public class Sorter {
    private ISortStrategy strategy;
    
    public void SetStrategy(ISortStrategy strategy) {
        this.strategy = strategy;
    }
    
    public void Sort(List<int> data) {
        strategy.Sort(data);
    }
}""",
    },
    
    "mvc": {
        "spring": """// Spring MVC Pattern
@Controller
@RequestMapping("/orders")
public class OrderController {  // View
    @Autowired
    private OrderService orderService;  // Model
    
    @GetMapping("/{id}")
    public String getOrder(@PathVariable Long id, Model model) {
        Order order = orderService.findById(id);  // Controller
        model.addAttribute("order", order);
        return "order-detail";  // View name
    }
}

@Service
public class OrderService {  // Model
    public Order findById(Long id) {
        return orderRepository.findById(id).orElseThrow();
    }
}""",
        ".net": """// .NET MVC Pattern
// Controller
public class OrderController : Controller {
    private readonly IOrderService orderService;
    
    public OrderController(IOrderService orderService) {
        this.orderService = orderService;
    }
    
    public IActionResult Details(int id) {
        var order = orderService.GetById(id);
        return View(order);  // View
    }
}

// Model
public class Order {
    public int Id { get; set; }
    public decimal Total { get; set; }
}""",
    },
    
    "repository": {
        "spring": """// Spring Data Repository Pattern
public interface UserRepository extends JpaRepository<User, Long> {
    List<User> findByEmail(String email);
    List<User> findByCreatedDateAfter(LocalDateTime date);
}

@Service
public class UserService {
    @Autowired
    private UserRepository userRepository;  // Repository abstraction
    
    public User findUser(Long id) {
        return userRepository.findById(id).orElseThrow();
    }
}""",
        ".net": """// .NET Repository Pattern
public interface IUserRepository {
    User GetById(int id);
    IEnumerable<User> GetAll();
    void Add(User user);
}

public class UserRepository : IUserRepository {
    private readonly DbContext context;
    
    public User GetById(int id) {
        return context.Users.Find(id);
    }
}""",
    },
    
    # Security Patterns
    "jwt": {
        "spring": """// Spring Security JWT
@Component
public class JwtTokenProvider {
    private String secretKey = "secret";
    
    public String generateToken(UserDetails userDetails) {
        return Jwts.builder()
            .setSubject(userDetails.getUsername())
            .setExpiration(new Date(System.currentTimeMillis() + 86400000))
            .signWith(SignatureAlgorithm.HS512, secretKey)
            .compact();
    }
    
    public boolean validateToken(String token) {
        try {
            Jwts.parser().setSigningKey(secretKey).parseClaimsJws(token);
            return true;
        } catch (JwtException e) {
            return false;
        }
    }
}""",
        ".net": """// .NET JWT Authentication
public class JwtTokenService {
    public string GenerateToken(User user) {
        var tokenHandler = new JwtSecurityTokenHandler();
        var key = Encoding.ASCII.GetBytes("secret");
        var tokenDescriptor = new SecurityTokenDescriptor {
            Subject = new ClaimsIdentity(new[] {
                new Claim(ClaimTypes.Name, user.Username)
            }),
            Expires = DateTime.UtcNow.AddDays(1),
            SigningCredentials = new SigningCredentials(
                new SymmetricSecurityKey(key),
                SecurityAlgorithms.HmacSha256Signature
            )
        };
        var token = tokenHandler.CreateToken(tokenDescriptor);
        return tokenHandler.WriteToken(token);
    }
}""",
    },
    
    "oauth": {
        "spring": """// Spring Security OAuth 2.0
@Configuration
@EnableAuthorizationServer
public class OAuth2Config extends AuthorizationServerConfigurerAdapter {
    @Override
    public void configure(ClientDetailsServiceConfigurer clients) {
        clients.inMemory()
            .withClient("client-id")
            .secret("client-secret")
            .authorizedGrantTypes("authorization_code", "refresh_token")
            .scopes("read", "write")
            .redirectUris("http://localhost:8080/callback");
    }
}""",
    },
    
    "authentication": {
        "spring": """// Spring Security Authentication
@Service
public class UserDetailsServiceImpl implements UserDetailsService {
    @Autowired
    private UserRepository userRepository;
    
    @Override
    public UserDetails loadUserByUsername(String username) {
        User user = userRepository.findByUsername(username)
            .orElseThrow(() -> new UsernameNotFoundException(username));
        
        return User.builder()
            .username(user.getUsername())
            .password(user.getPasswordHash())
            .authorities(getAuthorities(user))
            .build();
    }
}""",
        ".net": """// .NET Authentication
public class AuthenticationService {
    public async Task<AuthResult> AuthenticateAsync(string username, string password) {
        var user = await userRepository.FindByUsernameAsync(username);
        if (user == null || !VerifyPassword(password, user.PasswordHash)) {
            return AuthResult.Failed();
        }
        
        var token = jwtTokenService.GenerateToken(user);
        return AuthResult.Success(token);
    }
}""",
    },
    
    "authorization": {
        "spring": """// Spring Security Authorization (RBAC)
@Configuration
@EnableWebSecurity
public class SecurityConfig extends WebSecurityConfigurerAdapter {
    @Override
    protected void configure(HttpSecurity http) {
        http.authorizeRequests()
            .antMatchers("/admin/**").hasRole("ADMIN")
            .antMatchers("/user/**").hasAnyRole("USER", "ADMIN")
            .antMatchers("/public/**").permitAll()
            .anyRequest().authenticated();
    }
}""",
        ".net": """// .NET Authorization (RBAC)
[Authorize(Roles = "Admin")]
public class AdminController : Controller {
    [Authorize(Policy = "RequireAdminRole")]
    public IActionResult ManageUsers() {
        return View();
    }
}

// Startup.cs
services.AddAuthorization(options => {
    options.AddPolicy("RequireAdminRole", policy => {
        policy.RequireRole("Admin");
    });
});""",
    },
    
    # Testing Patterns
    "unit_testing": {
        "spring": """// Spring Boot Unit Testing
@SpringBootTest
class UserServiceTest {
    @MockBean
    private UserRepository userRepository;
    
    @Autowired
    private UserService userService;
    
    @Test
    void testFindUser() {
        User user = new User("test", "test@example.com");
        when(userRepository.findById(1L)).thenReturn(Optional.of(user));
        
        User found = userService.findUser(1L);
        assertEquals("test", found.getUsername());
    }
}""",
        ".net": """// .NET xUnit Unit Testing
public class UserServiceTests {
    private readonly Mock<IUserRepository> mockRepository;
    private readonly UserService userService;
    
    public UserServiceTests() {
        mockRepository = new Mock<IUserRepository>();
        userService = new UserService(mockRepository.Object);
    }
    
    [Fact]
    public void GetUser_ReturnsUser_WhenExists() {
        var user = new User { Id = 1, Username = "test" };
        mockRepository.Setup(r => r.GetById(1)).Returns(user);
        
        var result = userService.GetUser(1);
        
        Assert.Equal("test", result.Username);
    }
}""",
    },
    
    "mocking": {
        "spring": """// Spring Mockito Mocking
@ExtendWith(MockitoExtension.class)
class PaymentServiceTest {
    @Mock
    private PaymentGateway paymentGateway;
    
    @InjectMocks
    private PaymentService paymentService;
    
    @Test
    void testProcessPayment() {
        when(paymentGateway.process(any())).thenReturn(true);
        
        boolean result = paymentService.processPayment(100.0);
        
        assertTrue(result);
        verify(paymentGateway).process(any());
    }
}""",
        ".net": """// .NET Moq Mocking
public class PaymentServiceTests {
    [Fact]
    public void ProcessPayment_ReturnsTrue_WhenGatewaySucceeds() {
        var mockGateway = new Mock<IPaymentGateway>();
        mockGateway.Setup(g => g.Process(It.IsAny<decimal>())).Returns(true);
        
        var service = new PaymentService(mockGateway.Object);
        var result = service.ProcessPayment(100m);
        
        Assert.True(result);
        mockGateway.Verify(g => g.Process(100m), Times.Once);
    }
}""",
    },
    
    # Deployment Patterns
    "blue_green": {
        "kubernetes": """# Kubernetes Blue-Green Deployment
# Blue deployment (current)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app-blue
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
      version: blue
  template:
    metadata:
      labels:
        app: myapp
        version: blue
---
# Green deployment (new)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app-green
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
      version: green
---
# Service switches between blue/green
apiVersion: v1
kind: Service
metadata:
  name: app-service
spec:
  selector:
    app: myapp
    version: blue  # Switch to 'green' for deployment""",
        "docker": """# Docker Blue-Green Deployment
# docker-compose.blue.yml
version: '3'
services:
  app:
    image: myapp:v1.0
    labels:
      - "version=blue"

# docker-compose.green.yml  
version: '3'
services:
  app:
    image: myapp:v1.1
    labels:
      - "version=green"

# Switch traffic by updating load balancer configuration""",
    },
    
    "canary": {
        "kubernetes": """# Kubernetes Canary Deployment
# Main deployment (90% traffic)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app-main
spec:
  replicas: 9
---
# Canary deployment (10% traffic)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app-canary
spec:
  replicas: 1
---
# Service with traffic splitting
apiVersion: v1
kind: Service
metadata:
  name: app-service
spec:
  selector:
    app: myapp
  # Istio/Linkerd handles traffic splitting""",
    },
    
    # Performance Patterns
    "caching": {
        "spring": """// Spring Cache Abstraction
@Service
public class ProductService {
    @Cacheable(value = "products", key = "#id")
    public Product getProduct(Long id) {
        return productRepository.findById(id).orElseThrow();
    }
    
    @CacheEvict(value = "products", key = "#id")
    public void updateProduct(Long id, Product product) {
        productRepository.save(product);
    }
}

@Configuration
@EnableCaching
public class CacheConfig {
    @Bean
    public CacheManager cacheManager() {
        return new ConcurrentMapCacheManager("products");
    }
}""",
        ".net": """// .NET Memory Cache
public class ProductService {
    private readonly IMemoryCache cache;
    
    public ProductService(IMemoryCache cache) {
        this.cache = cache;
    }
    
    public Product GetProduct(int id) {
        return cache.GetOrCreate($"product-{id}", entry => {
            entry.AbsoluteExpirationRelativeToNow = TimeSpan.FromMinutes(5);
            return productRepository.GetById(id);
        });
    }
}""",
    },
    
    "load_balancing": {
        "kubernetes": """# Kubernetes Load Balancing
apiVersion: v1
kind: Service
metadata:
  name: app-service
spec:
  type: LoadBalancer
  selector:
    app: myapp
  ports:
  - port: 80
    targetPort: 8080
  # Kubernetes automatically load balances across pods""",
        "docker": """# Docker Swarm Load Balancing
version: '3'
services:
  web:
    image: nginx
    deploy:
      replicas: 3
      # Docker Swarm load balances across replicas
    ports:
      - "80:80"
---
# docker-compose up --scale web=3""",
    },
    
    "rate_limiting": {
        "spring": """// Spring Rate Limiting with Bucket4j
@Configuration
public class RateLimitConfig {
    @Bean
    public RateLimiter rateLimiter() {
        return RateLimiter.create(100.0);  // 100 requests per second
    }
}

@RestController
public class ApiController {
    @Autowired
    private RateLimiter rateLimiter;
    
    @GetMapping("/api/data")
    public ResponseEntity<?> getData() {
        if (!rateLimiter.tryAcquire()) {
            return ResponseEntity.status(429).build();
        }
        return ResponseEntity.ok(data);
    }
}""",
        "kubernetes": """# Kubernetes Rate Limiting (Istio)
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: ratings
spec:
  hosts:
  - ratings
  http:
  - match:
    - headers:
        end-user:
          exact: jason
    route:
    - destination:
        host: ratings
        subset: v1
    fault:
      delay:
        percentage:
          value: 0.1
        fixedDelay: 5s""",
    },
    
    # Integration Patterns
    "message_queue": {
        "spring": """// Spring JMS Message Queue
@Configuration
@EnableJms
public class JmsConfig {
    @Bean
    public JmsTemplate jmsTemplate(ConnectionFactory connectionFactory) {
        return new JmsTemplate(connectionFactory);
    }
}

@Service
public class OrderService {
    @Autowired
    private JmsTemplate jmsTemplate;
    
    public void createOrder(Order order) {
        jmsTemplate.convertAndSend("order.queue", order);
    }
}

@JmsListener(destination = "order.queue")
public void processOrder(Order order) {
    // Process order from queue
}""",
        "kafka": """// Apache Kafka Producer/Consumer
// Producer
Properties props = new Properties();
props.put("bootstrap.servers", "localhost:9092");
props.put("key.serializer", "org.apache.kafka.common.serialization.StringSerializer");
props.put("value.serializer", "org.apache.kafka.common.serialization.StringSerializer");

KafkaProducer<String, String> producer = new KafkaProducer<>(props);
producer.send(new ProducerRecord<>("orders", orderId, orderJson));

// Consumer
KafkaConsumer<String, String> consumer = new KafkaConsumer<>(props);
consumer.subscribe(Collections.singletonList("orders"));
ConsumerRecords<String, String> records = consumer.poll(Duration.ofMillis(100));
for (ConsumerRecord<String, String> record : records) {
    processOrder(record.value());
}""",
    },
    
    "publish_subscribe": {
        "kafka": """// Apache Kafka Pub-Sub
// Publisher
KafkaProducer<String, String> producer = new KafkaProducer<>(props);
producer.send(new ProducerRecord<>("events", "order.created", eventJson));

// Multiple Subscribers
// Subscriber 1: Email Service
KafkaConsumer<String, String> emailConsumer = new KafkaConsumer<>(props);
emailConsumer.subscribe(Collections.singletonList("events"));

// Subscriber 2: Notification Service  
KafkaConsumer<String, String> notifConsumer = new KafkaConsumer<>(props);
notifConsumer.subscribe(Collections.singletonList("events"));

// Both receive the same message""",
        "spring": """// Spring Event Pub-Sub
// Publisher
@Service
public class OrderService {
    @Autowired
    private ApplicationEventPublisher eventPublisher;
    
    public void createOrder(Order order) {
        // ... create order
        eventPublisher.publishEvent(new OrderCreatedEvent(order));
    }
}

// Multiple Subscribers
@Component
public class EmailService {
    @EventListener
    public void handleOrderCreated(OrderCreatedEvent event) {
        sendEmail(event.getOrder());
    }
}

@Component
public class NotificationService {
    @EventListener
    public void handleOrderCreated(OrderCreatedEvent event) {
        sendNotification(event.getOrder());
    }
}""",
    },
    
    # Crypto Algorithms
    "aes": {
        "spring": """// Spring Security AES Encryption
@Service
public class EncryptionService {
    private final SecretKey secretKey;
    private final Cipher cipher;
    
    public EncryptionService() throws Exception {
        KeyGenerator keyGenerator = KeyGenerator.getInstance("AES");
        keyGenerator.init(256);
        secretKey = keyGenerator.generateKey();
        cipher = Cipher.getInstance("AES/GCM/NoPadding");
    }
    
    public String encrypt(String plaintext) throws Exception {
        cipher.init(Cipher.ENCRYPT_MODE, secretKey);
        byte[] encrypted = cipher.doFinal(plaintext.getBytes());
        return Base64.getEncoder().encodeToString(encrypted);
    }
}""",
        ".net": """// .NET AES Encryption
public class EncryptionService {
    public string Encrypt(string plaintext) {
        using (Aes aes = Aes.Create()) {
            aes.Key = Encoding.UTF8.GetBytes("32-byte-key-here-123456789012");
            aes.IV = new byte[16];
            
            ICryptoTransform encryptor = aes.CreateEncryptor();
            using (MemoryStream ms = new MemoryStream()) {
                using (CryptoStream cs = new CryptoStream(ms, encryptor, CryptoStreamMode.Write)) {
                    using (StreamWriter sw = new StreamWriter(cs)) {
                        sw.Write(plaintext);
                    }
                }
                return Convert.ToBase64String(ms.ToArray());
            }
        }
    }
}""",
    },
    
    "rsa": {
        "spring": """// Spring Security RSA
@Service
public class RsaEncryptionService {
    private final KeyPair keyPair;
    
    public RsaEncryptionService() throws NoSuchAlgorithmException {
        KeyPairGenerator keyGen = KeyPairGenerator.getInstance("RSA");
        keyGen.initialize(2048);
        keyPair = keyGen.generateKeyPair();
    }
    
    public byte[] encrypt(byte[] data) throws Exception {
        Cipher cipher = Cipher.getInstance("RSA");
        cipher.init(Cipher.ENCRYPT_MODE, keyPair.getPublic());
        return cipher.doFinal(data);
    }
}""",
    },
    
    "sha256": {
        "spring": """// Spring Security SHA-256 Hashing
@Service
public class PasswordEncoder {
    public String encode(String password) {
        try {
            MessageDigest digest = MessageDigest.getInstance("SHA-256");
            byte[] hash = digest.digest(password.getBytes(StandardCharsets.UTF_8));
            return Base64.getEncoder().encodeToString(hash);
        } catch (NoSuchAlgorithmException e) {
            throw new RuntimeException(e);
        }
    }
}""",
        ".net": """// .NET SHA-256 Hashing
public class PasswordHasher {
    public string HashPassword(string password) {
        using (SHA256 sha256 = SHA256.Create()) {
            byte[] hashBytes = sha256.ComputeHash(Encoding.UTF8.GetBytes(password));
            return Convert.ToBase64String(hashBytes);
        }
    }
}""",
    },
    
    # Distributed Patterns
    "leader_election": {
        "kubernetes": """# Kubernetes Leader Election
apiVersion: apps/v1
kind: Deployment
metadata:
  name: leader-election
spec:
  replicas: 3
  template:
    spec:
      containers:
      - name: app
        # Uses Kubernetes endpoints for leader election
        env:
        - name: LEADER_ELECTION
          value: "true"
        # Only leader pod processes requests""",
        "kafka": """// Kafka Consumer Group Leader Election
Properties props = new Properties();
props.put("group.id", "my-consumer-group");
// Kafka automatically elects leader for consumer group
// Leader coordinates partition assignment
KafkaConsumer<String, String> consumer = new KafkaConsumer<>(props);
consumer.subscribe(Collections.singletonList("topic"));""",
    },
    
    "circuit_breaker": {
        "spring": """// Spring Cloud Circuit Breaker (Resilience4j)
@Service
public class ExternalServiceClient {
    private final CircuitBreaker circuitBreaker;
    
    public ExternalServiceClient() {
        circuitBreaker = CircuitBreaker.of("externalService", 
            CircuitBreakerConfig.custom()
                .failureRateThreshold(50)
                .waitDurationInOpenState(Duration.ofSeconds(30))
                .build());
    }
    
    public String callExternalService() {
        return circuitBreaker.executeSupplier(() -> {
            // Call external service
            return restTemplate.getForObject("http://external/api", String.class);
        });
    }
}""",
    },
    
    "retry_pattern": {
        "spring": """// Spring Retry
@Service
public class PaymentService {
    @Retryable(value = {PaymentException.class}, maxAttempts = 3, backoff = @Backoff(delay = 1000))
    public void processPayment(Payment payment) {
        // Retries up to 3 times with 1 second delay
        paymentGateway.process(payment);
    }
    
    @Recover
    public void recover(PaymentException e, Payment payment) {
        // Handle failure after all retries
    }
}

@Configuration
@EnableRetry
public class RetryConfig {
}""",
    },
    
    # ML Algorithms
    "linear_regression": {
        "spring": """// Spring ML Integration (example structure)
@Service
public class PredictionService {
    // Uses linear regression for predictions
    public double predictPrice(double size, double location) {
        // Linear regression model: price = a * size + b * location + c
        return model.predict(size, location);
    }
}""",
    },
    
    "svm": {
        "spring": """// Spring ML - SVM Classifier
@Service
public class ClassificationService {
    private final SVMClassifier classifier;
    
    public String classify(Features features) {
        // SVM used for binary/multi-class classification
        return classifier.predict(features);
    }
}""",
    },
    
    # Monitoring
    "log_aggregation": {
        "kubernetes": """# Kubernetes Log Aggregation (Fluentd/ELK)
apiVersion: v1
kind: ConfigMap
metadata:
  name: fluentd-config
data:
  fluent.conf: |
    <source>
      @type tail
      path /var/log/containers/*.log
    </source>
    <match **>
      @type elasticsearch
      host elasticsearch.logging.svc.cluster.local
    </match>
---
# DaemonSet collects logs from all pods
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: fluentd
spec:
  template:
    spec:
      containers:
      - name: fluentd
        image: fluent/fluentd-kubernetes-daemonset""",
        "docker": """# Docker Log Aggregation
# docker-compose.yml with centralized logging
version: '3'
services:
  app:
    image: myapp
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
  
  fluentd:
    image: fluent/fluentd
    volumes:
      - ./logs:/var/log
    # Aggregates logs from all containers""",
    },
}

# Category-based framework examples for algorithms not in specific mapping
CATEGORY_FRAMEWORKS: Dict[str, Dict[str, str]] = {
    "sorting": {
        "spring": """// Spring Data JPA - Sorting
public interface UserRepository extends JpaRepository<User, Long> {
    List<User> findAll(Sort sort);
    // Spring uses efficient sorting algorithms for query results
}""",
        "j2ee": """// J2EE Collections.sort()
List<Order> orders = getOrders();
Collections.sort(orders, Comparator.comparing(Order::getDate));
// Uses optimized sorting algorithms""",
    },
    "searching": {
        "spring": """// Spring Data - Indexed search
public interface ProductRepository extends JpaRepository<Product, Long> {
    Optional<Product> findBySku(String sku);  // Uses indexed search
}""",
    },
    "trees": {
        "spring": """// Spring BeanFactory - Tree structure
@Component
public class ServiceA {
    @Autowired
    private ServiceB serviceB;  // Tree-based dependency graph
}""",
    },
    "graphs": {
        "kubernetes": """# Kubernetes - Service graph
apiVersion: v1
kind: Service
metadata:
  name: frontend
spec:
  selector:
    app: frontend
  # Graph algorithms for service discovery""",
    },
    "security": {
        "spring": """// Spring Security
@Configuration
@EnableWebSecurity
public class SecurityConfig extends WebSecurityConfigurerAdapter {
    // Security patterns implementation
}""",
    },
    "testing": {
        "spring": """// Spring Boot Testing
@SpringBootTest
class ServiceTest {
    @Test
    void testMethod() {
        // Testing pattern implementation
    }
}""",
    },
    "deployment": {
        "kubernetes": """# Kubernetes Deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app
spec:
  replicas: 3
  # Deployment pattern implementation""",
    },
    "performance": {
        "spring": """// Spring Cache
@Cacheable("cache")
public Object getData() {
    // Performance pattern implementation
}""",
    },
    "patterns": {
        "spring": """// Spring Framework Pattern
@Component
public class Service {
    // Design pattern implementation
}""",
    },
}


def infer_category(lecture_path: str) -> Optional[str]:
    """Infer category from lecture path."""
    path_lower = lecture_path.lower()
    
    if any(x in path_lower for x in ["sorting", "sort"]):
        return "sorting"
    elif any(x in path_lower for x in ["searching", "search"]):
        return "searching"
    elif any(x in path_lower for x in ["tree", "trees"]):
        return "trees"
    elif any(x in path_lower for x in ["graph", "graphs"]):
        return "graphs"
    elif any(x in path_lower for x in ["dynamic_programming", "dp"]):
        return "dp"
    elif any(x in path_lower for x in ["string", "strings"]):
        return "strings"
    elif any(x in path_lower for x in ["security", "crypto", "encryption", "jwt", "oauth", "authentication"]):
        return "security"
    elif any(x in path_lower for x in ["testing", "test", "tdd", "mocking"]):
        return "testing"
    elif any(x in path_lower for x in ["deployment", "blue_green", "canary"]):
        return "deployment"
    elif any(x in path_lower for x in ["performance", "caching", "load_balancing", "rate_limiting"]):
        return "performance"
    elif any(x in path_lower for x in ["pattern", "solid", "creational", "structural", "behavioral", "architectural"]):
        return "patterns"
    elif any(x in path_lower for x in ["integration", "message_queue", "publish_subscribe", "cqrs"]):
        return "integration"
    elif any(x in path_lower for x in ["distributed", "leader_election", "circuit_breaker"]):
        return "distributed"
    elif any(x in path_lower for x in ["monitoring", "observability", "log_aggregation"]):
        return "monitoring"
    elif any(x in path_lower for x in ["ml", "machine_learning", "neural", "cnn", "rnn"]):
        return "ml"
    
    return None


def get_framework_examples(algorithm_name: str, category: Optional[str]) -> Dict[str, str]:
    """Get framework examples for an algorithm."""
    # Try exact match first
    normalized_name = algorithm_name.lower().replace("-", "_")
    if normalized_name in FRAMEWORK_EXAMPLES:
        return FRAMEWORK_EXAMPLES[normalized_name]
    
    # Try category-based examples
    if category and category in CATEGORY_FRAMEWORKS:
        return CATEGORY_FRAMEWORKS[category]
    
    return {}


def generate_examples_section(algorithm_name: str, category: Optional[str]) -> str:
    """Generate the Examples of Implementation section."""
    examples = get_framework_examples(algorithm_name, category)
    
    if not examples:
        return """## Examples of Implementation

This algorithm/pattern is implemented in various frameworks and technologies.

*Note: Framework-specific examples will be added based on actual implementations.*
"""
    
    section = "## Examples of Implementation\n\n"
    section += "This algorithm/pattern is implemented in the following frameworks and technologies:\n\n"
    
    # Spring Framework
    if "spring" in examples:
        section += "### Spring Framework\n\n"
        section += "```java\n"
        section += examples["spring"].strip()
        section += "\n```\n\n"
        # More specific purpose based on algorithm type
        if "singleton" in algorithm_name.lower():
            section += "**Purpose**: Spring manages beans as singletons by default, ensuring " \
                      "single instance per application context for efficient resource usage.\n\n"
        elif "factory" in algorithm_name.lower():
            section += "**Purpose**: Spring's BeanFactory and ApplicationContext use factory pattern " \
                      "to create and manage bean instances with dependency injection.\n\n"
        elif "observer" in algorithm_name.lower():
            section += "**Purpose**: Spring's ApplicationEventPublisher implements observer pattern " \
                      "for decoupled event-driven communication between components.\n\n"
        elif "jwt" in algorithm_name.lower() or "token" in algorithm_name.lower():
            section += "**Purpose**: Spring Security uses JWT for stateless authentication and " \
                      "authorization in REST APIs and microservices.\n\n"
        elif "repository" in algorithm_name.lower():
            section += "**Purpose**: Spring Data repositories abstract data access, providing " \
                      "consistent interface for database operations across different persistence technologies.\n\n"
        elif "mvc" in algorithm_name.lower():
            section += "**Purpose**: Spring MVC separates concerns into Model, View, and Controller " \
                      "for building web applications with clear separation of responsibilities.\n\n"
        elif "sort" in algorithm_name.lower():
            section += "**Purpose**: Spring Data JPA uses sorting algorithms for efficient query " \
                      "result ordering and pagination in database operations.\n\n"
        elif "search" in algorithm_name.lower():
            section += "**Purpose**: Spring Data repositories use search algorithms for indexed " \
                      "queries and efficient data retrieval from databases.\n\n"
        else:
            section += "**Purpose**: Spring Framework uses this pattern for dependency injection, " \
                      "bean management, and enterprise application development.\n\n"
    
    # J2EE
    if "j2ee" in examples:
        section += "### J2EE (Java Enterprise Edition)\n\n"
        section += "```java\n"
        section += examples["j2ee"].strip()
        section += "\n```\n\n"
        # More specific purpose for J2EE
        if "singleton" in algorithm_name.lower():
            section += "**Purpose**: J2EE Singleton EJB ensures single instance per application " \
                      "for shared resources like caches and connection pools.\n\n"
        elif "factory" in algorithm_name.lower():
            section += "**Purpose**: J2EE uses factory pattern for creating enterprise resources " \
                      "like DataSource, JMS connections, and EJB instances.\n\n"
        elif "repository" in algorithm_name.lower():
            section += "**Purpose**: J2EE JPA repositories provide data access abstraction for " \
                      "enterprise applications with transaction management.\n\n"
        else:
            section += "**Purpose**: J2EE implements this pattern for enterprise Java applications, " \
                      "EJB containers, and Java EE specifications.\n\n"
    
    # .NET
    if ".net" in examples:
        section += "### .NET Framework\n\n"
        section += "```csharp\n"
        section += examples[".net"].strip()
        section += "\n```\n\n"
        section += "**Purpose**: .NET Framework uses this pattern for dependency injection, " \
                  "ASP.NET Core, and enterprise application development.\n\n"
    
    # Docker
    if "docker" in examples:
        section += "### Docker\n\n"
        section += "```dockerfile\n"
        section += examples["docker"].strip()
        section += "\n```\n\n"
        section += "**Purpose**: Docker uses this pattern for containerization, " \
                  "image layering, and container orchestration.\n\n"
    
    # Kubernetes
    if "kubernetes" in examples:
        section += "### Kubernetes\n\n"
        section += "```yaml\n"
        section += examples["kubernetes"].strip()
        section += "\n```\n\n"
        section += "**Purpose**: Kubernetes uses this pattern for container orchestration, " \
                  "service discovery, and resource management.\n\n"
    
    # Apache Kafka
    if "kafka" in examples:
        section += "### Apache Kafka\n\n"
        section += "```java\n"
        section += examples["kafka"].strip()
        section += "\n```\n\n"
        section += "**Purpose**: Apache Kafka uses this pattern for event streaming, " \
                  "message queuing, and distributed system communication.\n\n"
    
    return section


def update_readme_examples(readme_path: Path, algorithm_name: str, category: Optional[str]) -> bool:
    """Update the Examples of Implementation section in a README file."""
    try:
        content = readme_path.read_text(encoding="utf-8")
        new_section = generate_examples_section(algorithm_name, category)
        
        # Pattern to match the "Examples of Implementation" section
        # Matches from "## Examples of Implementation" to the next "##" or end of file
        pattern = r"(##\s+Examples\s+of\s+Implementation\s*\n)(.*?)(?=\n##\s+|$)"
        
        if re.search(pattern, content, re.IGNORECASE | re.DOTALL):
            # Section exists, replace it
            new_content = re.sub(pattern, r"\1" + new_section.split("## Examples of Implementation\n")[1], 
                                content, flags=re.IGNORECASE | re.DOTALL)
        else:
            # Section doesn't exist, add it before "Do Not Confuse With" or at the end
            confuse_pattern = r"(##\s+Do\s+Not\s+Confuse\s+With)"
            if re.search(confuse_pattern, content, re.IGNORECASE):
                new_content = re.sub(confuse_pattern, new_section + "\\1", content, flags=re.IGNORECASE)
            else:
                # Add at the end
                if not content.endswith("\n"):
                    content += "\n"
                new_content = content + "\n" + new_section
        
        if new_content != content:
            readme_path.write_text(new_content, encoding="utf-8")
            return True
        
        return False
    except Exception as e:
        print(f"Error processing {readme_path}: {e}")
        return False


def main():
    """Main function to process all algorithm READMEs."""
    updated_count = 0
    processed_count = 0
    
    # Find all algorithm directories
    for semester_dir in ROOT.glob("semester_*"):
        if not semester_dir.is_dir():
            continue
        
        for lecture_dir in semester_dir.iterdir():
            if not lecture_dir.is_dir():
                continue
            
            for algo_dir in lecture_dir.iterdir():
                if not algo_dir.is_dir():
                    continue
                
                # Check if this is an algorithm directory
                if not ((algo_dir / "algorithm.py").exists() or 
                       (algo_dir / "Algorithm.java").exists() or
                       (algo_dir / "README.md").exists()):
                    continue
                
                readme_path = algo_dir / "README.md"
                if not readme_path.exists():
                    continue
                
                algorithm_name = algo_dir.name
                category = infer_category(str(lecture_dir))
                
                processed_count += 1
                if update_readme_examples(readme_path, algorithm_name, category):
                    updated_count += 1
                    print(f"Updated: {readme_path.relative_to(ROOT)}")
    
    print(f"\nProcessed {processed_count} algorithm READMEs")
    print(f"Updated {updated_count} 'Examples of Implementation' sections")


if __name__ == "__main__":
    main()

