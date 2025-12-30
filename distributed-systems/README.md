# Distributed Systems

Building reliable, scalable distributed applications with modern patterns and technologies.

---

## 📋 Core Concepts

### 1. **CAP Theorem**

**You can only guarantee 2 out of 3:**
- **C**onsistency: All nodes see the same data
- **A**vailability: Every request gets a response
- **P**artition tolerance: System works despite network failures

```
        Consistency
           /  \
          /    \
         /      \
    CA /        \ CP
      /          \
     /     AP     \
    /_____________\
  Availability   Partition
                Tolerance
```

#### Real-World Examples:
- **CP Systems (Consistency + Partition Tolerance):** MongoDB, HBase, Redis (with replication)
  - Choose consistency over availability during network partitions
  - Better for financial transactions, inventory management
  
- **AP Systems (Availability + Partition Tolerance):** Cassandra, DynamoDB, Riak
  - Choose availability over consistency during network partitions
  - Better for social media feeds, shopping carts
  
- **CA Systems (Consistency + Availability):** Traditional RDBMS (single node)
  - Not partition-tolerant (single point of failure)

---

### 2. **Consensus Algorithms**

#### Raft Consensus
```python
"""
Raft: Leader election and log replication

States: Leader, Follower, Candidate
Terms: Logical clock for leader elections
"""

from enum import Enum
from typing import List, Dict
import time
import random

class State(Enum):
    FOLLOWER = 1
    CANDIDATE = 2
    LEADER = 3

class RaftNode:
    def __init__(self, node_id: int, cluster_size: int):
        self.node_id = node_id
        self.cluster_size = cluster_size
        self.state = State.FOLLOWER
        self.current_term = 0
        self.voted_for = None
        self.log = []
        self.commit_index = 0
        self.last_applied = 0
        
        # Leader state
        self.next_index = {}
        self.match_index = {}
        
        # Timeouts
        self.election_timeout = random.uniform(150, 300)  # ms
        self.last_heartbeat = time.time()
    
    def start_election(self):
        """Candidate starts election"""
        self.state = State.CANDIDATE
        self.current_term += 1
        self.voted_for = self.node_id
        votes_received = 1
        
        # Request votes from other nodes
        for node in self.get_other_nodes():
            vote_granted = self.request_vote(node)
            if vote_granted:
                votes_received += 1
        
        # Check if won election (majority)
        if votes_received > self.cluster_size // 2:
            self.become_leader()
    
    def become_leader(self):
        """Transition to leader state"""
        self.state = State.LEADER
        
        # Initialize leader state
        for node_id in range(self.cluster_size):
            if node_id != self.node_id:
                self.next_index[node_id] = len(self.log)
                self.match_index[node_id] = 0
        
        # Send heartbeats
        self.send_heartbeats()
    
    def append_entries(self, term: int, leader_id: int, 
                      prev_log_index: int, entries: List):
        """Follower receives append entries (heartbeat or log replication)"""
        if term < self.current_term:
            return False
        
        self.last_heartbeat = time.time()
        self.state = State.FOLLOWER
        
        if term > self.current_term:
            self.current_term = term
            self.voted_for = None
        
        # Log replication logic here
        return True
```

