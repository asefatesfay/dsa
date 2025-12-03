"""
Queue - Real World Applications
================================
Practical problems and use cases in real systems.
"""

from collections import deque
from typing import List, Optional
import time


# Problem 1: Print Job Queue
class PrintQueue:
    """
    Manage print jobs in office printer.
    Real-world use: Printer management systems, print servers
    """
    def __init__(self):
        self.queue = deque()
        self.job_id = 0
    
    def add_job(self, document: str, pages: int, priority: str = "normal") -> int:
        """Add print job to queue"""
        self.job_id += 1
        job = {
            'id': self.job_id,
            'document': document,
            'pages': pages,
            'priority': priority,
            'timestamp': time.time()
        }
        
        if priority == "urgent":
            # Add urgent jobs to front
            self.queue.appendleft(job)
        else:
            self.queue.append(job)
        
        return self.job_id
    
    def process_next(self) -> Optional[dict]:
        """Process next print job"""
        if self.queue:
            return self.queue.popleft()
        return None
    
    def cancel_job(self, job_id: int) -> bool:
        """Cancel specific job"""
        for i, job in enumerate(self.queue):
            if job['id'] == job_id:
                del self.queue[i]
                return True
        return False
    
    def get_queue_status(self) -> dict:
        """Get queue statistics"""
        total_pages = sum(job['pages'] for job in self.queue)
        return {
            'jobs_waiting': len(self.queue),
            'total_pages': total_pages,
            'next_job': self.queue[0]['document'] if self.queue else None
        }

print("Problem 1: Print Job Queue")
printer = PrintQueue()
printer.add_job("Report.pdf", 10)
printer.add_job("Invoice.pdf", 2, "urgent")
printer.add_job("Presentation.pptx", 25)
print(f"Queue status: {printer.get_queue_status()}")
job = printer.process_next()
print(f"Processing: {job['document']} ({job['pages']} pages)")
print(f"After processing: {printer.get_queue_status()}")
print()


# Problem 2: Customer Service Call Center
class CallCenter:
    """
    Manage incoming customer calls.
    Real-world use: Call centers, customer support systems
    """
    def __init__(self, num_agents: int):
        self.num_agents = num_agents
        self.available_agents = num_agents
        self.call_queue = deque()
        self.active_calls = []
        self.call_id = 0
    
    def receive_call(self, customer: str, issue: str, priority: int = 1) -> dict:
        """Receive incoming call"""
        self.call_id += 1
        call = {
            'id': self.call_id,
            'customer': customer,
            'issue': issue,
            'priority': priority,
            'wait_time': 0,
            'status': 'waiting'
        }
        
        if self.available_agents > 0:
            self._assign_to_agent(call)
        else:
            self.call_queue.append(call)
            call['status'] = 'queued'
        
        return call
    
    def _assign_to_agent(self, call: dict) -> None:
        """Assign call to available agent"""
        call['status'] = 'in_progress'
        self.active_calls.append(call)
        self.available_agents -= 1
    
    def end_call(self, call_id: int) -> bool:
        """End call and assign next from queue"""
        for i, call in enumerate(self.active_calls):
            if call['id'] == call_id:
                self.active_calls.pop(i)
                self.available_agents += 1
                
                # Assign next call from queue
                if self.call_queue:
                    next_call = self.call_queue.popleft()
                    self._assign_to_agent(next_call)
                
                return True
        return False
    
    def get_statistics(self) -> dict:
        """Get call center statistics"""
        return {
            'calls_in_queue': len(self.call_queue),
            'active_calls': len(self.active_calls),
            'available_agents': self.available_agents,
            'avg_wait_time': sum(c.get('wait_time', 0) for c in self.call_queue) / len(self.call_queue) if self.call_queue else 0
        }

print("Problem 2: Customer Service Call Center")
center = CallCenter(num_agents=2)
center.receive_call("Alice", "Billing issue")
center.receive_call("Bob", "Technical support")
center.receive_call("Charlie", "Account access")
print(f"Statistics: {center.get_statistics()}")
center.end_call(1)
print(f"After ending call 1: {center.get_statistics()}")
print()


