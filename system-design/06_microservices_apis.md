# Microservices & APIs

Microservices architecture breaks down a monolithic application into small, independent services. Each service handles a specific business capability and can be developed, deployed, and scaled independently.

---

## 🏗️ Monolithic vs Microservices

### Monolithic Architecture

```
┌─────────────────────────────────────┐
│      Monolithic Application         │
│  ┌──────────────────────────────┐   │
│  │      User Interface (UI)     │   │
│  └──────────────┬───────────────┘   │
│                 │                    │
│  ┌──────────────▼───────────────┐   │
│  │    Business Logic Layer      │   │
│  │  • User Service              │   │
│  │  • Product Service           │   │
│  │  • Order Service             │   │
│  │  • Payment Service           │   │
│  └──────────────┬───────────────┘   │
│                 │                    │
│  ┌──────────────▼───────────────┐   │
│  │    Single Database           │   │
│  └──────────────────────────────┘   │
└─────────────────────────────────────┘
```

**Advantages:**
- ✅ Simple to develop initially
- ✅ Easy to test (everything in one place)
- ✅ Easy to deploy (single artifact)
- ✅ No network overhead

**Disadvantages:**
- ❌ Tight coupling (changes affect everything)
- ❌ Difficult to scale (must scale entire app)
- ❌ Technology lock-in (one language/framework)
- ❌ Long deployment times (whole app)
- ❌ Hard to understand as it grows

### Microservices Architecture

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   User      │     │  Product    │     │   Order     │
│  Service    │     │  Service    │     │  Service    │
│             │     │             │     │             │
│ ┌─────────┐ │     │ ┌─────────┐ │     │ ┌─────────┐ │
│ │   DB    │ │     │ │   DB    │ │     │ │   DB    │ │
│ └─────────┘ │     │ └─────────┘ │     │ └─────────┘ │
└──────┬──────┘     └──────┬──────┘     └──────┬──────┘
       │                   │                   │
       └───────────┬───────┴───────────┬───────┘
                   │                   │
              ┌────▼────────────────────▼─────┐
              │     API Gateway / BFF         │
              └───────────────────────────────┘
```

**Advantages:**
- ✅ Independent development & deployment
- ✅ Technology diversity (use best tool for each service)
- ✅ Fault isolation (one service failure doesn't crash all)
- ✅ Scalability (scale services independently)
- ✅ Easier to understand (small codebases)

**Disadvantages:**
- ❌ Distributed complexity
- ❌ Network latency
- ❌ Data consistency challenges
- ❌ Testing complexity
- ❌ Deployment complexity

---

## 🔗 Service Communication

### 1. Synchronous Communication (REST/gRPC)

**REST API (JSON over HTTP)**

```python
# User Service
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    user = db.get_user(user_id)
    return jsonify({
        'id': user.id,
        'name': user.name,
        'email': user.email
    })

# Order Service calling User Service
import requests

def create_order(user_id, items):
    # Sync call to User Service
    response = requests.get(f'http://user-service/users/{user_id}')
    
    if response.status_code == 404:
        raise ValueError("User not found")
    
    user = response.json()
    
    # Create order
    order = Order(user_id=user_id, items=items)
    db.save(order)
    
    return order
```

**REST Best Practices:**

```python
# ✅ Good: RESTful resource-based URLs
GET    /api/v1/users             # List users
GET    /api/v1/users/123         # Get user
POST   /api/v1/users             # Create user
PUT    /api/v1/users/123         # Update user
DELETE /api/v1/users/123         # Delete user

# ✅ Good: Nested resources
GET    /api/v1/users/123/orders  # Get user's orders

# ❌ Bad: Action-based URLs
GET    /api/v1/getUser?id=123
POST   /api/v1/createUser
```

**HTTP Status Codes:**
```
2xx Success
  200 OK - Request succeeded
  201 Created - Resource created
  204 No Content - Request succeeded, no body

4xx Client Errors
  400 Bad Request - Invalid input
  401 Unauthorized - Not authenticated
  403 Forbidden - Not authorized
  404 Not Found - Resource doesn't exist
  409 Conflict - Resource conflict (duplicate)
  429 Too Many Requests - Rate limited

