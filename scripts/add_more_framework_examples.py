#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Add framework examples for remaining design patterns.
Expands coverage to all major patterns.
"""

import re
from pathlib import Path
from typing import Dict, Optional

ROOT = Path(__file__).resolve().parents[1]

# Additional framework examples for remaining patterns
ADDITIONAL_FRAMEWORK_EXAMPLES = {
    'composite': {
        'spring': '''// Spring Framework - Composite Pattern
public interface Component {
    void operation();
    void add(Component component);
    void remove(Component component);
}

@Component
public class Leaf implements Component {
    private String name;
    
    public Leaf(String name) {
        this.name = name;
    }
    
    @Override
    public void operation() {
        System.out.println("Leaf: " + name);
    }
    
    @Override
    public void add(Component component) {
        throw new UnsupportedOperationException();
    }
    
    @Override
    public void remove(Component component) {
        throw new UnsupportedOperationException();
    }
}

@Component
public class Composite implements Component {
    private List<Component> children = new ArrayList<>();
    private String name;
    
    public Composite(String name) {
        this.name = name;
    }
    
    @Override
    public void operation() {
        System.out.println("Composite: " + name);
        for (Component child : children) {
            child.operation();
        }
    }
    
    @Override
    public void add(Component component) {
        children.add(component);
    }
    
    @Override
    public void remove(Component component) {
        children.remove(component);
    }
}''',
        'dotnet': '''// .NET - Composite Pattern
public interface IComponent
{
    void Operation();
    void Add(IComponent component);
    void Remove(IComponent component);
}

public class Leaf : IComponent
{
    private readonly string _name;
    
    public Leaf(string name)
    {
        _name = name;
    }
    
    public void Operation()
    {
        Console.WriteLine($"Leaf: {_name}");
    }
    
    public void Add(IComponent component)
    {
        throw new NotSupportedException();
    }
    
    public void Remove(IComponent component)
    {
        throw new NotSupportedException();
    }
}

public class Composite : IComponent
{
    private readonly List<IComponent> _children = new List<IComponent>();
    private readonly string _name;
    
    public Composite(string name)
    {
        _name = name;
    }
    
    public void Operation()
    {
        Console.WriteLine($"Composite: {_name}");
        foreach (var child in _children)
        {
            child.Operation();
        }
    }
    
    public void Add(IComponent component)
    {
        _children.Add(component);
    }
    
    public void Remove(IComponent component)
    {
        _children.Remove(component);
    }
}'''
    },
    
    'facade': {
        'spring': '''// Spring Framework - Facade Pattern
@Service
public class OrderFacade {
    @Autowired
    private InventoryService inventoryService;
    
    @Autowired
    private PaymentService paymentService;
    
    @Autowired
    private ShippingService shippingService;
    
    @Autowired
    private NotificationService notificationService;
    
    public OrderResult processOrder(Order order) {
        // Facade simplifies complex subsystem interactions
        // 1. Check inventory
        if (!inventoryService.checkAvailability(order.getItems())) {
            return OrderResult.failure("Items not available");
        }
        
        // 2. Process payment
        PaymentResult payment = paymentService.processPayment(order.getPayment());
        if (!payment.isSuccess()) {
            return OrderResult.failure("Payment failed");
        }
        
        // 3. Reserve inventory
        inventoryService.reserveItems(order.getItems());
        
        // 4. Create shipment
        Shipment shipment = shippingService.createShipment(order);
        
        // 5. Send notifications
        notificationService.sendOrderConfirmation(order);
        
        return OrderResult.success(shipment);
    }
}''',
        'dotnet': '''// .NET - Facade Pattern
public class OrderFacade
{
    private readonly IInventoryService _inventoryService;
    private readonly IPaymentService _paymentService;
    private readonly IShippingService _shippingService;
    private readonly INotificationService _notificationService;
    
    public OrderFacade(
        IInventoryService inventoryService,
        IPaymentService paymentService,
        IShippingService shippingService,
        INotificationService notificationService)
    {
        _inventoryService = inventoryService;
        _paymentService = paymentService;
        _shippingService = shippingService;
        _notificationService = notificationService;
    }
    
    public OrderResult ProcessOrder(Order order)
    {
        // Facade simplifies complex subsystem
        if (!_inventoryService.CheckAvailability(order.Items))
        {
            return OrderResult.Failure("Items not available");
        }
        
        var payment = _paymentService.ProcessPayment(order.Payment);
        if (!payment.IsSuccess)
        {
            return OrderResult.Failure("Payment failed");
        }
        
        _inventoryService.ReserveItems(order.Items);
        var shipment = _shippingService.CreateShipment(order);
        _notificationService.SendOrderConfirmation(order);
        
        return OrderResult.Success(shipment);
    }
}'''
    },
    
    'template_method': {
        'spring': '''// Spring Framework - Template Method Pattern
public abstract class DataProcessor {
    // Template method
    public final void process(Data data) {
        validate(data);
        Data transformed = transform(data);
        save(transformed);
        notify(transformed);
    }
    
    protected abstract void validate(Data data);
    protected abstract Data transform(Data data);
    
    protected void save(Data data) {
        // Default implementation
        repository.save(data);
    }
    
    protected void notify(Data data) {
        // Default implementation
        notificationService.send(data);
    }
}

@Component
public class CSVDataProcessor extends DataProcessor {
    @Override
    protected void validate(Data data) {
        // CSV-specific validation
    }
    
    @Override
    protected Data transform(Data data) {
        // CSV-specific transformation
        return csvParser.parse(data);
    }
}

@Component
public class JSONDataProcessor extends DataProcessor {
    @Override
    protected void validate(Data data) {
        // JSON-specific validation
    }
    
    @Override
    protected Data transform(Data data) {
        // JSON-specific transformation
        return jsonParser.parse(data);
    }
}''',
        'dotnet': '''// .NET - Template Method Pattern
public abstract class DataProcessor
{
    // Template method
    public void Process(Data data)
    {
        Validate(data);
        var transformed = Transform(data);
        Save(transformed);
        Notify(transformed);
    }
    
    protected abstract void Validate(Data data);
    protected abstract Data Transform(Data data);
    
    protected virtual void Save(Data data)
    {
        _repository.Save(data);
    }
    
    protected virtual void Notify(Data data)
    {
        _notificationService.Send(data);
    }
}

public class CsvDataProcessor : DataProcessor
{
    protected override void Validate(Data data)
    {
        // CSV validation
    }
    
    protected override Data Transform(Data data)
    {
        return _csvParser.Parse(data);
    }
}

public class JsonDataProcessor : DataProcessor
{
    protected override void Validate(Data data)
    {
        // JSON validation
    }
    
    protected override Data Transform(Data data)
    {
        return _jsonParser.Parse(data);
    }
}'''
    },
    
    'chain_of_responsibility': {
        'spring': '''// Spring Framework - Chain of Responsibility Pattern
public abstract class Handler {
    protected Handler next;
    
    public Handler setNext(Handler next) {
        this.next = next;
        return next;
    }
    
    public abstract boolean handle(Request request);
    
    protected boolean handleNext(Request request) {
        if (next == null) {
            return true;
        }
        return next.handle(request);
    }
}

@Component
public class AuthenticationHandler extends Handler {
    @Override
    public boolean handle(Request request) {
        if (!isAuthenticated(request)) {
            return false;
        }
        return handleNext(request);
    }
    
    private boolean isAuthenticated(Request request) {
        // Authentication logic
        return request.getToken() != null;
    }
}

@Component
public class AuthorizationHandler extends Handler {
    @Override
    public boolean handle(Request request) {
        if (!isAuthorized(request)) {
            return false;
        }
        return handleNext(request);
    }
    
    private boolean isAuthorized(Request request) {
        // Authorization logic
        return request.getUser().hasPermission(request.getResource());
    }
}

@Component
public class ValidationHandler extends Handler {
    @Override
    public boolean handle(Request request) {
        if (!isValid(request)) {
            return false;
        }
        return handleNext(request);
    }
    
    private boolean isValid(Request request) {
        // Validation logic
        return request.getData() != null;
    }
}

// Usage
@Autowired
private AuthenticationHandler authHandler;
@Autowired
private AuthorizationHandler authzHandler;
@Autowired
private ValidationHandler validationHandler;

// Build chain
authHandler.setNext(authzHandler).setNext(validationHandler);
authHandler.handle(request);''',
        'dotnet': '''// .NET - Chain of Responsibility Pattern
public abstract class Handler
{
    protected Handler _next;
    
    public Handler SetNext(Handler next)
    {
        _next = next;
        return next;
    }
    
    public abstract bool Handle(Request request);
    
    protected bool HandleNext(Request request)
    {
        if (_next == null)
        {
            return true;
        }
        return _next.Handle(request);
    }
}

public class AuthenticationHandler : Handler
{
    public override bool Handle(Request request)
    {
        if (!IsAuthenticated(request))
        {
            return false;
        }
        return HandleNext(request);
    }
    
    private bool IsAuthenticated(Request request)
    {
        return request.Token != null;
    }
}

// Usage
var authHandler = new AuthenticationHandler();
var authzHandler = new AuthorizationHandler();
var validationHandler = new ValidationHandler();

authHandler.SetNext(authzHandler).SetNext(validationHandler);
authHandler.Handle(request);'''
    },
    
    'bridge': {
        'spring': '''// Spring Framework - Bridge Pattern
public interface Renderer {
    void renderCircle(float radius);
    void renderSquare(float side);
}

@Component("vectorRenderer")
public class VectorRenderer implements Renderer {
    @Override
    public void renderCircle(float radius) {
        System.out.println("Drawing circle with radius " + radius + " using vectors");
    }
    
    @Override
    public void renderSquare(float side) {
        System.out.println("Drawing square with side " + side + " using vectors");
    }
}

@Component("rasterRenderer")
public class RasterRenderer implements Renderer {
    @Override
    public void renderCircle(float radius) {
        System.out.println("Drawing circle with radius " + radius + " using pixels");
    }
    
    @Override
    public void renderSquare(float side) {
        System.out.println("Drawing square with side " + side + " using pixels");
    }
}

public abstract class Shape {
    protected Renderer renderer;
    
    public Shape(Renderer renderer) {
        this.renderer = renderer;
    }
    
    public abstract void draw();
}

@Component
public class Circle extends Shape {
    private float radius;
    
    @Autowired
    public Circle(@Qualifier("vectorRenderer") Renderer renderer) {
        super(renderer);
    }
    
    @Override
    public void draw() {
        renderer.renderCircle(radius);
    }
}''',
        'dotnet': '''// .NET - Bridge Pattern
public interface IRenderer
{
    void RenderCircle(float radius);
    void RenderSquare(float side);
}

public class VectorRenderer : IRenderer
{
    public void RenderCircle(float radius)
    {
        Console.WriteLine($"Drawing circle with radius {radius} using vectors");
    }
    
    public void RenderSquare(float side)
    {
        Console.WriteLine($"Drawing square with side {side} using vectors");
    }
}

public abstract class Shape
{
    protected IRenderer Renderer;
    
    protected Shape(IRenderer renderer)
    {
        Renderer = renderer;
    }
    
    public abstract void Draw();
}

public class Circle : Shape
{
    private readonly float _radius;
    
    public Circle(IRenderer renderer, float radius) : base(renderer)
    {
        _radius = radius;
    }
    
    public override void Draw()
    {
        Renderer.RenderCircle(_radius);
    }
}'''
    },
    
    'memento': {
        'spring': '''// Spring Framework - Memento Pattern
public class Memento {
    private final String state;
    
    public Memento(String state) {
        this.state = state;
    }
    
    public String getState() {
        return state;
    }
}

@Component
public class Originator {
    private String state;
    
    public void setState(String state) {
        this.state = state;
    }
    
    public String getState() {
        return state;
    }
    
    public Memento saveStateToMemento() {
        return new Memento(state);
    }
    
    public void getStateFromMemento(Memento memento) {
        state = memento.getState();
    }
}

@Service
public class Caretaker {
    private List<Memento> mementoList = new ArrayList<>();
    
    public void add(Memento memento) {
        mementoList.add(memento);
    }
    
    public Memento get(int index) {
        return mementoList.get(index);
    }
}''',
        'dotnet': '''// .NET - Memento Pattern
public class Memento
{
    public string State { get; }
    
    public Memento(string state)
    {
        State = state;
    }
}

public class Originator
{
    private string _state;
    
    public void SetState(string state)
    {
        _state = state;
    }
    
    public string GetState()
    {
        return _state;
    }
    
    public Memento SaveStateToMemento()
    {
        return new Memento(_state);
    }
    
    public void GetStateFromMemento(Memento memento)
    {
        _state = memento.State;
    }
}

public class Caretaker
{
    private readonly List<Memento> _mementoList = new List<Memento>();
    
    public void Add(Memento memento)
    {
        _mementoList.Add(memento);
    }
    
    public Memento Get(int index)
    {
        return _mementoList[index];
    }
}'''
    },
    
    'state': {
        'spring': '''// Spring Framework - State Pattern
public interface State {
    void handle(Context context);
}

@Component("concreteStateA")
public class ConcreteStateA implements State {
    @Override
    public void handle(Context context) {
        System.out.println("Handling in State A");
        context.setState(context.getStateB());
    }
}

@Component("concreteStateB")
public class ConcreteStateB implements State {
    @Override
    public void handle(Context context) {
        System.out.println("Handling in State B");
        context.setState(context.getStateA());
    }
}

@Component
public class Context {
    @Autowired
    @Qualifier("concreteStateA")
    private State stateA;
    
    @Autowired
    @Qualifier("concreteStateB")
    private State stateB;
    
    private State currentState;
    
    @PostConstruct
    public void init() {
        currentState = stateA;
    }
    
    public void setState(State state) {
        this.currentState = state;
    }
    
    public void request() {
        currentState.handle(this);
    }
    
    public State getStateA() { return stateA; }
    public State getStateB() { return stateB; }
}''',
        'dotnet': '''// .NET - State Pattern
public interface IState
{
    void Handle(Context context);
}

public class ConcreteStateA : IState
{
    public void Handle(Context context)
    {
        Console.WriteLine("Handling in State A");
        context.State = new ConcreteStateB();
    }
}

public class ConcreteStateB : IState
{
    public void Handle(Context context)
    {
        Console.WriteLine("Handling in State B");
        context.State = new ConcreteStateA();
    }
}

public class Context
{
    public IState State { get; set; }
    
    public Context(IState state)
    {
        State = state;
    }
    
    public void Request()
    {
        State.Handle(this);
    }
}'''
    },
    
    'visitor': {
        'spring': '''// Spring Framework - Visitor Pattern
public interface Element {
    void accept(Visitor visitor);
}

public interface Visitor {
    void visit(ConcreteElementA element);
    void visit(ConcreteElementB element);
}

@Component
public class ConcreteElementA implements Element {
    @Override
    public void accept(Visitor visitor) {
        visitor.visit(this);
    }
    
    public String operationA() {
        return "ConcreteElementA";
    }
}

@Component
public class ConcreteElementB implements Element {
    @Override
    public void accept(Visitor visitor) {
        visitor.visit(this);
    }
    
    public String operationB() {
        return "ConcreteElementB";
    }
}

@Component
public class ConcreteVisitor implements Visitor {
    @Override
    public void visit(ConcreteElementA element) {
        System.out.println("Visiting " + element.operationA());
    }
    
    @Override
    public void visit(ConcreteElementB element) {
        System.out.println("Visiting " + element.operationB());
    }
}''',
        'dotnet': '''// .NET - Visitor Pattern
public interface IElement
{
    void Accept(IVisitor visitor);
}

public interface IVisitor
{
    void Visit(ConcreteElementA element);
    void Visit(ConcreteElementB element);
}

public class ConcreteElementA : IElement
{
    public void Accept(IVisitor visitor)
    {
        visitor.Visit(this);
    }
    
    public string OperationA()
    {
        return "ConcreteElementA";
    }
}

public class ConcreteVisitor : IVisitor
{
    public void Visit(ConcreteElementA element)
    {
        Console.WriteLine($"Visiting {element.OperationA()}");
    }
    
    public void Visit(ConcreteElementB element)
    {
        Console.WriteLine($"Visiting {element.OperationB()}");
    }
}'''
    }
}

def add_framework_examples_to_readme(readme_path: Path, algorithm_name: str) -> bool:
    """Add framework examples to README."""
    try:
        content = readme_path.read_text(encoding='utf-8')
        
        # Check if already has comprehensive examples
        if "Spring Framework" in content and "```java" in content and "```csharp" in content:
            return False
        
        # Get examples
        examples = ADDITIONAL_FRAMEWORK_EXAMPLES.get(algorithm_name, {})
        if not examples:
            return False
        
        # Build examples section
        examples_section = "\n\n## Examples of Implementation\n\n"
        examples_section += "This pattern is implemented in the following frameworks and technologies:\n\n"
        
        if 'spring' in examples:
            examples_section += "### Spring Framework\n\n"
            examples_section += "```java\n" + examples['spring'] + "\n```\n\n"
            examples_section += "**Purpose**: Spring Framework uses this pattern for dependency injection, bean management, and enterprise application development.\n\n"
        
        if 'dotnet' in examples:
            examples_section += "### .NET Framework\n\n"
            examples_section += "```csharp\n" + examples['dotnet'] + "\n```\n\n"
            examples_section += "**Purpose**: .NET Framework implements this pattern for service registration, dependency injection, and application architecture.\n\n"
        
        # Insert before References or at end
        if "## References" in content:
            content = content.replace("## References", examples_section + "\n## References")
        elif "## Examples of Implementation" in content:
            # Replace existing section
            pattern = r"## Examples of Implementation.*?(?=\n## |$)"
            content = re.sub(pattern, examples_section.strip(), content, flags=re.DOTALL)
        else:
            content = content.rstrip() + "\n\n" + examples_section
        
        readme_path.write_text(content, encoding='utf-8')
        return True
    except Exception as e:
        print(f"Error processing {readme_path}: {e}")
        return False

def main():
    """Add framework examples to remaining patterns."""
    updated = 0
    
    for algo_name in ADDITIONAL_FRAMEWORK_EXAMPLES.keys():
        for readme_path in ROOT.rglob(f"*/{algo_name}/README.md"):
            if add_framework_examples_to_readme(readme_path, algo_name):
                updated += 1
                print(f"[OK] Added framework examples to {readme_path.relative_to(ROOT)}")
    
    # Check for variations
    variations = {
        'composite_pattern': 'composite',
        'facade_pattern': 'facade',
        'template_method_pattern': 'template_method',
        'chain_of_responsibility_pattern': 'chain_of_responsibility',
        'bridge_pattern': 'bridge',
        'memento_pattern': 'memento',
        'state_pattern': 'state',
        'visitor_pattern': 'visitor',
    }
    
    for pattern_name, example_key in variations.items():
        for readme_path in ROOT.rglob(f"*/{pattern_name}/README.md"):
            if add_framework_examples_to_readme(readme_path, example_key):
                updated += 1
                print(f"[OK] Added framework examples to {readme_path.relative_to(ROOT)}")
    
    print(f"\n[COMPLETE] Added framework examples to {updated} patterns")

if __name__ == "__main__":
    main()