# Problem 3: Task Scheduler (CPU Scheduling)
class TaskScheduler:
    """
    Schedule tasks for execution (Round Robin).
    Real-world use: Operating systems, process schedulers
    """
    def __init__(self, time_quantum: int = 2):
        self.time_quantum = time_quantum
        self.ready_queue = deque()
        self.completed = []
        self.current_time = 0
    
    def add_task(self, task_id: str, burst_time: int, arrival_time: int = 0):
        """Add task to scheduler"""
        task = {
            'id': task_id,
            'burst_time': burst_time,
            'remaining_time': burst_time,
            'arrival_time': arrival_time,
            'completion_time': 0,
            'waiting_time': 0
        }
        self.ready_queue.append(task)
    
    def execute_cycle(self) -> Optional[dict]:
        """Execute one scheduling cycle"""
        if not self.ready_queue:
            return None
        
        task = self.ready_queue.popleft()
        execution_time = min(self.time_quantum, task['remaining_time'])
        
        self.current_time += execution_time
        task['remaining_time'] -= execution_time
        
        if task['remaining_time'] > 0:
            # Task not finished, add back to queue
            self.ready_queue.append(task)
        else:
            # Task completed
            task['completion_time'] = self.current_time
            task['turnaround_time'] = task['completion_time'] - task['arrival_time']
            task['waiting_time'] = task['turnaround_time'] - task['burst_time']
            self.completed.append(task)
        
        return {
            'task_id': task['id'],
            'executed_time': execution_time,
            'remaining': task['remaining_time']
        }
    
    def run_all(self) -> List[dict]:
        """Run until all tasks complete"""
        execution_log = []
        while self.ready_queue:
            result = self.execute_cycle()
            if result:
                execution_log.append(result)
        return execution_log
    
    def get_statistics(self) -> dict:
        """Get scheduling statistics"""
        if not self.completed:
            return {}
        
        avg_waiting = sum(t['waiting_time'] for t in self.completed) / len(self.completed)
        avg_turnaround = sum(t['turnaround_time'] for t in self.completed) / len(self.completed)
        
        return {
            'completed_tasks': len(self.completed),
            'avg_waiting_time': avg_waiting,
            'avg_turnaround_time': avg_turnaround,
            'total_time': self.current_time
        }

print("Problem 3: Task Scheduler (Round Robin)")
scheduler = TaskScheduler(time_quantum=2)
scheduler.add_task("P1", 5)
scheduler.add_task("P2", 3)
scheduler.add_task("P3", 8)
log = scheduler.run_all()
print(f"Execution log: {log[:3]}...")  # First 3 entries
print(f"Statistics: {scheduler.get_statistics()}")
print()


# Problem 4: Web Server Request Queue
class WebServer:
    """
    Handle HTTP requests with rate limiting.
    Real-world use: Web servers, API gateways, load balancers
    """
    def __init__(self, max_concurrent: int = 10, rate_limit: int = 100):
        self.max_concurrent = max_concurrent
        self.rate_limit = rate_limit
        self.request_queue = deque()
        self.processing = []
        self.request_count = 0
        self.request_history = deque()  # (timestamp, request_id)
    
    def receive_request(self, url: str, method: str = "GET") -> dict:
        """Receive HTTP request"""
        current_time = time.time()
        
        # Remove old requests from history (older than 1 second)
        while self.request_history and self.request_history[0][0] < current_time - 1:
            self.request_history.popleft()
        
        # Check rate limit
        if len(self.request_history) >= self.rate_limit:
            return {'status': 'rejected', 'reason': 'rate_limit_exceeded'}
        
        self.request_count += 1
        request = {
            'id': self.request_count,
            'url': url,
            'method': method,
            'timestamp': current_time,
            'status': 'queued'
        }
        
        self.request_history.append((current_time, self.request_count))
        
        if len(self.processing) < self.max_concurrent:
            request['status'] = 'processing'
            self.processing.append(request)
        else:
            self.request_queue.append(request)
        
        return request
    
    def complete_request(self, request_id: int) -> bool:
        """Mark request as completed"""
        for i, req in enumerate(self.processing):
            if req['id'] == request_id:
                self.processing.pop(i)
                
                # Process next queued request
                if self.request_queue:
                    next_req = self.request_queue.popleft()
                    next_req['status'] = 'processing'
                    self.processing.append(next_req)
                
                return True
        return False
    
    def get_status(self) -> dict:
        """Get server status"""
        return {
            'queue_length': len(self.request_queue),
            'processing': len(self.processing),
            'capacity_used': f"{len(self.processing)}/{self.max_concurrent}",
            'requests_per_second': len(self.request_history)
        }