5xx Server Errors
  500 Internal Server Error - Server error
  503 Service Unavailable - Server down/overloaded
```

**gRPC (Protocol Buffers)**

```protobuf
// user.proto
syntax = "proto3";

service UserService {
  rpc GetUser (GetUserRequest) returns (User);
  rpc CreateUser (CreateUserRequest) returns (User);
}

message GetUserRequest {
  int64 user_id = 1;
}

message User {
  int64 id = 1;
  string name = 2;
  string email = 3;
}
```

```python
# gRPC Server
import grpc
from concurrent import futures
import user_pb2_grpc

class UserService(user_pb2_grpc.UserServiceServicer):
    def GetUser(self, request, context):
        user = db.get_user(request.user_id)
        return user_pb2.User(
            id=user.id,
            name=user.name,
            email=user.email
        )

# Start server
server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
user_pb2_grpc.add_UserServiceServicer_to_server(UserService(), server)
server.add_insecure_port('[::]:50051')
server.start()

# gRPC Client
channel = grpc.insecure_channel('localhost:50051')
stub = user_pb2_grpc.UserServiceStub(channel)
user = stub.GetUser(user_pb2.GetUserRequest(user_id=123))
```

**REST vs gRPC:**

| Feature | REST | gRPC |
|---------|------|------|
| Protocol | HTTP/1.1 | HTTP/2 |
| Data Format | JSON/XML | Protocol Buffers (binary) |
| Performance | Slower (text parsing) | Faster (binary, HTTP/2) |
| Browser Support | ✅ Yes | ❌ Limited |
| Streaming | ❌ No | ✅ Yes (bidirectional) |
| Code Generation | Manual | Auto-generated |
| Human Readable | ✅ Yes | ❌ Binary |
| Use Case | Public APIs, CRUD | Internal services, high perf |

### 2. Asynchronous Communication (Message Queues)

**Message Queue Architecture:**

```
┌──────────────┐      ┌──────────────┐      ┌──────────────┐
│   Producer   │─────▶│ Message Queue│─────▶│   Consumer   │
│  (Service A) │      │ (Kafka/RabbitMQ)    │  (Service B) │
└──────────────┘      └──────────────┘      └──────────────┘
```

**Example: Order Processing**

```python
# Order Service (Producer)
from kafka import KafkaProducer
import json

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def create_order(user_id, items):
    order = Order(user_id=user_id, items=items)
    db.save(order)
    
    # Publish event (async, non-blocking)
    producer.send('order-created', {
        'order_id': order.id,
        'user_id': user_id,
        'total': order.total,
        'timestamp': datetime.now().isoformat()
    })
    
    return order

# Notification Service (Consumer)
from kafka import KafkaConsumer

consumer = KafkaConsumer(
    'order-created',
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

for message in consumer:
    order = message.value
    
    # Send notification
    send_email(
        to=get_user_email(order['user_id']),
        subject='Order Confirmation',
        body=f"Your order {order['order_id']} is confirmed"
    )
    
    # Send SMS
    send_sms(
        to=get_user_phone(order['user_id']),
        body=f"Order {order['order_id']} confirmed"
    )
```

**Message Queue Benefits:**
1. **Decoupling:** Services don't need to know about each other
2. **Reliability:** Messages persisted, retry on failure
3. **Scalability:** Multiple consumers process in parallel
4. **Async:** Producer doesn't wait for consumers

**When to Use Each:**

```
Synchronous (REST/gRPC):
  ✅ Need immediate response (get user info)
  ✅ Request-response pattern
  ✅ Simple workflows
  
Asynchronous (Message Queue):
  ✅ Don't need immediate response (send email)
  ✅ Fan-out (one event, multiple consumers)
  ✅ Heavy processing (video encoding)
  ✅ Retry logic needed
```

---

## 🌐 API Gateway

The API Gateway is a single entry point for all clients. It routes requests to appropriate microservices.

### Architecture

```
┌─────────┐
│ Mobile  │──┐
└─────────┘  │
             │
┌─────────┐  │    ┌──────────────────┐
│   Web   │──┼───▶│   API Gateway    │
└─────────┘  │    │ • Authentication │
             │    │ • Rate Limiting  │
┌─────────┐  │    │ • Load Balancing │
│   IoT   │──┘    │ • Request Routing│
└─────────┘       └─────────┬────────┘
                            │
            ┌───────────────┼───────────────┐
            │               │               │
       ┌────▼───┐      ┌────▼───┐     ┌────▼───┐
       │ User   │      │Product │     │ Order  │
       │Service │      │Service │     │Service │
       └────────┘      └────────┘     └────────┘
```

### Responsibilities

**1. Authentication & Authorization**

```python
from flask import Flask, request, jsonify
import jwt

app = Flask(__name__)

@app.before_request
def authenticate():
    token = request.headers.get('Authorization')
    
    if not token:
        return jsonify({'error': 'No token'}), 401
    
    try:
        # Verify JWT
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        request.user_id = payload['user_id']
        request.roles = payload['roles']
    except jwt.InvalidTokenError:
        return jsonify({'error': 'Invalid token'}), 401
```

**2. Request Routing**

```python
# Nginx configuration
upstream user_service {
    server user-service-1:5000;
    server user-service-2:5000;
}

upstream order_service {
    server order-service-1:5000;
    server order-service-2:5000;
}

server {
    listen 80;
    
    location /api/users/ {
        proxy_pass http://user_service;
    }
    
    location /api/orders/ {
        proxy_pass http://order_service;
    }
}
```

**3. Rate Limiting**

```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["100 per hour"]
)

