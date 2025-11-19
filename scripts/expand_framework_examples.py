#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Expand framework examples to more algorithms and patterns.
Adds comprehensive Spring, .NET, Docker, Kubernetes examples.
"""

import re
from pathlib import Path
from typing import Dict, Optional

ROOT = Path(__file__).resolve().parents[1]

# Comprehensive framework examples
FRAMEWORK_EXAMPLES_EXPANDED = {
    "singleton": {
        "spring": """// Spring Framework - Singleton Bean (Default Scope)
@Component
@Scope("singleton")  // Default, can be omitted
public class DatabaseConnectionManager {
    @Autowired
    private DataSource dataSource;
    
    // Spring container ensures single instance per application context
    public Connection getConnection() throws SQLException {
        return dataSource.getConnection();
    }
}

// Usage
@Autowired
private DatabaseConnectionManager dbManager;""",
        "dotnet": """// .NET Core - Singleton Service
public class CacheService
{
    private static CacheService _instance;
    private static readonly object _lock = new object();
    
    private CacheService() { }
    
    public static CacheService GetInstance()
    {
        if (_instance == null)
        {
            lock (_lock)
            {
                if (_instance == null)
                {
                    _instance = new CacheService();
                }
            }
        }
        return _instance;
    }
}

// .NET Core DI Registration
services.AddSingleton<CacheService>();

// Usage
public class MyController : Controller
{
    private readonly CacheService _cache;
    
    public MyController(CacheService cache)
    {
        _cache = cache;  // Same instance injected everywhere
    }
}""",
        "docker": """# Docker - Single Container Instance
# docker-compose.yml
version: '3.8'
services:
  database:
    image: postgres:13
    container_name: postgres-singleton
    ports:
      - "5432:5432"
    environment:
      POSTGRES_DB: mydb
    # Only one instance should run
    deploy:
      replicas: 1
    restart: unless-stopped

# Kubernetes - Singleton Pod
apiVersion: apps/v1
kind: Deployment
metadata:
  name: database-singleton
spec:
  replicas: 1  # Only one instance
  selector:
    matchLabels:
      app: database
  template:
    metadata:
      labels:
        app: database
    spec:
      containers:
      - name: postgres
        image: postgres:13""",
    },
    "factory": {
        "spring": """// Spring Framework - Factory Pattern
@Component
public class PaymentProcessorFactory {
    
    @Autowired
    private List<PaymentProcessor> processors;
    
    public PaymentProcessor getProcessor(String type) {
        return processors.stream()
            .filter(p -> p.supports(type))
            .findFirst()
            .orElseThrow(() -> new IllegalArgumentException("Unknown type: " + type));
    }
}

// Interface
public interface PaymentProcessor {
    boolean supports(String type);
    void processPayment(BigDecimal amount);
}

// Implementations
@Component
public class CreditCardProcessor implements PaymentProcessor {
    @Override
    public boolean supports(String type) {
        return "credit_card".equals(type);
    }
    
    @Override
    public void processPayment(BigDecimal amount) {
        // Process credit card payment
    }
}

// Usage
@Autowired
private PaymentProcessorFactory factory;

PaymentProcessor processor = factory.getProcessor("credit_card");
processor.processPayment(new BigDecimal("100.00"));""",
        "dotnet": """// .NET - Factory Pattern
public interface IPaymentProcessor
{
    void ProcessPayment(decimal amount);
}

public class PaymentProcessorFactory
{
    public IPaymentProcessor CreateProcessor(string type)
    {
        return type switch
        {
            "credit_card" => new CreditCardProcessor(),
            "paypal" => new PayPalProcessor(),
            "stripe" => new StripeProcessor(),
            _ => throw new ArgumentException($"Unknown processor type: {type}")
        };
    }
}

// .NET Core DI with Factory
services.AddTransient<PaymentProcessorFactory>();
services.AddTransient<CreditCardProcessor>();
services.AddTransient<PayPalProcessor>();

// Usage
public class PaymentService
{
    private readonly PaymentProcessorFactory _factory;
    
    public PaymentService(PaymentProcessorFactory factory)
    {
        _factory = factory;
    }
    
    public void ProcessPayment(string type, decimal amount)
    {
        var processor = _factory.CreateProcessor(type);
        processor.ProcessPayment(amount);
    }
}""",
        "kubernetes": """# Kubernetes - Factory Pattern for Pod Creation
apiVersion: v1
kind: ConfigMap
metadata:
  name: processor-config
