#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Add framework examples (Spring, .NET, Docker, Kubernetes) to algorithm READMEs.
"""

import re
from pathlib import Path
from typing import Dict, Optional

ROOT = Path(__file__).resolve().parents[1]

# Framework examples by algorithm category
FRAMEWORK_EXAMPLES = {
    'singleton': {
        'spring': '''// Spring Framework - Singleton Bean
@Component
@Scope("singleton")  // Default scope
public class DatabaseConnection {
    private static DatabaseConnection instance;
    
    @PostConstruct
    public void init() {
        instance = this;
    }
    
    public static DatabaseConnection getInstance() {
        return instance;
    }
}

// Usage in Spring
@Autowired
private DatabaseConnection dbConnection;''',
        'dotnet': '''// .NET - Singleton Service
public class DatabaseConnection
{
    private static DatabaseConnection _instance;
    private static readonly object _lock = new object();
    
    private DatabaseConnection() { }
    
    public static DatabaseConnection GetInstance()
    {
        if (_instance == null)
        {
            lock (_lock)
            {
                if (_instance == null)
                {
                    _instance = new DatabaseConnection();
                }
            }
        }
        return _instance;
    }
}

// .NET Core DI
services.AddSingleton<DatabaseConnection>();''',
        'docker': '''# Docker - Single Container Instance
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
      replicas: 1'''
    },
    
    'factory': {
        'spring': '''// Spring Framework - Factory Pattern
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

// Usage
@Autowired
private PaymentProcessorFactory factory;

PaymentProcessor processor = factory.getProcessor("credit_card");''',
        'dotnet': '''// .NET - Factory Pattern
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
            _ => throw new ArgumentException("Unknown type")
        };
    }
}

// .NET Core DI
services.AddTransient<PaymentProcessorFactory>();''',
        'kubernetes': '''# Kubernetes - Factory Pattern for Pod Creation
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
  template:
    spec:
      containers:
      - name: processor
        image: payment-processor:latest
        env:
        - name: PROCESSOR_TYPE
          valueFrom:
            configMapKeyRef:
              name: processor-config
              key: processor-type'''
    },
    
    'observer': {
        'spring': '''// Spring Framework - Observer Pattern (Event Listener)
@Component
public class OrderService {
    
    @Autowired
    private ApplicationEventPublisher eventPublisher;
    
    public void createOrder(Order order) {
        // Create order logic
        eventPublisher.publishEvent(new OrderCreatedEvent(order));
    }
}

@Component
public class EmailNotificationListener {
    
    @EventListener
    public void handleOrderCreated(OrderCreatedEvent event) {
        // Send email notification
        System.out.println("Sending email for order: " + event.getOrder().getId());
    }
}''',
        'dotnet': '''// .NET - Observer Pattern (Events)
public class OrderService
{
    public event EventHandler<OrderCreatedEventArgs> OrderCreated;
    
    public void CreateOrder(Order order)
    {
        // Create order logic
        OnOrderCreated(new OrderCreatedEventArgs(order));
    }
    
    protected virtual void OnOrderCreated(OrderCreatedEventArgs e)
    {
        OrderCreated?.Invoke(this, e);
    }
}

public class EmailNotificationService
{
    public void Subscribe(OrderService orderService)
    {
        orderService.OrderCreated += HandleOrderCreated;
    }
    
    private void HandleOrderCreated(object sender, OrderCreatedEventArgs e)
    {
        Console.WriteLine($"Sending email for order: {e.Order.Id}");
    }
}''',
        'kafka': '''# Apache Kafka - Observer Pattern (Pub/Sub)
# Producer
from kafka import KafkaProducer

producer = KafkaProducer(bootstrap_servers='localhost:9092')
producer.send('order-events', key=b'order-123', value=b'{"orderId": "123", "status": "created"}')

# Consumer 1 - Email Service
from kafka import KafkaConsumer

consumer = KafkaConsumer('order-events', bootstrap_servers='localhost:9092')
for message in consumer:
    order_data = json.loads(message.value)
    send_email_notification(order_data)

# Consumer 2 - Inventory Service
consumer2 = KafkaConsumer('order-events', bootstrap_servers='localhost:9092')
for message in consumer2:
    order_data = json.loads(message.value)
    update_inventory(order_data)'''
    },
    
    'caching': {
        'spring': '''// Spring Framework - Caching
@Service
public class ProductService {
    
    @Cacheable(value = "products", key = "#id")
    public Product getProduct(Long id) {
        // Expensive database call
        return productRepository.findById(id);
    }
    
    @CacheEvict(value = "products", key = "#product.id")
    public void updateProduct(Product product) {
        productRepository.save(product);
    }
}

// Configuration
@EnableCaching
@Configuration
public class CacheConfig {
    @Bean
    public CacheManager cacheManager() {
        return new ConcurrentMapCacheManager("products");
    }
}''',
        'dotnet': '''// .NET - Caching
public class ProductService
{
    private readonly IMemoryCache _cache;
    
    public ProductService(IMemoryCache cache)
    {
        _cache = cache;
    }
    
    public Product GetProduct(int id)
    {
        return _cache.GetOrCreate($"product-{id}", entry =>
        {
            entry.AbsoluteExpirationRelativeToNow = TimeSpan.FromMinutes(5);
            return _productRepository.GetById(id);
        });
    }
}

// Startup.cs
services.AddMemoryCache();
services.AddScoped<ProductService>();''',
        'redis': '''# Redis - Distributed Caching
import redis
import json

r = redis.Redis(host='localhost', port=6379, db=0)

def get_product(product_id):
    # Try cache first
    cached = r.get(f"product:{product_id}")
    if cached:
        return json.loads(cached)
    
    # Fetch from database
    product = db.get_product(product_id)
    
    # Cache for 5 minutes
    r.setex(f"product:{product_id}", 300, json.dumps(product))
    return product'''
    },
    
    'load_balancing': {
        'nginx': '''# Nginx - Load Balancing
upstream backend {
    least_conn;  # Load balancing algorithm
    server backend1.example.com;
    server backend2.example.com;
    server backend3.example.com;
}

server {
    listen 80;
    
    location / {
        proxy_pass http://backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}''',
        'kubernetes': '''# Kubernetes - Load Balancing (Service)
apiVersion: v1
kind: Service
metadata:
  name: backend-service
spec:
  selector:
    app: backend
  ports:
  - port: 80
    targetPort: 8080
  type: LoadBalancer
  # Kubernetes automatically load balances across pods
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: backend
spec:
  replicas: 3  # 3 instances for load balancing
  selector:
    matchLabels:
      app: backend
  template:
    metadata:
      labels:
        app: backend
    spec:
      containers:
      - name: backend
        image: backend:latest
        ports:
        - containerPort: 8080''',
        'docker': '''# Docker Swarm - Load Balancing
docker service create \\
  --name backend \\
  --replicas 3 \\
  --publish 80:8080 \\
  backend:latest

# Docker Swarm automatically load balances across replicas
# Access via: http://localhost (load balanced across 3 containers)'''
    }
}

def add_framework_examples_to_readme(readme_path: Path, algorithm_name: str) -> bool:
    """Add framework examples to README."""
    try:
        content = readme_path.read_text(encoding='utf-8')
        
        # Check if examples section exists (try different variations)
        has_examples_section = (
            "## Examples of Implementation" in content or
            "## Examples" in content or
            "### Examples" in content
        )
        
        if not has_examples_section:
            # Add examples section before References or at end
            examples_section = "\n\n## Examples of Implementation\n\n"
            if "## References" in content:
                content = content.replace("## References", examples_section + "## References")
            else:
                content = content.rstrip() + examples_section
        
        # Check if already has framework examples
        if "Spring Framework" in content and "```java" in content:
            return False
        
        # Get examples for this algorithm (try exact match, then partial)
        examples = FRAMEWORK_EXAMPLES.get(algorithm_name, {})
        if not examples:
            # Try partial match
            for key, ex in FRAMEWORK_EXAMPLES.items():
                if key in algorithm_name or algorithm_name in key:
                    examples = ex
                    break
        
        if not examples:
            return False
        
        # Build examples section
        examples_section = "\n\n### Spring Framework\n\n"
        if 'spring' in examples:
            examples_section += "```java\n" + examples['spring'] + "\n```\n\n"
            examples_section += "**Purpose**: Spring Framework uses this pattern for dependency injection, bean management, and enterprise application development.\n\n"
        
        examples_section += "### .NET Framework\n\n"
        if 'dotnet' in examples:
            examples_section += "```csharp\n" + examples['dotnet'] + "\n```\n\n"
            examples_section += "**Purpose**: .NET Framework implements this pattern for service registration, dependency injection, and application architecture.\n\n"
        
        if 'docker' in examples:
            examples_section += "### Docker\n\n"
            examples_section += "```yaml\n" + examples['docker'] + "\n```\n\n"
            examples_section += "**Purpose**: Docker uses this pattern for container orchestration and service management.\n\n"
        
        if 'kubernetes' in examples:
            examples_section += "### Kubernetes\n\n"
            examples_section += "```yaml\n" + examples['kubernetes'] + "\n```\n\n"
            examples_section += "**Purpose**: Kubernetes implements this pattern for pod management, service discovery, and orchestration.\n\n"
        
        if 'kafka' in examples:
            examples_section += "### Apache Kafka\n\n"
            examples_section += "```python\n" + examples['kafka'] + "\n```\n\n"
            examples_section += "**Purpose**: Kafka uses this pattern for event streaming, pub/sub messaging, and distributed systems.\n\n"
        
        # Insert before "## References" or at end
        if "## References" in content:
            content = content.replace("## References", examples_section + "\n## References")
        else:
            content = content.rstrip() + "\n\n" + examples_section
        
        readme_path.write_text(content, encoding='utf-8')
        return True
    except Exception as e:
        print(f"Error processing {readme_path}: {e}")
        return False

def main():
    """Add framework examples to all relevant algorithms."""
    updated = 0
    
    # Process algorithms that have framework examples
    for algo_name in FRAMEWORK_EXAMPLES.keys():
        for readme_path in ROOT.rglob(f"*/{algo_name}/README.md"):
            if add_framework_examples_to_readme(readme_path, algo_name):
                updated += 1
                print(f"[OK] Added framework examples to {readme_path.relative_to(ROOT)}")
    
    # Also add to common patterns and algorithms
    common_patterns = {
        'caching': 'caching',
        'load_balancing': 'load_balancing',
        'rate_limiting': 'rate_limiting',
        'circuit_breaker': 'circuit_breaker',
        'retry_pattern': 'retry_pattern',
        'blue_green': 'blue_green',
        'canary': 'canary',
        'observer': 'observer',
        'factory': 'factory',
        'abstract_factory': 'factory',
        'strategy': 'strategy',
        'adapter': 'adapter',
        'decorator': 'decorator',
        'proxy': 'proxy',
        'command': 'command',
        'iterator': 'iterator',
    }
    
    for pattern_name, example_key in common_patterns.items():
        for readme_path in ROOT.rglob(f"*/{pattern_name}/README.md"):
            if add_framework_examples_to_readme(readme_path, example_key):
                updated += 1
                print(f"[OK] Added framework examples to {readme_path.relative_to(ROOT)}")
    
    print(f"\n[COMPLETE] Added framework examples to {updated} algorithms")

if __name__ == "__main__":
    main()

