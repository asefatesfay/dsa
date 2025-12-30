# Distributed Systems - Real-World Examples

## 🎯 Case Study: Netflix Microservices

**Scale:**
- 200 million subscribers
- 1 trillion API calls/month
- 800+ microservices
- Multi-region deployment

**Architecture:**

```
┌─────────────────────────────────────────────┐
│              Edge Services                   │
│  - API Gateway (Zuul)                        │
│  - CDN (Open Connect)                        │
└───────────────┬─────────────────────────────┘
                │
    ┌───────────┴───────────┐
    │                       │
    ▼                       ▼
┌─────────────┐      ┌─────────────┐
│  Eureka     │      │  Hystrix    │
│  (Service   │      │  (Circuit   │
│  Discovery) │      │  Breaker)   │
└─────────────┘      └─────────────┘
                │
    ┌───────────┼───────────┐
    │           │           │
    ▼           ▼           ▼
┌────────┐  ┌────────┐  ┌────────┐
│ User   │  │Billing │  │Content │
│Service │  │Service │  │Service │
└────────┘  └────────┘  └────────┘
```

**Key Patterns:**
1. **Service Discovery:** Eureka
2. **Circuit Breaker:** Hystrix
3. **Load Balancing:** Ribbon
4. **API Gateway:** Zuul
5. **Distributed Tracing:** Zipkin

## 🎯 Real Problem: Distributed Transaction

**Scenario:** E-commerce order processing

**Problem:** Atomic operation across services
- Inventory service: Reserve items
- Payment service: Charge customer
- Shipping service: Create shipment

**Solution: Saga Pattern**

```python
from enum import Enum

class SagaState(Enum):
    STARTED = 1
    INVENTORY_RESERVED = 2
    PAYMENT_COMPLETED = 3
    SHIPPING_CREATED = 4
    COMPLETED = 5
    FAILED = 6

class OrderSaga:
    def __init__(self, order_id):
        self.order_id = order_id
        self.state = SagaState.STARTED
    
    async def execute(self):
        try:
            # Step 1: Reserve inventory
            await inventory_service.reserve(self.order_id)
            self.state = SagaState.INVENTORY_RESERVED
            
            # Step 2: Process payment
            await payment_service.charge(self.order_id)
            self.state = SagaState.PAYMENT_COMPLETED
            
            # Step 3: Create shipment
            await shipping_service.create(self.order_id)
            self.state = SagaState.SHIPPING_CREATED
            
            self.state = SagaState.COMPLETED
            
        except Exception as e:
            # Compensating transactions (rollback)
            await self.rollback()
            self.state = SagaState.FAILED
            raise
    
    async def rollback(self):
        """Execute compensating transactions"""
        if self.state >= SagaState.SHIPPING_CREATED:
            await shipping_service.cancel(self.order_id)
        
        if self.state >= SagaState.PAYMENT_COMPLETED:
            await payment_service.refund(self.order_id)
        
        if self.state >= SagaState.INVENTORY_RESERVED:
            await inventory_service.release(self.order_id)
```

## 🎯 Event-Driven Architecture: Real Implementation

**Use Case:** User Registration Flow

```python
# Producer
from kafka import KafkaProducer
import json

producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def register_user(email, password):
    # 1. Create user in database
    user_id = db.create_user(email, hash_password(password))
    
    # 2. Publish event
    event = {
        'event_type': 'user.registered',
        'user_id': user_id,
        'email': email,
        'timestamp': time.time()
    }
    
    producer.send('user-events', value=event, key=str(user_id))
    producer.flush()
    
    return user_id

# Consumer 1: Send Welcome Email
class WelcomeEmailConsumer:
    def __init__(self):
        self.consumer = KafkaConsumer(
            'user-events',
            bootstrap_servers=['localhost:9092'],
            group_id='email-service',
            value_deserializer=lambda m: json.loads(m.decode('utf-8'))
        )
    
    def process(self):
        for message in self.consumer:
            event = message.value
            
            if event['event_type'] == 'user.registered':
                send_welcome_email(event['email'])
                self.consumer.commit()

# Consumer 2: Create User Profile
class ProfileCreationConsumer:
    def __init__(self):
        self.consumer = KafkaConsumer(
            'user-events',
            bootstrap_servers=['localhost:9092'],
            group_id='profile-service',
            value_deserializer=lambda m: json.loads(m.decode('utf-8'))
        )
    
    def process(self):
        for message in self.consumer:
            event = message.value
            
            if event['event_type'] == 'user.registered':
                create_default_profile(event['user_id'])
                self.consumer.commit()

# Consumer 3: Analytics Tracking
class AnalyticsConsumer:
    def __init__(self):
        self.consumer = KafkaConsumer(
            'user-events',
            bootstrap_servers=['localhost:9092'],
            group_id='analytics-service',
            value_deserializer=lambda m: json.loads(m.decode('utf-8'))
        )
    
    def process(self):
        for message in self.consumer:
            event = message.value
            
            if event['event_type'] == 'user.registered':
                track_registration(event['user_id'], event['timestamp'])
                self.consumer.commit()
```