data:
  processor-type: "credit_card"
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: payment-processor
spec:
  replicas: 3
  selector:
    matchLabels:
      app: payment-processor
  template:
    metadata:
      labels:
        app: payment-processor
    spec:
      containers:
      - name: processor
        image: payment-processor:latest
        env:
        - name: PROCESSOR_TYPE
          valueFrom:
            configMapKeyRef:
              name: processor-config
              key: processor-type
        # Factory pattern: container creates processor based on env var""",
    },
    "observer": {
        "spring": """// Spring Framework - Observer Pattern (Event Listener)
@Component
public class OrderService {
    
    @Autowired
    private ApplicationEventPublisher eventPublisher;
    
    public void createOrder(Order order) {
        // Create order logic
        orderRepository.save(order);
        
        // Publish event
        eventPublisher.publishEvent(new OrderCreatedEvent(order));
    }
}

// Event
public class OrderCreatedEvent extends ApplicationEvent {
    private final Order order;
    
    public OrderCreatedEvent(Order order) {
        super(order);
        this.order = order;
    }
    
    public Order getOrder() {
        return order;
    }
}

// Observer 1: Email Service
@Component
public class EmailNotificationListener {
    
    @EventListener
    @Async
    public void handleOrderCreated(OrderCreatedEvent event) {
        Order order = event.getOrder();
        emailService.sendOrderConfirmation(order);
    }
}

// Observer 2: Inventory Service
@Component
public class InventoryService {
    
    @EventListener
    public void handleOrderCreated(OrderCreatedEvent event) {
        Order order = event.getOrder();
        inventoryService.updateStock(order.getItems());
    }
}""",
        "dotnet": """// .NET - Observer Pattern (Events)
public class OrderService
{
    public event EventHandler<OrderCreatedEventArgs> OrderCreated;
    
    public void CreateOrder(Order order)
    {
        // Create order logic
        _orderRepository.Save(order);
        
        // Notify observers
        OnOrderCreated(new OrderCreatedEventArgs(order));
    }
    
    protected virtual void OnOrderCreated(OrderCreatedEventArgs e)
    {
        OrderCreated?.Invoke(this, e);
    }
}

// Observer 1: Email Service
public class EmailNotificationService
{
    public void Subscribe(OrderService orderService)
    {
        orderService.OrderCreated += HandleOrderCreated;
    }
    
    private void HandleOrderCreated(object sender, OrderCreatedEventArgs e)
    {
        var order = e.Order;
        _emailService.SendOrderConfirmation(order);
    }
}

// .NET Core - Using IMediator (MediatR)
public class OrderCreatedHandler : INotificationHandler<OrderCreatedEvent>
{
    public Task Handle(OrderCreatedEvent notification, CancellationToken cancellationToken)
    {
        // Handle order created event
        return Task.CompletedTask;
    }
}""",
        "kafka": """# Apache Kafka - Observer Pattern (Pub/Sub)
# Producer
from kafka import KafkaProducer
import json

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Publish event
order_event = {
    'orderId': '12345',
    'status': 'created',
    'items': [{'productId': 'P1', 'quantity': 2}]
}
producer.send('order-events', key=b'order-123', value=order_event)

# Consumer 1 - Email Service
from kafka import KafkaConsumer

consumer1 = KafkaConsumer(
    'order-events',
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

for message in consumer1:
    order_data = message.value
    send_email_notification(order_data)

# Consumer 2 - Inventory Service
consumer2 = KafkaConsumer(
    'order-events',
    bootstrap_servers='localhost:9092',
    group_id='inventory-service',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

for message in consumer2:
    order_data = message.value
    update_inventory(order_data)""",
    },
    "strategy": {
        "spring": """// Spring Framework - Strategy Pattern
public interface SortingStrategy {
    void sort(List<Integer> list);
}

@Component("quickSort")
public class QuickSortStrategy implements SortingStrategy {
    @Override
    public void sort(List<Integer> list) {
        Collections.sort(list);
    }
}

@Component("mergeSort")
public class MergeSortStrategy implements SortingStrategy {
    @Override
    public void sort(List<Integer> list) {
        // Merge sort implementation
    }
}

// Context
@Service
public class SortService {
    private final Map<String, SortingStrategy> strategies;
    
    @Autowired
    public SortService(List<SortingStrategy> strategyList) {
        strategies = strategyList.stream()
            .collect(Collectors.toMap(
                s -> s.getClass().getAnnotation(Component.class).value(),
                Function.identity()
            ));
    }
    
    public void sort(List<Integer> list, String strategyName) {
        SortingStrategy strategy = strategies.get(strategyName);
        if (strategy == null) {
            throw new IllegalArgumentException("Unknown strategy: " + strategyName);
        }
        strategy.sort(list);
    }
}""",
        "dotnet": """// .NET - Strategy Pattern
public interface ISortingStrategy
{
    void Sort(List<int> list);
}

public class QuickSortStrategy : ISortingStrategy
{
    public void Sort(List<int> list)
    {
        list.Sort();
    }
}

public class MergeSortStrategy : ISortingStrategy
{
    public void Sort(List<int> list)
    {
        // Merge sort implementation
    }
}

// Context
public class SortService
{
    private readonly Dictionary<string, ISortingStrategy> _strategies;
    
    public SortService()
    {
        _strategies = new Dictionary<string, ISortingStrategy>
        {
            { "quick", new QuickSortStrategy() },
            { "merge", new MergeSortStrategy() }
        };
    }
    
    public void Sort(List<int> list, string strategyName)
    {
        if (!_strategies.TryGetValue(strategyName, out var strategy))
        {
            throw new ArgumentException($"Unknown strategy: {strategyName}");
        }
        strategy.Sort(list);
    }
}

// .NET Core DI
services.AddTransient<ISortingStrategy, QuickSortStrategy>();
services.AddTransient<ISortingStrategy, MergeSortStrategy>();""",
        "kubernetes": """# Kubernetes - Strategy Pattern for Deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: sort-service
spec:
  replicas: 3
  template:
    spec:
      containers:
      - name: sorter
        image: sort-service:latest
        env:
        - name: SORT_STRATEGY
          value: "quick"  # Strategy: quick, merge, heap
        # Service uses strategy based on env var""",
    },
    "adapter": {
        "spring": """// Spring Framework - Adapter Pattern
// Target Interface
public interface PaymentGateway {
    void processPayment(BigDecimal amount);
}

// Adaptee (Third-party library)
public class LegacyPaymentSystem {
    public void pay(String amount) {
        // Legacy payment processing
    }
}

// Adapter
@Component
public class LegacyPaymentAdapter implements PaymentGateway {
    private final LegacyPaymentSystem legacySystem;
    
    public LegacyPaymentAdapter(LegacyPaymentSystem legacySystem) {
        this.legacySystem = legacySystem;
    }
    
    @Override
    public void processPayment(BigDecimal amount) {
        // Adapt BigDecimal to String
        legacySystem.pay(amount.toString());
    }
}

// Usage
@Service
public class PaymentService {
    @Autowired
    private PaymentGateway paymentGateway;
    
    public void pay(BigDecimal amount) {
        paymentGateway.processPayment(amount);
    }
}""",
        "dotnet": """// .NET - Adapter Pattern
// Target Interface
public interface IPaymentGateway
{
    void ProcessPayment(decimal amount);
}

// Adaptee (Third-party)
public class LegacyPaymentSystem
{
    public void Pay(string amount)
    {
        // Legacy implementation
    }
}

// Adapter
public class LegacyPaymentAdapter : IPaymentGateway
{
    private readonly LegacyPaymentSystem _legacySystem;
    
    public LegacyPaymentAdapter(LegacyPaymentSystem legacySystem)
    {
        _legacySystem = legacySystem;
    }
    
    public void ProcessPayment(decimal amount)
    {
        _legacySystem.Pay(amount.ToString());
    }
}

// .NET Core DI
services.AddSingleton<LegacyPaymentSystem>();
services.AddSingleton<IPaymentGateway, LegacyPaymentAdapter>();""",
        "docker": """# Docker - Adapter Pattern (Service Adapter)
# docker-compose.yml
version: '3.8'
services:
  legacy-service:
    image: legacy-payment:1.0
    ports:
      - "8080:8080"
  
  adapter-service:
    image: payment-adapter:latest
    environment:
      - LEGACY_SERVICE_URL=http://legacy-service:8080
    depends_on:
      - legacy-service
    # Adapter translates between new API and legacy service""",
    },
    "decorator": {
        "spring": """// Spring Framework - Decorator Pattern
public interface DataService {
    String fetchData(String key);
}

// Concrete Component
@Service
public class BasicDataService implements DataService {
    @Override
    public String fetchData(String key) {
        return "Data for " + key;
    }
}

// Decorator
@Service
public class CachingDataServiceDecorator implements DataService {
    private final DataService dataService;
    private final Cache cache;
    
    @Autowired
    public CachingDataServiceDecorator(
            @Qualifier("basicDataService") DataService dataService,
            Cache cache) {
        this.dataService = dataService;
        this.cache = cache;
    }
    
    @Override
    public String fetchData(String key) {
        String cached = cache.get(key);
        if (cached != null) {
            return cached;
        }
        String data = dataService.fetchData(key);
        cache.put(key, data);
        return data;
    }
}

// Another Decorator
@Service
public class LoggingDataServiceDecorator implements DataService {
    private final DataService dataService;
    
    @Autowired
    public LoggingDataServiceDecorator(
            @Qualifier("cachingDataServiceDecorator") DataService dataService) {
        this.dataService = dataService;
    }
    
    @Override
    public String fetchData(String key) {
        logger.info("Fetching data for key: " + key);
        String data = dataService.fetchData(key);
        logger.info("Fetched data: " + data);
        return data;
    }
}""",
        "dotnet": """// .NET - Decorator Pattern
public interface IDataService
{
    string FetchData(string key);
}

// Concrete Component
public class BasicDataService : IDataService
{
    public string FetchData(string key)
    {
        return $"Data for {key}";
    }
}

// Decorator
public class CachingDataServiceDecorator : IDataService
{
    private readonly IDataService _dataService;
    private readonly IMemoryCache _cache;
    
    public CachingDataServiceDecorator(IDataService dataService, IMemoryCache cache)
    {
        _dataService = dataService;
        _cache = cache;
    }
    
    public string FetchData(string key)
    {
        if (_cache.TryGetValue(key, out string cached))
        {
            return cached;
        }
        
        var data = _dataService.FetchData(key);
        _cache.Set(key, data);
        return data;
    }
}

// .NET Core DI - Decorator Chain
services.AddSingleton<BasicDataService>();
services.Decorate<IDataService, CachingDataServiceDecorator>();
services.Decorate<IDataService, LoggingDataServiceDecorator>();""",
        "nginx": """# Nginx - Decorator Pattern (Middleware)
# nginx.conf
server {
    listen 80;
    
    # Decorator 1: Logging
    access_log /var/log/nginx/access.log;
    
    # Decorator 2: Caching
    proxy_cache_path /var/cache/nginx levels=1:2 keys_zone=my_cache:10m;
    
    location / {
        # Decorator 3: Compression
        gzip on;
        gzip_types text/plain application/json;
        
        # Decorator 4: Rate Limiting
        limit_req zone=api_limit burst=10;
        
        proxy_pass http://backend;
        proxy_cache my_cache;
    }
}""",
    },
    "proxy": {
        "spring": """// Spring Framework - Proxy Pattern
public interface ImageService {
    Image loadImage(String filename);
}

// Real Subject
@Service
public class RealImageService implements ImageService {
    @Override
    public Image loadImage(String filename) {
        // Expensive operation: load from disk
        return new Image(filename);
    }
}

// Proxy
@Service
public class ImageServiceProxy implements ImageService {
    private final ImageService realService;
    private final Map<String, Image> cache = new ConcurrentHashMap<>();
    
    @Autowired
    public ImageServiceProxy(@Qualifier("realImageService") ImageService realService) {
        this.realService = realService;
    }
    
    @Override
    public Image loadImage(String filename) {
        return cache.computeIfAbsent(filename, realService::loadImage);
    }
}

// Spring AOP Proxy
@Aspect
@Component
public class ImageServiceAspect {
    @Around("execution(* ImageService.loadImage(..))")
    public Object cacheImage(ProceedingJoinPoint joinPoint) throws Throwable {
        String filename = (String) joinPoint.getArgs()[0];
        // Caching logic
        return joinPoint.proceed();
    }
}""",
        "dotnet": """// .NET - Proxy Pattern
public interface IImageService
{
    Image LoadImage(string filename);
}

// Real Subject
public class RealImageService : IImageService
{
    public Image LoadImage(string filename)
    {
        // Expensive operation
        return new Image(filename);
    }
}

// Proxy
public class ImageServiceProxy : IImageService
{
    private readonly IImageService _realService;
    private readonly IMemoryCache _cache;
    
    public ImageServiceProxy(IImageService realService, IMemoryCache cache)
    {
        _realService = realService;
        _cache = cache;
    }
    
    public Image LoadImage(string filename)
    {
        return _cache.GetOrCreate(filename, entry =>
        {
            entry.AbsoluteExpirationRelativeToNow = TimeSpan.FromMinutes(5);
            return _realService.LoadImage(filename);
        });
    }
}

// .NET Core DI
services.AddSingleton<RealImageService>();
services.AddSingleton<IImageService, ImageServiceProxy>();""",
        "nginx": """# Nginx - Proxy Pattern (Reverse Proxy)
# nginx.conf
server {
    listen 80;
    server_name example.com;
    
    location / {
        # Proxy to backend service
        proxy_pass http://backend-servers;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        
        # Proxy features
        proxy_cache my_cache;
        proxy_cache_valid 200 10m;
        proxy_buffering on;
    }
}

upstream backend-servers {
    server backend1:8080;
    server backend2:8080;
    server backend3:8080;
}""",
    },
    "command": {
        "spring": """// Spring Framework - Command Pattern
public interface Command {
    void execute();
    void undo();
}

@Component
public class CreateOrderCommand implements Command {
    private final OrderService orderService;
    private final Order order;
    private Long orderId;
    
    public CreateOrderCommand(OrderService orderService, Order order) {
        this.orderService = orderService;
        this.order = order;
    }
    
    @Override
    public void execute() {
        orderId = orderService.createOrder(order);
    }
    
    @Override
    public void undo() {
        if (orderId != null) {
            orderService.deleteOrder(orderId);
        }
    }
}

// Invoker
@Service
public class CommandInvoker {
    private final Stack<Command> history = new Stack<>();
    
    public void executeCommand(Command command) {
        command.execute();
        history.push(command);
    }
    
    public void undo() {
        if (!history.isEmpty()) {
            Command command = history.pop();
            command.undo();
        }
    }
}""",
        "dotnet": """// .NET - Command Pattern
public interface ICommand
{
    void Execute();
    void Undo();
}

public class CreateOrderCommand : ICommand
{
    private readonly OrderService _orderService;
    private readonly Order _order;
    private long? _orderId;
    
    public CreateOrderCommand(OrderService orderService, Order order)
    {
        _orderService = orderService;
        _order = order;
    }
    
    public void Execute()
    {
        _orderId = _orderService.CreateOrder(_order);
    }
    
    public void Undo()
    {
        if (_orderId.HasValue)
        {
            _orderService.DeleteOrder(_orderId.Value);
        }
    }
}

// Invoker
public class CommandInvoker
{
    private readonly Stack<ICommand> _history = new Stack<ICommand>();
    
    public void ExecuteCommand(ICommand command)
    {
        command.Execute();
        _history.Push(command);
    }
    
    public void Undo()
    {
        if (_history.Count > 0)
        {
            var command = _history.Pop();
            command.Undo();
        }
    }
}""",
    },
    "iterator": {
        "spring": """// Spring Framework - Iterator Pattern
public interface CustomIterator<T> {
    boolean hasNext();
    T next();
}

@Component
public class UserRepository {
    private final List<User> users = new ArrayList<>();
    
    public CustomIterator<User> iterator() {
        return new UserIterator(users);
    }
}

// Custom Iterator
public class UserIterator implements CustomIterator<User> {
    private final List<User> users;
    private int position = 0;
    
    public UserIterator(List<User> users) {
        this.users = users;
    }
    
    @Override
    public boolean hasNext() {
        return position < users.size();
    }
    
    @Override
    public User next() {
        if (!hasNext()) {
            throw new NoSuchElementException();
        }
        return users.get(position++);
    }
}

// Usage
@Service
public class UserService {
    @Autowired
    private UserRepository userRepository;
    
    public void processAllUsers() {
        CustomIterator<User> iterator = userRepository.iterator();
        while (iterator.hasNext()) {
            User user = iterator.next();
            // Process user
        }
    }
}""",
        "dotnet": """// .NET - Iterator Pattern (IEnumerable/IEnumerator)
public class UserCollection : IEnumerable<User>
{
    private readonly List<User> _users = new List<User>();
    
    public void Add(User user)
    {
        _users.Add(user);
    }
    
    public IEnumerator<User> GetEnumerator()
    {
        return new UserIterator(_users);
    }
    
    IEnumerator IEnumerable.GetEnumerator()
    {
        return GetEnumerator();
    }
}

// Iterator
public class UserIterator : IEnumerator<User>
{
    private readonly List<User> _users;
    private int _position = -1;
    
    public UserIterator(List<User> users)
    {
        _users = users;
    }
    
    public User Current => _users[_position];
    
    object IEnumerator.Current => Current;
    
    public bool MoveNext()
    {
        _position++;
        return _position < _users.Count;
    }
    
    public void Reset()
    {
        _position = -1;
    }
    
    public void Dispose() { }
}

// Usage
var users = new UserCollection();
foreach (var user in users)
{
    // Process user
}""",
    },
}