@app.route('/api/orders')
@limiter.limit("10 per minute")
def create_order():
    # Create order
    pass
```

**4. Request/Response Transformation**

```python
# Client expects different format
@app.route('/api/v1/users/<user_id>')
def get_user_v1(user_id):
    # Call backend service
    user = requests.get(f'http://user-service/users/{user_id}').json()
    
    # Transform response for v1 clients
    return jsonify({
        'userId': user['id'],  # Camel case
        'fullName': user['name'],
        'emailAddress': user['email']
    })
```

**5. Circuit Breaker**

```python
from pybreaker import CircuitBreaker

# Prevent cascading failures
user_service_breaker = CircuitBreaker(
    fail_max=5,  # Open after 5 failures
    timeout_duration=60  # Stay open for 60 seconds
)

@app.route('/api/orders')
def create_order():
    try:
        # Call user service with circuit breaker
        user = user_service_breaker.call(
            requests.get,
            f'http://user-service/users/{user_id}'
        )
    except CircuitBreakerError:
        # Service is down, return cached data or error
        return jsonify({'error': 'User service unavailable'}), 503
```

---

## 🗄️ Data Management

### Database per Service

Each microservice has its own database. No shared databases.

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│ User Service │     │Order Service │     │ Inventory    │
│              │     │              │     │  Service     │
│ ┌──────────┐ │     │ ┌──────────┐ │     │ ┌──────────┐ │
│ │ User DB  │ │     │ │ Order DB │ │     │ │Inventory │ │
│ └──────────┘ │     │ └──────────┘ │     │ │   DB     │ │
└──────────────┘     └──────────────┘     │ └──────────┘ │
                                          └──────────────┘
```

**Benefits:**
- ✅ Independent scaling
- ✅ Technology diversity (SQL, NoSQL, etc.)
- ✅ Fault isolation
- ✅ Clear ownership

**Challenges:**
- ❌ No ACID transactions across services
- ❌ Joins across databases
- ❌ Data consistency

### Saga Pattern (Distributed Transactions)

**Problem:** How to maintain data consistency across services without distributed transactions?

**Example: E-commerce Order**
1. Create order
2. Reserve inventory
3. Process payment
4. Update shipping

If payment fails, must rollback order and inventory.

#### Choreography-Based Saga

Services communicate via events:

```python
# Order Service
def create_order(user_id, items):
    order = Order(user_id=user_id, items=items, status='PENDING')
    db.save(order)
    
    # Publish event
    event_bus.publish('OrderCreated', {
        'order_id': order.id,
        'items': items
    })

# Inventory Service (listens to OrderCreated)
@event_bus.subscribe('OrderCreated')
def reserve_inventory(event):
    order_id = event['order_id']
    items = event['items']
    
    if can_reserve(items):
        reserve(items)
        event_bus.publish('InventoryReserved', {'order_id': order_id})
    else:
        event_bus.publish('InventoryReservationFailed', {'order_id': order_id})

# Payment Service (listens to InventoryReserved)
@event_bus.subscribe('InventoryReserved')
def process_payment(event):
    order_id = event['order_id']
    
    if payment_successful():
        event_bus.publish('PaymentProcessed', {'order_id': order_id})
    else:
        event_bus.publish('PaymentFailed', {'order_id': order_id})

# Order Service (listens to PaymentFailed)
@event_bus.subscribe('PaymentFailed')
def handle_payment_failure(event):
    order_id = event['order_id']
    
    # Compensating transaction
    db.update_order_status(order_id, 'CANCELLED')
    
    # Tell inventory to release
    event_bus.publish('ReleaseInventory', {'order_id': order_id})
```

#### Orchestration-Based Saga

Central orchestrator coordinates the saga:

```python
class OrderSagaOrchestrator:
    def create_order(self, user_id, items):
        saga_id = generate_id()
        
        try:
            # Step 1: Create order
            order = order_service.create_order(user_id, items)
            
            # Step 2: Reserve inventory
            inventory_service.reserve(order.id, items)
            
            # Step 3: Process payment
            payment_service.charge(user_id, order.total)
            
            # Step 4: Update shipping
            shipping_service.create_shipment(order.id)
            
            # Success - commit saga
            order_service.update_status(order.id, 'CONFIRMED')
            
        except InventoryException:
            # Rollback: Cancel order
            order_service.cancel(order.id)
            raise
            
        except PaymentException:
            # Rollback: Release inventory, cancel order
            inventory_service.release(order.id)
            order_service.cancel(order.id)
            raise
```

**Choreography vs Orchestration:**

| Aspect | Choreography | Orchestration |
|--------|--------------|---------------|
| Coordination | Distributed (events) | Centralized (orchestrator) |
| Complexity | Hard to track flow | Easier to understand |
| Coupling | Loose | Tighter |
| Failure Handling | Distributed | Centralized |
| Best For | Simple workflows | Complex workflows |

---

## 🔍 Service Discovery

How do services find each other in a dynamic environment?

### Client-Side Discovery

```
┌─────────┐         ┌──────────────┐
│ Service │────────▶│  Registry    │
│   A     │◀────────│ (Consul/Etcd)│
└────┬────┘         └──────────────┘
     │ 1. Query                   ▲
     │    "Where is Service B?"   │ 2. Heartbeat
     │                            │    (Register)
     ▼ 3. Get IP:Port             │
┌─────────┐                  ┌─────────┐
│ Service │─────────────────▶│ Service │
│   A     │  4. Direct call  │    B    │
└─────────┘                  └─────────┘
```

```python
import consul

# Service B registers itself
def register_service():
    c = consul.Consul()
    c.agent.service.register(
        name='service-b',
        service_id='service-b-1',
        address='192.168.1.10',
        port=5000,
        check=consul.Check.http('http://192.168.1.10:5000/health', interval='10s')
    )

# Service A discovers Service B
def call_service_b():
    c = consul.Consul()
    
    # Get all instances of service-b
    _, services = c.health.service('service-b', passing=True)
    
    # Pick one (round-robin, random, etc.)
    service = random.choice(services)
    address = service['Service']['Address']
    port = service['Service']['Port']
    
    # Make request
    response = requests.get(f'http://{address}:{port}/api/data')
    return response.json()
```

### Server-Side Discovery

```
┌─────────┐         ┌──────────────┐         ┌─────────┐
│ Service │────────▶│Load Balancer │────────▶│ Service │
│   A     │         │   (Nginx)    │         │    B    │
└─────────┘         └──────┬───────┘         └─────────┘
                           │                       ▲
                           │                       │
                           ▼                       │
                    ┌──────────────┐               │
                    │   Registry   │───────────────┘
                    │(Consul/K8s)  │ Sync instances
                    └──────────────┘
```

---

## 📊 Monitoring & Observability

### 1. Health Checks