#### Two-Phase Commit (2PC)
```python
"""
Two-Phase Commit: Distributed transaction protocol

Phase 1: Prepare - Coordinator asks all participants to prepare
Phase 2: Commit/Abort - Based on unanimous agreement
"""

from enum import Enum
from typing import List, Dict

class TransactionState(Enum):
    INIT = 1
    PREPARED = 2
    COMMITTED = 3
    ABORTED = 4

class Coordinator:
    def __init__(self, participants: List[str]):
        self.participants = participants
        self.state = TransactionState.INIT
    
    def execute_transaction(self, transaction_data: Dict) -> bool:
        """
        Execute 2PC protocol
        Returns True if committed, False if aborted
        """
        # Phase 1: Prepare
        print("Phase 1: Sending PREPARE to all participants")
        prepared_responses = []
        
        for participant in self.participants:
            response = self.send_prepare(participant, transaction_data)
            prepared_responses.append(response)
            
            if not response:
                # Any participant votes NO -> abort
                print(f"Participant {participant} voted NO")
                self.send_abort_to_all()
                self.state = TransactionState.ABORTED
                return False
        
        # All participants voted YES
        self.state = TransactionState.PREPARED
        
        # Phase 2: Commit
        print("Phase 2: Sending COMMIT to all participants")
        for participant in self.participants:
            self.send_commit(participant)
        
        self.state = TransactionState.COMMITTED
        return True
    
    def send_prepare(self, participant: str, data: Dict) -> bool:
        """Ask participant to prepare transaction"""
        # Participant checks if it can commit
        # Returns True (YES) or False (NO)
        pass
    
    def send_commit(self, participant: str):
        """Tell participant to commit"""
        pass
    
    def send_abort_to_all(self):
        """Tell all participants to abort"""
        for participant in self.participants:
            self.send_abort(participant)

class Participant:
    def __init__(self, participant_id: str):
        self.participant_id = participant_id
        self.state = TransactionState.INIT
        self.transaction_log = []
    
    def prepare(self, transaction_data: Dict) -> bool:
        """
        Prepare phase:
        - Validate transaction
        - Lock resources
        - Write to transaction log
        - Return YES/NO vote
        """
        try:
            # Validate transaction
            if not self.validate_transaction(transaction_data):
                return False
            
            # Lock resources
            self.lock_resources(transaction_data)
            
            # Write prepare record to log
            self.transaction_log.append(('PREPARE', transaction_data))
            
            self.state = TransactionState.PREPARED
            return True
        except Exception as e:
            print(f"Prepare failed: {e}")
            return False
    
    def commit(self):
        """Commit phase: Apply changes and release locks"""
        self.transaction_log.append(('COMMIT',))
        self.apply_changes()
        self.release_locks()
        self.state = TransactionState.COMMITTED
    
    def abort(self):
        """Abort: Rollback and release locks"""
        self.transaction_log.append(('ABORT',))
        self.rollback_changes()
        self.release_locks()
        self.state = TransactionState.ABORTED
```

---

### 3. **Message Queues**

#### Kafka Producer/Consumer
```python
from kafka import KafkaProducer, KafkaConsumer
from kafka.errors import KafkaError
import json

# Producer
class EventProducer:
    def __init__(self, bootstrap_servers: List[str]):
        self.producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            acks='all',  # Wait for all replicas
            retries=3,
            max_in_flight_requests_per_connection=1  # Preserve order
        )
    
    def send_event(self, topic: str, key: str, value: dict):
        """Send event to Kafka topic"""
        future = self.producer.send(
            topic,
            key=key.encode('utf-8'),
            value=value
        )
        
        try:
            # Block for 'synchronous' send
            record_metadata = future.get(timeout=10)
            print(f"Message sent to {record_metadata.topic} "
                  f"partition {record_metadata.partition} "
                  f"offset {record_metadata.offset}")
        except KafkaError as e:
            print(f"Failed to send message: {e}")

# Consumer
class EventConsumer:
    def __init__(self, bootstrap_servers: List[str], 
                 group_id: str, topics: List[str]):
        self.consumer = KafkaConsumer(
            *topics,
            bootstrap_servers=bootstrap_servers,
            group_id=group_id,
            value_deserializer=lambda m: json.loads(m.decode('utf-8')),
            enable_auto_commit=False,  # Manual commit for at-least-once
            auto_offset_reset='earliest'
        )
    
    def consume(self):
        """Consume messages from Kafka"""
        for message in self.consumer:
            try:
                # Process message
                self.process_message(message.value)
                
                # Commit offset after successful processing
                self.consumer.commit()
                
            except Exception as e:
                print(f"Error processing message: {e}")
                # Don't commit - message will be reprocessed
    
    def process_message(self, data: dict):
        """Process individual message (idempotent operation)"""
        print(f"Processing: {data}")

# Usage
producer = EventProducer(['localhost:9092'])
producer.send_event('user-events', 'user-123', {
    'event_type': 'user_registered',
    'user_id': 123,
    'timestamp': time.time()
})

consumer = EventConsumer(
    ['localhost:9092'],
    group_id='analytics-service',
    topics=['user-events']
)
consumer.consume()
```