**Benefits:**
- Loose coupling between services
- Easy to add new consumers
- Fault tolerance (replay events)
- Asynchronous processing

## 🎯 Interview Question: Design Uber's Matching System

**Requirements:**
- Match riders with drivers in real-time
- Sub-second latency
- Handle 1M concurrent requests
- Geographical constraints

**Solution:**

```python
import redis
from geopy.distance import geodesic

class RideMatchingService:
    def __init__(self):
        self.redis = redis.Redis(host='localhost', port=6379)
    
    def update_driver_location(self, driver_id, lat, lon):
        """Update driver location using Redis Geospatial"""
        self.redis.geoadd('drivers:active', lon, lat, driver_id)
        
        # Set expiry (30 seconds)
        self.redis.expire(f'driver:{driver_id}:location', 30)
    
    def find_nearby_drivers(self, lat, lon, radius_km=5):
        """Find drivers within radius"""
        nearby = self.redis.georadius(
            'drivers:active',
            lon, lat,
            radius_km, unit='km',
            withdist=True,
            withcoord=True,
            sort='ASC'
        )
        
        return [
            {
                'driver_id': driver[0].decode(),
                'distance': float(driver[1]),
                'coordinates': driver[2]
            }
            for driver in nearby
        ]
    
    def request_ride(self, rider_id, pickup_lat, pickup_lon):
        """Request ride and match with nearest available driver"""
        
        # Find nearby drivers (within 5km)
        nearby_drivers = self.find_nearby_drivers(
            pickup_lat, 
            pickup_lon, 
            radius_km=5
        )
        
        if not nearby_drivers:
            return None  # No drivers available
        
        # Sort by distance and status
        for driver in nearby_drivers:
            driver_id = driver['driver_id']
            
            # Try to atomically claim driver
            claimed = self.redis.set(
                f'driver:{driver_id}:claimed',
                rider_id,
                nx=True,  # Only if not exists
                ex=60     # Expire in 60 seconds
            )
            
            if claimed:
                # Successfully matched!
                ride_id = self.create_ride(rider_id, driver_id)
                
                # Notify driver via push notification
                self.notify_driver(driver_id, ride_id)
                
                return {
                    'ride_id': ride_id,
                    'driver_id': driver_id,
                    'eta': self.calculate_eta(driver, pickup_lat, pickup_lon)
                }
        
        return None  # All drivers claimed by other riders
```

## 📊 System Comparison

| Pattern | Use Case | Pros | Cons |
|---------|----------|------|------|
| **Monolith** | Small teams, simple apps | Easy to develop, deploy | Hard to scale |
| **Microservices** | Large teams, complex apps | Independent scaling | Complexity, latency |
| **Serverless** | Event-driven, variable load | Auto-scaling, no servers | Cold starts, vendor lock-in |
| **Event-Driven** | Async processing | Loose coupling | Eventual consistency |
| **CQRS** | Read-heavy workloads | Optimized reads/writes | Complexity |

## 🔧 Debugging Distributed Systems

```bash
# 1. Check service health
kubectl get pods -n production

# 2. Trace request across services
curl http://jaeger:16686/api/traces/{trace-id}

# 3. Check message queue lag
kafka-consumer-groups --bootstrap-server localhost:9092 \
  --describe --group user-service

# 4. Monitor metrics
curl http://prometheus:9090/api/v1/query?query=up

# 5. Check logs
kubectl logs -f deployment/user-service | grep ERROR
```