def add_framework_examples_to_readme(readme_path: Path, algorithm_name: str) -> bool:
    """Add comprehensive framework examples to README."""
    try:
        content = readme_path.read_text(encoding="utf-8")

        # Check if already has comprehensive examples
        if (
            "Spring Framework" in content
            and "```java" in content
            and "```csharp" in content
        ):
            return False

        # Get examples
        examples = FRAMEWORK_EXAMPLES_EXPANDED.get(algorithm_name, {})
        if not examples:
            return False

        # Build comprehensive examples section
        examples_section = "\n\n## Examples of Implementation\n\n"
        examples_section += "This pattern/algorithm is implemented in the following frameworks and technologies:\n\n"

        if "spring" in examples:
            examples_section += "### Spring Framework\n\n"
            examples_section += "```java\n" + examples["spring"] + "\n```\n\n"
            examples_section += "**Purpose**: Spring Framework uses this pattern for dependency injection, bean management, and enterprise application development.\n\n"

        if "dotnet" in examples:
            examples_section += "### .NET Framework\n\n"
            examples_section += "```csharp\n" + examples["dotnet"] + "\n```\n\n"
            examples_section += "**Purpose**: .NET Framework implements this pattern for service registration, dependency injection, and application architecture.\n\n"

        if "docker" in examples:
            examples_section += "### Docker\n\n"
            examples_section += "```yaml\n" + examples["docker"] + "\n```\n\n"
            examples_section += "**Purpose**: Docker uses this pattern for container orchestration and service management.\n\n"

        if "kubernetes" in examples:
            examples_section += "### Kubernetes\n\n"
            examples_section += "```yaml\n" + examples["kubernetes"] + "\n```\n\n"
            examples_section += "**Purpose**: Kubernetes implements this pattern for pod management, service discovery, and orchestration.\n\n"

        if "kafka" in examples:
            examples_section += "### Apache Kafka\n\n"
            examples_section += "```python\n" + examples["kafka"] + "\n```\n\n"
            examples_section += "**Purpose**: Kafka uses this pattern for event streaming, pub/sub messaging, and distributed systems.\n\n"

        if "nginx" in examples:
            examples_section += "### Nginx\n\n"
            examples_section += "```nginx\n" + examples["nginx"] + "\n```\n\n"
            examples_section += "**Purpose**: Nginx implements this pattern for reverse proxying, load balancing, and request routing.\n\n"

        # Insert before References or at end
        if "## References" in content:
            content = content.replace(
                "## References", examples_section + "\n## References"
            )
        elif "## Examples of Implementation" in content:
            # Replace existing section
            pattern = r"## Examples of Implementation.*?(?=\n## |$)"
            content = re.sub(
                pattern, examples_section.strip(), content, flags=re.DOTALL
            )
        else:
            content = content.rstrip() + "\n\n" + examples_section

        readme_path.write_text(content, encoding="utf-8")
        return True
    except Exception as e:
        print(f"Error processing {readme_path}: {e}")
        return False


