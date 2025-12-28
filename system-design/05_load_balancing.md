# Load Balancing

Distribute traffic across multiple servers for high availability and scalability.

---

## 📋 Table of Contents
1. [What is Load Balancing?](#what-is-load-balancing)
2. [Load Balancing Algorithms](#load-balancing-algorithms)
3. [Layer 4 vs Layer 7](#layer-4-vs-layer-7)
4. [Health Checks](#health-checks)
5. [Session Persistence](#session-persistence)
6. [DNS Load Balancing](#dns-load-balancing)
7. [Global Server Load Balancing](#global-server-load-balancing)

---

## What is Load Balancing?

### Purpose

**Problem:**
```
Single Server:
  - Handles 1,000 RPS
  - If it fails → Entire system down
  - Can't scale beyond hardware limits
```

**Solution:**
```
Load Balancer → distributes to 10 servers
  - Each handles 100 RPS
  - If one fails → 9 servers continue
  - Easy to add more servers
```

### Benefits

✅ **Scalability:** Add more servers to handle increased traffic  
✅ **High Availability:** No single point of failure  
✅ **Fault Tolerance:** Automatically route around failures  
✅ **Flexibility:** Rolling updates, maintenance without downtime  
✅ **Performance:** Optimize resource utilization  

### Architecture

```
                Client Requests
                      ↓
                Load Balancer
              ↙       ↓       ↘
         Server 1  Server 2  Server 3
            ↓         ↓         ↓
         Database  Database  Database
        (Replicas)
```

### Popular Load Balancers

**Hardware:**
- F5 Big-IP
- Citrix NetScaler
- A10 Networks

**Software:**
- Nginx
- HAProxy
- AWS ELB/ALB
- Google Cloud Load Balancer
- Traefik

---

## Load Balancing Algorithms

### 1. Round Robin

**Algorithm:** Distribute requests sequentially.

```
Request 1 → Server 1
Request 2 → Server 2
Request 3 → Server 3
Request 4 → Server 1 (cycle repeats)
```

**Implementation:**
```python
class RoundRobinLoadBalancer:
    def __init__(self, servers):
        self.servers = servers
        self.current = 0
    
    def get_server(self):
        server = self.servers[self.current]
        self.current = (self.current + 1) % len(self.servers)
        return server
```

**Advantages:**
✅ Simple implementation  
✅ Even distribution  
✅ No state required  

**Disadvantages:**
❌ Ignores server capacity  
❌ Ignores server load  
❌ Assumes all servers equal  

**Use Cases:**
- Servers with identical specs
- Stateless applications
- Development/testing

### 2. Weighted Round Robin

**Algorithm:** Distribute based on server capacity.

```
Server 1 (weight=3): ■ ■ ■
Server 2 (weight=2): ■ ■
Server 3 (weight=1): ■

Pattern: S1, S1, S1, S2, S2, S3
```

**Implementation:**
```python
class WeightedRoundRobin:
    def __init__(self, servers):
        # servers = [(server1, 3), (server2, 2), (server3, 1)]
        self.servers = []
        for server, weight in servers:
            self.servers.extend([server] * weight)
        self.current = 0
    
    def get_server(self):
        server = self.servers[self.current]
        self.current = (self.current + 1) % len(self.servers)
        return server
```

**Use Cases:**
- Mixed server capacities
- New server rollouts (gradually increase weight)
- A/B testing

### 3. Least Connections

**Algorithm:** Send to server with fewest active connections.

```
Server 1: 10 connections ✓ (chosen)
Server 2: 25 connections
Server 3: 18 connections
```

**Implementation:**
```python
class LeastConnectionsLoadBalancer:
    def __init__(self, servers):
        self.servers = servers
        self.connections = {server: 0 for server in servers}
    
    def get_server(self):
        return min(self.connections, key=self.connections.get)
    
    def on_request_start(self, server):
        self.connections[server] += 1
    
    def on_request_end(self, server):
        self.connections[server] -= 1
```

**Advantages:**
✅ Considers current load  
✅ Better for long-lived connections  
✅ Adapts to varying request times  

**Disadvantages:**
❌ More complex (track state)  
❌ Load balancer can be bottleneck  

**Use Cases:**
- WebSocket connections
- Database connections
- Long-running requests
- Varying request durations

### 4. Least Response Time

**Algorithm:** Send to server with lowest avg response time + fewest connections.

```
Server 1: 50ms avg, 10 connections → Score: 50ms
Server 2: 100ms avg, 5 connections → Score: 100ms
Server 3: 30ms avg, 8 connections → Score: 30ms ✓ (chosen)
```

**Advantages:**
✅ Performance-aware  
✅ Adapts to server health  

**Disadvantages:**
❌ Complex to implement  
❌ Requires monitoring  

**Use Cases:**
- Performance-critical applications
- Mixed workloads

### 5. IP Hash (Source IP)

**Algorithm:** Hash client IP to determine server.

```
client_ip = "192.168.1.100"
server_index = hash(client_ip) % num_servers
```

**Implementation:**
```python
class IPHashLoadBalancer:
    def __init__(self, servers):
        self.servers = servers
    
    def get_server(self, client_ip):
        hash_value = hash(client_ip)
        index = hash_value % len(self.servers)
        return self.servers[index]
```

**Advantages:**
✅ Sticky sessions (same client → same server)  
✅ Cache-friendly  
✅ No session state in load balancer  

**Disadvantages:**
❌ Uneven distribution (if few clients)  
❌ Adding/removing servers changes mapping  

**Use Cases:**
- Stateful applications
- Server-side caching
- WebSocket connections

### 6. Consistent Hashing

**Algorithm:** Use hash ring to minimize disruption when scaling.

```
Hash Ring: 0 ─────────────────────── 2^32
           ↑       ↑         ↑
        Server1  Server2  Server3

Client IP → Hash → Find next server clockwise
```

**Advantages:**
✅ Minimal remapping when scaling  
✅ Only K/n keys need remapping (K=keys, n=servers)  

**Implementation:**
```python
import hashlib
import bisect

class ConsistentHashLoadBalancer:
    def __init__(self, servers, virtual_nodes=150):
        self.ring = []
        self.ring_dict = {}
        
        for server in servers:
            for i in range(virtual_nodes):
                key = f"{server}:{i}"
                hash_value = int(hashlib.md5(key.encode()).hexdigest(), 16)
                self.ring.append(hash_value)
                self.ring_dict[hash_value] = server
        
        self.ring.sort()
    
    def get_server(self, key):
        hash_value = int(hashlib.md5(key.encode()).hexdigest(), 16)
        index = bisect.bisect_right(self.ring, hash_value)
        if index == len(self.ring):
            index = 0
        return self.ring_dict[self.ring[index]]
```

**Use Cases:**
- Distributed caching (Memcached, Redis cluster)
- Content delivery networks
- Scalable systems

### 7. Random

**Algorithm:** Select random server.

```python
import random

class RandomLoadBalancer:
    def __init__(self, servers):
        self.servers = servers
    
    def get_server(self):
        return random.choice(self.servers)
```

**Advantages:**
✅ Simple  
✅ Stateless  
✅ Good distribution over time  

**Disadvantages:**
❌ Not deterministic  
❌ Short-term imbalance possible  

**Use Cases:**
- Simple applications
- Failover backup algorithm

---

## Layer 4 vs Layer 7

### OSI Model Layers

```
Layer 7: Application (HTTP, HTTPS, FTP)
Layer 6: Presentation
Layer 5: Session
Layer 4: Transport (TCP, UDP)
Layer 3: Network (IP)
Layer 2: Data Link
Layer 1: Physical
```

### Layer 4 Load Balancing (Transport Layer)

**What it sees:**
- Source IP and Port
- Destination IP and Port
- TCP/UDP headers

**What it does:**
- Network Address Translation (NAT)
- Forward packets
- Cannot see application data

**Example:**
```
Client: 192.168.1.100:54321
   ↓
Load Balancer: 10.0.0.1:80
   ↓ (NAT)
Server: 10.0.1.50:8080

Load balancer doesn't know:
- HTTP method (GET, POST)
- URL path
- Headers or cookies
```

**Advantages:**
✅ Faster (less processing)  
✅ Lower latency  
✅ Protocol agnostic (HTTP, SMTP, FTP)  
✅ More efficient  

**Disadvantages:**
❌ No application awareness  
❌ Can't route based on content  
❌ Can't modify requests  
❌ Limited SSL termination  

**Use Cases:**
- High-performance requirements
- Non-HTTP protocols
- Simple forwarding

### Layer 7 Load Balancing (Application Layer)

**What it sees:**
- HTTP methods, URLs, headers
- Cookies
- Request/response content

**What it does:**
- Content-based routing
- SSL termination
- Request/response modification
- Caching

**Example Routing:**
```
Request: GET /api/users
   ↓
Load Balancer analyzes:
   - Path: /api/users
   - Method: GET
   - Header: Accept-Language: en
   ↓
Routes to: API Server Cluster

Request: GET /images/logo.png
   ↓
Routes to: Static File Server
```

**Implementation (Nginx):**
```nginx
http {
    upstream api_servers {
        server api1.example.com;
        server api2.example.com;
    }
    
    upstream web_servers {
        server web1.example.com;
        server web2.example.com;
    }
    
    server {
        listen 80;
        
        # Route API traffic
        location /api/ {
            proxy_pass http://api_servers;
        }
        
        # Route web traffic
        location / {
            proxy_pass http://web_servers;
        }
    }
}
```

**Advanced Routing:**
```nginx
# Route based on header
map $http_user_agent $backend {
    ~*Mobile mobile_servers;
    default  desktop_servers;
}

# Route based on cookie (A/B testing)
map $cookie_version $version {
    "v2" new_servers;
    default old_servers;
}

# Route based on geographic location
geo $geo {
    default us_servers;
    185.0.0.0/8 eu_servers;
    202.0.0.0/8 asia_servers;
}
```

**Advantages:**
✅ Content-based routing  
✅ SSL termination (offload from backend)  
✅ Request manipulation  
✅ Better caching  
✅ Security features (WAF)  

**Disadvantages:**
❌ Higher latency (more processing)  
❌ More CPU intensive  
❌ HTTP-specific  

**Use Cases:**
- Microservices (route by path)
- A/B testing (route by cookie)
- Mobile vs desktop (route by user-agent)
- Multi-tenancy (route by subdomain)

---

## Health Checks

### Purpose

Automatically detect and remove unhealthy servers from rotation.

### Types of Health Checks

#### 1. Active Health Checks

**Load balancer probes servers periodically:**

```
Every 5 seconds:
  Load Balancer → GET /health → Server
  
Response:
  200 OK → Server healthy
  Timeout / 5xx → Server unhealthy
```

**Configuration (HAProxy):**
```
backend api_servers
    server api1 10.0.1.1:8080 check inter 5s rise 2 fall 3
    server api2 10.0.1.2:8080 check inter 5s rise 2 fall 3
    
# inter: check interval
# rise: consecutive successes to mark healthy
# fall: consecutive failures to mark unhealthy
```

**Health Check Endpoint:**
```python
@app.route('/health')
def health_check():
    # Check database connection
    if not db.ping():
        return jsonify({"status": "unhealthy"}), 503
    
    # Check external dependencies
    if not redis.ping():
        return jsonify({"status": "unhealthy"}), 503
    
    return jsonify({"status": "healthy"}), 200
```

#### 2. Passive Health Checks

**Monitor actual traffic, not separate probes:**

```
Request succeeds → Server healthy
Request fails → Increment error count
Error count > threshold → Mark unhealthy
```

**Configuration (Nginx):**
```nginx
upstream backend {
    server server1.example.com max_fails=3 fail_timeout=30s;
    server server2.example.com max_fails=3 fail_timeout=30s;
}

# After 3 failures, mark unhealthy for 30 seconds
```

**Advantages:**
✅ No extra traffic  
✅ Detects real issues  
✅ Lower overhead  

**Disadvantages:**
❌ Slower detection  
❌ Requires traffic  

### Best Practices

1. **Check Dependencies:**
```python
def health_check():
    checks = {
        'database': check_database(),
        'cache': check_redis(),
        'external_api': check_external_api()
    }
    
    all_healthy = all(checks.values())
    status_code = 200 if all_healthy else 503
    
    return jsonify({
        'status': 'healthy' if all_healthy else 'unhealthy',
        'checks': checks
    }), status_code
```

2. **Use Appropriate Intervals:**
```
Critical services: 2-5 seconds
Standard services: 10-30 seconds
Background workers: 60 seconds
```

3. **Implement Graceful Degradation:**
```python
# Fail health check but keep serving requests briefly
# Allows connection draining before removal
```

---

## Session Persistence (Sticky Sessions)

### Problem

**Stateful applications store session data on server:**

```
User login → Server 1 (stores session)
Next request → Server 2 (no session) → User must login again ❌
```

### Solutions

#### 1. Cookie-Based Persistence

**Load balancer injects cookie:**

```
First Request:
  Client → Load Balancer → Server 1
  Response: Set-Cookie: SERVER=server1
  
Subsequent Requests:
  Client → Load Balancer (sees SERVER=server1) → Server 1
```

**Configuration (Nginx):**
```nginx
upstream backend {
    ip_hash;  # Simple IP-based stickiness
}

# Or more advanced:
upstream backend {
    server server1;
    server server2;
    sticky cookie srv_id expires=1h domain=.example.com path=/;
}
```

#### 2. IP Hash

**Hash client IP:**

```python
server = hash(client_ip) % num_servers
```

**Limitations:**
- Multiple users behind NAT → same server
- IP change → session lost

#### 3. External Session Store (Recommended)

**Store sessions externally:**

```
User login → Any Server → Store session in Redis
Next request → Any Server → Load session from Redis
```

**Implementation:**
```python
# Flask with Redis sessions
from flask import Flask, session
from flask_session import Session

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_REDIS'] = redis.StrictRedis(host='localhost')
Session(app)

@app.route('/login', methods=['POST'])
def login():
    # Session stored in Redis, not on server
    session['user_id'] = user.id
    return 'Logged in'

@app.route('/dashboard')
def dashboard():
    # Any server can load session from Redis
    user_id = session.get('user_id')
    return f'Dashboard for user {user_id}'
```

**Advantages:**
✅ Any server can handle any request  
✅ Easy horizontal scaling  
✅ Session survives server failure  

---

## DNS Load Balancing

### How it Works

**Multiple A records for same domain:**

```
Query: www.example.com
DNS Response:
  203.0.113.1
  203.0.113.2
  203.0.113.3

Client picks one (usually first)
```

**Configuration:**
```
# DNS zone file
www.example.com.  300  IN  A  203.0.113.1
www.example.com.  300  IN  A  203.0.113.2
www.example.com.  300  IN  A  203.0.113.3
```

### Round Robin DNS

**DNS returns IPs in rotating order:**

```
Request 1: [IP1, IP2, IP3]
Request 2: [IP2, IP3, IP1]
Request 3: [IP3, IP1, IP2]
```

### Advantages
✅ Simple  
✅ No single point of failure  
✅ Distributed globally  

### Disadvantages
❌ No health checks  
❌ Client caching (DNS TTL)  
❌ Uneven distribution  
❌ Can't detect server failures  

### Use Cases
- Geographic distribution
- Primary load distribution method
- Used with CDNs

---

## Global Server Load Balancing (GSLB)

### Purpose

Route users to nearest/best data center globally.

### Architecture

```
          User (London)
               ↓
       DNS / GSLB Service
         ↓           ↓
    EU Datacenter   US Datacenter
    (203.0.113.1)  (203.0.113.2)
         ↓
    Choose: EU (lower latency)
```

### Routing Methods

#### 1. Geographic Routing

```
User in US → US data center
User in EU → EU data center
User in Asia → Asia data center
```

#### 2. Latency-Based Routing

```
Measure latency from user to each data center
Choose data center with lowest latency
```

#### 3. Weighted Routing

```
US Data Center: 70% of traffic
EU Data Center: 30% of traffic

Useful for:
- Gradual rollouts
- Cost optimization
- Capacity management
```

#### 4. Failover Routing

```
Primary: US-East
Secondary: US-West (only if primary unhealthy)
```

### Implementation (AWS Route 53)

```json
{
  "Name": "www.example.com",
  "Type": "A",
  "SetIdentifier": "US-East",
  "GeoLocation": {
    "ContinentCode": "NA"
  },
  "ResourceRecords": [
    {"Value": "203.0.113.1"}
  ]
}
```

---

## 💡 Key Takeaways

1. **Choose Right Algorithm:** Round robin for simple, least connections for varying loads
2. **Health Checks Essential:** Automatically remove unhealthy servers
3. **Avoid Sticky Sessions:** Use external session store (Redis)
4. **Layer 7 for Routing:** Content-based routing for microservices
5. **GSLB for Global:** Route users to nearest data center
6. **Monitor Metrics:** Response time, error rate, traffic distribution

---

## 🎯 Interview Tips

**Common Questions:**
- "How would you implement load balancing for this system?"
- "What happens if a server fails?"
- "How do you handle sessions with multiple servers?"

**Strong Answer:**
"I'd use an Application Load Balancer (Layer 7) with least connections algorithm. Health checks every 5 seconds remove unhealthy servers. For sessions, I'd use Redis as an external session store to enable any server to handle any request. I'd start with 3 servers behind the load balancer and auto-scale based on CPU utilization."

---

**Next:** [Microservices & APIs](06_microservices_apis.md)