#### RabbitMQ with Work Queues
```python
import pika
import json
import time

# Producer
class TaskPublisher:
    def __init__(self, host: str = 'localhost'):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=host)
        )
        self.channel = self.connection.channel()
        
        # Declare durable queue
        self.channel.queue_declare(queue='tasks', durable=True)
    
    def publish_task(self, task_data: dict):
        """Publish task to queue"""
        self.channel.basic_publish(
            exchange='',
            routing_key='tasks',
            body=json.dumps(task_data),
            properties=pika.BasicProperties(
                delivery_mode=2,  # Make message persistent
            )
        )
        print(f"Published task: {task_data}")
    
    def close(self):
        self.connection.close()

# Worker (Consumer)
class TaskWorker:
    def __init__(self, host: str = 'localhost'):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=host)
        )
        self.channel = self.connection.channel()
        
        # Declare same queue
        self.channel.queue_declare(queue='tasks', durable=True)
        
        # Fair dispatch - don't give worker new task until it finishes current
        self.channel.basic_qos(prefetch_count=1)
    
    def callback(self, ch, method, properties, body):
        """Process task"""
        task_data = json.loads(body)
        print(f"Processing task: {task_data}")
        
        try:
            # Simulate work
            time.sleep(task_data.get('duration', 1))
            
            # Acknowledge message after processing
            ch.basic_ack(delivery_tag=method.delivery_tag)
            print("Task completed")
            
        except Exception as e:
            print(f"Task failed: {e}")
            # Requeue message
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)
    
    def start(self):
        """Start consuming tasks"""
        self.channel.basic_consume(
            queue='tasks',
            on_message_callback=self.callback
        )
        
        print('Worker waiting for tasks...')
        self.channel.start_consuming()
```

---

### 4. **Distributed Caching**

#### Cache Consistency Patterns
```python
import redis
import hashlib
from typing import Optional

class DistributedCache:
    def __init__(self, redis_hosts: List[str]):
        self.nodes = [
            redis.Redis(host=host, port=6379, db=0)
            for host in redis_hosts
        ]
    
    def _get_node(self, key: str) -> redis.Redis:
        """Consistent hashing to determine which node"""
        hash_value = int(hashlib.md5(key.encode()).hexdigest(), 16)
        node_index = hash_value % len(self.nodes)
        return self.nodes[node_index]
    
    def get(self, key: str) -> Optional[str]:
        """Get value from cache"""
        node = self._get_node(key)
        return node.get(key)
    
    def set(self, key: str, value: str, ttl: int = 3600):
        """Set value in cache with TTL"""
        node = self._get_node(key)
        node.setex(key, ttl, value)
    
    def delete(self, key: str):
        """Delete key from cache"""
        node = self._get_node(key)
        node.delete(key)
    
    def cache_aside(self, key: str, fetch_func):
        """Cache-aside pattern"""
        # Try cache first
        cached = self.get(key)
        if cached:
            return json.loads(cached)
        
        # Cache miss - fetch from source
        value = fetch_func()
        
        # Store in cache
        self.set(key, json.dumps(value))
        
        return value
```

---

### 5. **Service Mesh & Circuit Breakers**