def main():
    """Add framework examples to all relevant algorithms."""
    updated = 0

    # Process all patterns with examples
    for algo_name in FRAMEWORK_EXAMPLES_EXPANDED.keys():
        for readme_path in ROOT.rglob(f"*/{algo_name}/README.md"):
            if add_framework_examples_to_readme(readme_path, algo_name):
                updated += 1
                print(
                    f"[OK] Added framework examples to {readme_path.relative_to(ROOT)}"
                )

    # Also check for variations
    pattern_variations = {
        "abstract_factory": "factory",
        "factory_method": "factory",
        "observer_pattern": "observer",
        "strategy_pattern": "strategy",
        "adapter_pattern": "adapter",
        "decorator_pattern": "decorator",
        "proxy_pattern": "proxy",
        "command_pattern": "command",
        "iterator_pattern": "iterator",
    }

    for pattern_name, example_key in pattern_variations.items():
        for readme_path in ROOT.rglob(f"*/{pattern_name}/README.md"):
            if add_framework_examples_to_readme(readme_path, example_key):
                updated += 1
                print(
                    f"[OK] Added framework examples to {readme_path.relative_to(ROOT)}"
                )

    print(f"\n[COMPLETE] Added framework examples to {updated} algorithms")


if __name__ == "__main__":
    main()