print("Problem 4: Web Server Request Queue")
server = WebServer(max_concurrent=3)
for i in range(5):
    result = server.receive_request(f"/api/data/{i}")
    print(f"Request {i}: {result['status']}")
print(f"Server status: {server.get_status()}")
server.complete_request(1)
print(f"After completing request 1: {server.get_status()}")
print()


# Problem 5: Message Queue System
class MessageQueue:
    """
    Implement message queue for microservices.
    Real-world use: RabbitMQ, Kafka, AWS SQS
    """
    def __init__(self, name: str):
        self.name = name
        self.messages = deque()
        self.dead_letter_queue = deque()
        self.message_id = 0
    
    def publish(self, payload: dict, priority: int = 0) -> int:
        """Publish message to queue"""
        self.message_id += 1
        message = {
            'id': self.message_id,
            'payload': payload,
            'priority': priority,
            'attempts': 0,
            'max_attempts': 3,
            'timestamp': time.time()
        }
        self.messages.append(message)
        return self.message_id
    
    def consume(self) -> Optional[dict]:
        """Consume message from queue"""
        if not self.messages:
            return None
        return self.messages.popleft()
    
    def ack(self, message: dict) -> bool:
        """Acknowledge message processed successfully"""
        # Message successfully processed, nothing to do
        return True
    
    def nack(self, message: dict) -> bool:
        """Negative acknowledgment - retry or move to DLQ"""
        message['attempts'] += 1
        
        if message['attempts'] < message['max_attempts']:
            # Retry - add back to queue
            self.messages.append(message)
            return True
        else:
            # Move to dead letter queue
            self.dead_letter_queue.append(message)
            return False
    
    def get_stats(self) -> dict:
        """Get queue statistics"""
        return {
            'queue_name': self.name,
            'messages_pending': len(self.messages),
            'messages_in_dlq': len(self.dead_letter_queue),
            'total_published': self.message_id
        }

print("Problem 5: Message Queue System")
mq = MessageQueue("order-processing")
mq.publish({'order_id': 101, 'amount': 99.99})
mq.publish({'order_id': 102, 'amount': 149.99})
print(f"Queue stats: {mq.get_stats()}")
msg = mq.consume()
print(f"Consumed: Order {msg['payload']['order_id']}")
mq.ack(msg)
print(f"After ack: {mq.get_stats()}")
print()


# Problem 6: Breadth-First Search (File System Search)
class FileSystem:
    """
    Search files in directory tree using BFS.
    Real-world use: File explorers, search tools
    """
    def __init__(self):
        self.tree = {}
    
    def add_directory(self, path: str, parent: str = "/"):
        """Add directory to filesystem"""
        if parent not in self.tree:
            self.tree[parent] = []
        self.tree[parent].append(path)
        if path not in self.tree:
            self.tree[path] = []
    
    def search_bfs(self, start: str, target: str) -> Optional[List[str]]:
        """Search for file/directory using BFS"""
        queue = deque([(start, [start])])
        visited = {start}
        
        while queue:
            current, path = queue.popleft()
            
            if current == target:
                return path
            
            for child in self.tree.get(current, []):
                if child not in visited:
                    visited.add(child)
                    queue.append((child, path + [child]))
        
        return None
    
    def list_all_files(self, start: str = "/") -> List[str]:
        """List all files under directory"""
        result = []
        queue = deque([start])
        
        while queue:
            current = queue.popleft()
            result.append(current)
            
            for child in self.tree.get(current, []):
                queue.append(child)
        
        return result