```python
@app.route('/health')
def health_check():
    # Check database
    try:
        db.execute("SELECT 1")
        db_healthy = True
    except:
        db_healthy = False
    
    # Check external dependencies
    redis_healthy = redis.ping()
    
    status = 'healthy' if (db_healthy and redis_healthy) else 'unhealthy'
    
    return jsonify({
        'status': status,
        'database': 'up' if db_healthy else 'down',
        'cache': 'up' if redis_healthy else 'down'
    }), 200 if status == 'healthy' else 503
```

### 2. Distributed Tracing

Track requests across multiple services:

```python
from opentelemetry import trace
from opentelemetry.instrumentation.requests import RequestsInstrumentor

# Auto-instrument requests
RequestsInstrumentor().instrument()

tracer = trace.get_tracer(__name__)

@app.route('/api/orders')
def create_order():
    with tracer.start_as_current_span("create_order"):
        # This span will be parent
        
        # Call user service (child span)
        user = requests.get('http://user-service/users/123')
        
        # Call inventory service (child span)
        inventory = requests.get('http://inventory-service/check')
        
        # Create order
        order = Order(...)
        db.save(order)
        
        return jsonify(order)
```

**Trace visualization:**
```
create_order (Order Service) ─────────────────────── 250ms
  ├── GET /users/123 (User Service) ──────────── 50ms
  ├── GET /check (Inventory Service) ───────── 30ms
  └── db.save (Database) ───────────────────── 150ms
```

### 3. Metrics

```python
from prometheus_client import Counter, Histogram, Gauge

# Request counter
request_count = Counter('http_requests_total', 'Total HTTP requests', ['method', 'endpoint'])

# Response time
response_time = Histogram('http_response_time_seconds', 'HTTP response time')

# Active connections
active_connections = Gauge('active_connections', 'Active database connections')

@app.route('/api/orders', methods=['POST'])
@response_time.time()  # Measure duration
def create_order():
    request_count.labels(method='POST', endpoint='/api/orders').inc()
    
    # Business logic
    order = create_order_logic()
    
    active_connections.set(db.get_active_connections())
    
    return jsonify(order)
```

---

## 💡 Best Practices

### 1. Design Principles

**Single Responsibility:** Each service does one thing well
```
✅ UserService: Manage users
✅ OrderService: Manage orders
✅ NotificationService: Send notifications

❌ UserOrderNotificationService: Too much
```

**Bounded Context (DDD):** Group related functionality
```
✅ Order Context: Orders, OrderItems, OrderStatus
✅ User Context: Users, Profiles, Preferences

❌ Mixed: Orders calling User database directly
```

**API Versioning:**
```python
# URL versioning (recommended)
@app.route('/api/v1/users')
def get_users_v1():
    return jsonify(users)

@app.route('/api/v2/users')
def get_users_v2():
    # New format
    return jsonify(enhanced_users)
```

### 2. Resilience Patterns

**Timeout:**
```python
# Always set timeouts
response = requests.get('http://service-b/api/data', timeout=5)
```

**Retry with Exponential Backoff:**
```python
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=10))
def call_external_service():
    return requests.get('http://external-api.com/data')
```

**Bulkhead:** Isolate resources
```python
# Separate thread pools for different services
user_service_pool = ThreadPoolExecutor(max_workers=10)
order_service_pool = ThreadPoolExecutor(max_workers=20)

# If order service is slow, user service isn't affected
```

---

## 🎯 Interview Tips

**Key Points to Cover:**
1. ✅ When to use microservices vs monolith
2. ✅ Sync vs async communication
3. ✅ API Gateway responsibilities
4. ✅ Data consistency (Saga pattern)
5. ✅ Service discovery

**Common Questions:**
- "When would you NOT use microservices?" → Small teams, simple apps, tight deadlines
- "How to handle distributed transactions?" → Saga pattern (choreography/orchestration)
- "How do services discover each other?" → Service registry (Consul, Kubernetes)
- "How to version APIs?" → URL versioning (/v1, /v2)

**Red Flags:**
- ❌ "Microservices solve all problems"
- ❌ "Make every function a microservice" (too granular)
- ❌ Shared databases between services
- ❌ No monitoring/tracing

---

**Next:** [Storage Systems](07_storage.md)