#### Circuit Breaker Pattern
```python
from enum import Enum
import time
from typing import Callable, Any

class CircuitState(Enum):
    CLOSED = 1      # Normal operation
    OPEN = 2        # Failing, reject requests
    HALF_OPEN = 3   # Testing if service recovered

class CircuitBreaker:
    def __init__(self, failure_threshold: int = 5, 
                 timeout: int = 60, 
                 success_threshold: int = 2):
        self.failure_threshold = failure_threshold
        self.timeout = timeout  # seconds
        self.success_threshold = success_threshold
        
        self.failure_count = 0
        self.success_count = 0
        self.last_failure_time = None
        self.state = CircuitState.CLOSED
    
    def call(self, func: Callable, *args, **kwargs) -> Any:
        """Execute function with circuit breaker protection"""
        
        if self.state == CircuitState.OPEN:
            if time.time() - self.last_failure_time > self.timeout:
                # Timeout passed, try again
                self.state = CircuitState.HALF_OPEN
                self.success_count = 0
            else:
                raise Exception("Circuit breaker is OPEN")
        
        try:
            result = func(*args, **kwargs)
            self._on_success()
            return result
            
        except Exception as e:
            self._on_failure()
            raise e
    
    def _on_success(self):
        """Handle successful call"""
        self.failure_count = 0
        
        if self.state == CircuitState.HALF_OPEN:
            self.success_count += 1
            if self.success_count >= self.success_threshold:
                self.state = CircuitState.CLOSED
                self.success_count = 0
    
    def _on_failure(self):
        """Handle failed call"""
        self.failure_count += 1
        self.last_failure_time = time.time()
        
        if self.failure_count >= self.failure_threshold:
            self.state = CircuitState.OPEN

# Usage
import requests

payment_service_breaker = CircuitBreaker(
    failure_threshold=5,
    timeout=60,
    success_threshold=2
)

def call_payment_service(amount: float):
    def make_request():
        response = requests.post(
            'https://payment-service/charge',
            json={'amount': amount},
            timeout=5
        )
        response.raise_for_status()
        return response.json()
    
    return payment_service_breaker.call(make_request)
```

---

### 6. **Distributed Tracing**

#### OpenTelemetry Implementation
```python
from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.instrumentation.requests import RequestsInstrumentor

# Setup tracing
trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer(__name__)

jaeger_exporter = JaegerExporter(
    agent_host_name="localhost",
    agent_port=6831,
)

span_processor = BatchSpanProcessor(jaeger_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)

# Auto-instrument requests library
RequestsInstrumentor().instrument()

# Create spans
def process_order(order_id: str):
    with tracer.start_as_current_span("process_order") as span:
        span.set_attribute("order.id", order_id)
        
        # Child span
        with tracer.start_as_current_span("validate_order"):
            validate_order(order_id)
        
        # Another child span
        with tracer.start_as_current_span("charge_payment"):
            charge_payment(order_id)
        
        # HTTP call automatically traced
        response = requests.post(f"https://inventory/reserve/{order_id}")
        
        span.set_attribute("order.status", "completed")
        return response.json()
```

---

## 🎯 Senior Engineer Focus Areas

### **1. Designing for Failure**
- Implement retries with exponential backoff
- Use circuit breakers for external services
- Design idempotent APIs
- Handle partial failures gracefully

### **2. Eventual Consistency**
- Understand CRDT (Conflict-free Replicated Data Types)
- Implement Saga pattern for distributed transactions
- Use event sourcing where appropriate

### **3. Scalability Patterns**
- Horizontal scaling with stateless services
- Load balancing strategies
- Database sharding
- Caching at multiple levels

### **4. Observability**
- Distributed tracing (Jaeger, Zipkin)
- Centralized logging (ELK, Splunk)
- Metrics and monitoring (Prometheus, Grafana)
- Alerting and on-call practices

---

## 📚 Learning Resources

**Books:**
- "Designing Data-Intensive Applications" - Martin Kleppmann
- "Distributed Systems" - Maarten van Steen
- "Building Microservices" - Sam Newman

**Papers:**
- "The Google File System" (GFS)
- "MapReduce: Simplified Data Processing on Large Clusters"
- "Dynamo: Amazon's Highly Available Key-value Store"
- "The Raft Consensus Algorithm"

**Practice:**
- Implement Raft consensus
- Build distributed cache
- Design event-driven architecture
- Set up Kafka cluster