print("Problem 6: File System Search (BFS)")
fs = FileSystem()
fs.add_directory("/home", "/")
fs.add_directory("/home/user", "/home")
fs.add_directory("/home/user/documents", "/home/user")
fs.add_directory("/home/user/downloads", "/home/user")
path = fs.search_bfs("/", "/home/user/documents")
print(f"Path to documents: {' -> '.join(path) if path else 'Not found'}")
print(f"All files: {fs.list_all_files()}")
print()


# Problem 7: Cache with LRU Eviction
class LRUCache:
    """
    Least Recently Used cache implementation.
    Real-world use: Redis, CDNs, browser cache
    """
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = {}
        self.queue = deque()
    
    def get(self, key: str) -> Optional[any]:
        """Get value from cache"""
        if key not in self.cache:
            return None
        
        # Move to end (most recent)
        self.queue.remove(key)
        self.queue.append(key)
        return self.cache[key]
    
    def put(self, key: str, value: any) -> None:
        """Put value in cache"""
        if key in self.cache:
            self.queue.remove(key)
        elif len(self.cache) >= self.capacity:
            # Evict least recently used
            lru_key = self.queue.popleft()
            del self.cache[lru_key]
        
        self.cache[key] = value
        self.queue.append(key)
    
    def get_stats(self) -> dict:
        """Get cache statistics"""
        return {
            'size': len(self.cache),
            'capacity': self.capacity,
            'usage_percent': (len(self.cache) / self.capacity) * 100,
            'items': list(self.queue)
        }

print("Problem 7: LRU Cache")
cache = LRUCache(capacity=3)
cache.put("page1", "Homepage")
cache.put("page2", "Products")
cache.put("page3", "About")
print(f"Cache: {cache.get_stats()}")
cache.put("page4", "Contact")  # Should evict page1
print(f"After adding page4: {cache.get_stats()}")
cache.get("page2")  # Access page2
cache.put("page5", "Blog")  # Should evict page3 (not page2)
print(f"After adding page5: {cache.get_stats()}")
print()


# Problem 8: Event-Driven Simulation (Restaurant Queue)
class Restaurant:
    """
    Simulate restaurant customer queue.
    Real-world use: Queue management systems, simulations
    """
    def __init__(self, num_tables: int):
        self.num_tables = num_tables
        self.available_tables = num_tables
        self.waiting_queue = deque()
        self.seated_customers = []
        self.customer_id = 0
    
    def customer_arrives(self, party_size: int, name: str) -> dict:
        """Customer arrives at restaurant"""
        self.customer_id += 1
        customer = {
            'id': self.customer_id,
            'name': name,
            'party_size': party_size,
            'arrival_time': time.time(),
            'status': 'waiting'
        }
        
        if self.available_tables > 0:
            self._seat_customer(customer)
        else:
            self.waiting_queue.append(customer)
        
        return customer
    
    def _seat_customer(self, customer: dict) -> None:
        """Seat customer at table"""
        customer['status'] = 'seated'
        customer['seated_time'] = time.time()
        self.seated_customers.append(customer)
        self.available_tables -= 1
    
    def customer_leaves(self, customer_id: int) -> bool:
        """Customer finishes and leaves"""
        for i, customer in enumerate(self.seated_customers):
            if customer['id'] == customer_id:
                self.seated_customers.pop(i)
                self.available_tables += 1
                
                # Seat next waiting customer
                if self.waiting_queue:
                    next_customer = self.waiting_queue.popleft()
                    self._seat_customer(next_customer)
                
                return True
        return False
    
    def get_status(self) -> dict:
        """Get restaurant status"""
        return {
            'customers_waiting': len(self.waiting_queue),
            'tables_occupied': len(self.seated_customers),
            'tables_available': self.available_tables,
            'next_in_line': self.waiting_queue[0]['name'] if self.waiting_queue else None
        }

print("Problem 8: Restaurant Queue Simulation")
restaurant = Restaurant(num_tables=2)
restaurant.customer_arrives(4, "Smith family")
restaurant.customer_arrives(2, "Jones couple")
restaurant.customer_arrives(3, "Brown party")
print(f"Status: {restaurant.get_status()}")
restaurant.customer_leaves(1)
print(f"After Smith family leaves: {restaurant.get_status()}")
