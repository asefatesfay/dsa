# Networking

Understanding networking is essential for designing distributed systems. This covers protocols, communication patterns, and network optimization.

---

## 🌐 OSI Model & TCP/IP

### OSI 7 Layers

```
┌────────────────────────────────────────────────────┐
│ Layer 7: Application (HTTP, DNS, FTP, SSH)         │ ← User applications
├────────────────────────────────────────────────────┤
│ Layer 6: Presentation (SSL/TLS, encryption)        │ ← Data formatting
├────────────────────────────────────────────────────┤
│ Layer 5: Session (APIs, sockets)                   │ ← Connection management
├────────────────────────────────────────────────────┤
│ Layer 4: Transport (TCP, UDP)                      │ ← End-to-end delivery
├────────────────────────────────────────────────────┤
│ Layer 3: Network (IP, routing)                     │ ← Routing between networks
├────────────────────────────────────────────────────┤
│ Layer 2: Data Link (Ethernet, MAC)                 │ ← Local network
├────────────────────────────────────────────────────┤
│ Layer 1: Physical (cables, signals)                │ ← Hardware
└────────────────────────────────────────────────────┘
```

**Practical TCP/IP Model (4 layers):**
```
Application Layer     → HTTP, DNS, SSH
Transport Layer       → TCP, UDP
Internet Layer        → IP, ICMP
Network Access Layer  → Ethernet, WiFi
```

---

## 📡 TCP vs UDP

### TCP (Transmission Control Protocol)

**Characteristics:**
- ✅ Reliable (guarantees delivery)
- ✅ Ordered (packets arrive in sequence)
- ✅ Connection-oriented (3-way handshake)
- ❌ Slower (overhead from reliability)
- ❌ More bandwidth (acknowledgments)

**3-Way Handshake:**
```
Client                Server
  │                     │
  │───── SYN ─────────▶│  1. Client: "Let's connect"
  │                     │
  │◀──── SYN-ACK ──────│  2. Server: "OK, ready"
  │                     │
  │───── ACK ─────────▶│  3. Client: "Confirmed"
  │                     │
  │◀═══ Data Flow ════▶│
```

**Use Cases:**
- ✅ Web browsing (HTTP/HTTPS)
- ✅ Email (SMTP, IMAP)
- ✅ File transfer (FTP, SSH)
- ✅ Database connections
- ✅ Any case where reliability is critical

**Example: TCP Socket (Python)**

```python
import socket

# TCP Server
def tcp_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 8080))
    server_socket.listen(5)
    
    print("TCP Server listening on port 8080...")
    
    while True:
        client_socket, address = server_socket.accept()
        print(f"Connection from {address}")
        
        # Receive data
        data = client_socket.recv(1024)
        print(f"Received: {data.decode()}")
        
        # Send response
        client_socket.send(b"Message received")
        client_socket.close()

# TCP Client
def tcp_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 8080))
    
    # Send data
    client_socket.send(b"Hello, Server!")
    
    # Receive response
    response = client_socket.recv(1024)
    print(f"Response: {response.decode()}")
    
    client_socket.close()
```

### UDP (User Datagram Protocol)

**Characteristics:**
- ✅ Fast (no handshake, no acknowledgments)
- ✅ Low latency
- ✅ Lightweight
- ❌ Unreliable (packets may be lost)
- ❌ Unordered (packets may arrive out of order)
- ❌ No congestion control

**Use Cases:**
- ✅ Video streaming (some packet loss OK)
- ✅ Gaming (low latency critical)
- ✅ VoIP (voice over IP)
- ✅ DNS queries (small, fast)
- ✅ IoT sensors (fire-and-forget)

**Example: UDP Socket (Python)**

```python
import socket

# UDP Server
def udp_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(('0.0.0.0', 8080))
    
    print("UDP Server listening on port 8080...")
    
    while True:
        # Receive data (no connection)
        data, address = server_socket.recvfrom(1024)
        print(f"Received from {address}: {data.decode()}")
        
        # Send response
        server_socket.sendto(b"Message received", address)

# UDP Client
def udp_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    # Send data (no connection)
    client_socket.sendto(b"Hello, Server!", ('localhost', 8080))
    
    # Receive response
    data, address = client_socket.recvfrom(1024)
    print(f"Response: {data.decode()}")
    
    client_socket.close()
```

### TCP vs UDP Comparison

| Feature | TCP | UDP |
|---------|-----|-----|
| **Reliability** | Guaranteed delivery | Best-effort |
| **Ordering** | In-order delivery | Out-of-order possible |
| **Speed** | Slower | Faster |
| **Overhead** | High (headers, ACKs) | Low (minimal headers) |
| **Connection** | Connection-oriented | Connectionless |
| **Use Case** | Reliability critical | Speed critical |
| **Examples** | HTTP, FTP, SSH | DNS, Streaming, Gaming |

---

## 🌍 HTTP/HTTPS

### HTTP (HyperText Transfer Protocol)

**Request-Response Model:**

```
Client                            Server
  │                                 │
  │──── HTTP Request ──────────────▶│
  │  GET /api/users HTTP/1.1        │
  │  Host: example.com              │
  │  Authorization: Bearer token    │
  │                                 │
  │◀─── HTTP Response ──────────────│
  │  HTTP/1.1 200 OK                │
  │  Content-Type: application/json │
  │  {"users": [...]}               │
  │                                 │
```

**HTTP Methods:**

```python
# GET - Retrieve data (idempotent, safe)
GET /api/users/123

# POST - Create resource (not idempotent)
POST /api/users
Body: {"name": "John", "email": "john@example.com"}

# PUT - Update entire resource (idempotent)
PUT /api/users/123
Body: {"name": "John Updated", "email": "john@example.com"}

# PATCH - Partial update (idempotent)
PATCH /api/users/123
Body: {"name": "John Updated"}

# DELETE - Delete resource (idempotent)
DELETE /api/users/123
```

**HTTP Status Codes:**
```
1xx Informational
  100 Continue - Server received headers, continue sending body

2xx Success
  200 OK - Request succeeded
  201 Created - Resource created
  204 No Content - Success, no body

3xx Redirection
  301 Moved Permanently - Resource moved
  302 Found - Temporary redirect
  304 Not Modified - Use cached version

4xx Client Errors
  400 Bad Request - Invalid request
  401 Unauthorized - Authentication required
  403 Forbidden - No permission
  404 Not Found - Resource doesn't exist
  429 Too Many Requests - Rate limited

5xx Server Errors
  500 Internal Server Error - Server error
  502 Bad Gateway - Upstream server error
  503 Service Unavailable - Server down
  504 Gateway Timeout - Upstream timeout
```

### HTTPS (HTTP Secure)

**TLS/SSL Encryption:**

```
Client                           Server
  │                                │
  │──── 1. Client Hello ─────────▶│
  │   (Supported ciphers)          │
  │                                │
  │◀─── 2. Server Hello ──────────│
  │   (Chosen cipher, certificate) │
  │                                │
  │──── 3. Verify Certificate ────│
  │   (Check CA, domain)           │
  │                                │
  │──── 4. Key Exchange ──────────▶│
  │   (Encrypted with public key)  │
  │                                │
  │◀═══ Encrypted Data Flow ═════▶│
```

**Certificate Example:**

```
Certificate:
  Domain: example.com
  Issuer: Let's Encrypt Authority
  Valid: 2024-01-01 to 2024-12-31
  Public Key: RSA 2048-bit
  
Verification:
  1. Browser checks certificate signature
  2. Verifies issuer (Let's Encrypt) is trusted CA
  3. Checks domain matches
  4. Validates not expired
```

**Setting up HTTPS (Nginx):**

```nginx
server {
    listen 443 ssl http2;
    server_name example.com;
    
    # SSL certificate
    ssl_certificate /etc/letsencrypt/live/example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/example.com/privkey.pem;
    
    # SSL settings
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;
    
    # HSTS (force HTTPS)
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    
    location / {
        proxy_pass http://localhost:3000;
    }
}

# Redirect HTTP to HTTPS
server {
    listen 80;
    server_name example.com;
    return 301 https://$server_name$request_uri;
}
```

### HTTP/1.1 vs HTTP/2 vs HTTP/3

```
HTTP/1.1:
  • One request per connection (or pipelining)
  • Head-of-line blocking
  • Text-based protocol
  • Max 6 concurrent connections per domain
  
HTTP/2:
  • Multiple requests over single connection (multiplexing)
  • Binary protocol (faster parsing)
  • Server push (proactive resource sending)
  • Header compression (HPACK)
  • No head-of-line blocking at HTTP layer
  • Still has TCP head-of-line blocking
  
HTTP/3:
  • Uses QUIC (over UDP, not TCP)
  • No TCP head-of-line blocking
  • Faster connection setup (0-RTT)
  • Better for mobile (connection migration)
  • Not yet universal support
```

---

## 🔌 WebSockets

Bi-directional, real-time communication over TCP.

### WebSocket vs HTTP

```
HTTP (Request-Response):
  Client ──request──▶ Server
  Client ◀─response── Server
  (Connection closes)
  
WebSocket (Persistent Connection):
  Client ──handshake──▶ Server
  Client ◀═══════════▶ Server (bidirectional)
  (Connection stays open)
```

**When to Use WebSockets:**
- ✅ Real-time chat
- ✅ Live notifications
- ✅ Collaborative editing
- ✅ Live sports scores
- ✅ Gaming
- ✅ Stock tickers

**WebSocket Example (Python):**

```python
# Server (using websockets library)
import asyncio
import websockets

connected_clients = set()

async def handler(websocket, path):
    # Register client
    connected_clients.add(websocket)
    
    try:
        async for message in websocket:
            print(f"Received: {message}")
            
            # Broadcast to all clients
            await asyncio.gather(
                *[client.send(f"User says: {message}") 
                  for client in connected_clients]
            )
    finally:
        # Unregister client
        connected_clients.remove(websocket)

async def main():
    async with websockets.serve(handler, "0.0.0.0", 8765):
        await asyncio.Future()  # Run forever

asyncio.run(main())

# Client
import asyncio
import websockets

async def client():
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        # Send message
        await websocket.send("Hello, Server!")
        
        # Receive messages
        async for message in websocket:
            print(f"Received: {message}")

asyncio.run(client())
```

**WebSocket Architecture:**

```
┌──────────┐         ┌──────────────┐
│ Client 1 │◀───────▶│              │
└──────────┘         │              │
                     │  WebSocket   │
┌──────────┐         │   Server     │
│ Client 2 │◀───────▶│  (pub/sub)   │
└──────────┘         │              │
                     │              │
┌──────────┐         │              │
│ Client 3 │◀───────▶│              │
└──────────┘         └──────────────┘

All clients receive messages in real-time
```

---

## 🚀 gRPC (Google Remote Procedure Call)

Binary protocol using HTTP/2 and Protocol Buffers.

### gRPC vs REST

| Feature | REST | gRPC |
|---------|------|------|
| Protocol | HTTP/1.1 | HTTP/2 |
| Data Format | JSON (text) | Protobuf (binary) |
| Performance | Slower | Faster (7-10x) |
| Streaming | No | Yes (4 types) |
| Browser Support | ✅ Full | ⚠️ Limited (gRPC-Web) |
| Human Readable | ✅ Yes | ❌ Binary |
| Code Generation | Manual | Auto-generated |
| Use Case | Public APIs | Internal microservices |

### gRPC Streaming Types

```
1. Unary (like REST):
   Client ──request──▶ Server
   Client ◀─response── Server

2. Server Streaming:
   Client ──request──▶ Server
   Client ◀─stream─── Server (multiple responses)

3. Client Streaming:
   Client ──stream───▶ Server (multiple requests)
   Client ◀─response── Server

4. Bidirectional Streaming:
   Client ◀═stream══▶ Server (both directions)
```

**Example: Stock Price Updates (Server Streaming)**

```protobuf
// stock.proto
syntax = "proto3";

service StockService {
  rpc StreamPrices (StockRequest) returns (stream StockPrice);
}

message StockRequest {
  repeated string symbols = 1;  // ["AAPL", "GOOGL"]
}

message StockPrice {
  string symbol = 1;
  double price = 2;
  int64 timestamp = 3;
}
```

```python
# Server
class StockService(stock_pb2_grpc.StockServiceServicer):
    def StreamPrices(self, request, context):
        # Stream prices every second
        while True:
            for symbol in request.symbols:
                price = get_current_price(symbol)
                yield stock_pb2.StockPrice(
                    symbol=symbol,
                    price=price,
                    timestamp=int(time.time())
                )
            time.sleep(1)

# Client
stub = stock_pb2_grpc.StockServiceStub(channel)
request = stock_pb2.StockRequest(symbols=['AAPL', 'GOOGL'])

for price_update in stub.StreamPrices(request):
    print(f"{price_update.symbol}: ${price_update.price}")
```

---

## 🌐 DNS (Domain Name System)

Translates domain names to IP addresses.

### DNS Resolution Process

```
1. User types: https://www.example.com
   
2. Browser checks cache:
   • Browser cache
   • OS cache
   
3. If not cached, query DNS:
   
   Browser ──────────▶ DNS Resolver (ISP)
                       │
                       ├─▶ Root DNS (.)
                       │   "Who handles .com?"
                       │
                       ├─▶ TLD DNS (.com)
                       │   "Who handles example.com?"
                       │
                       └─▶ Authoritative DNS (example.com)
                           "IP: 93.184.216.34"
   
   Browser ◀────────── IP Address
   
4. Browser connects to 93.184.216.34:443
```

### DNS Record Types

```
A Record (Address):
  example.com → 93.184.216.34 (IPv4)

AAAA Record:
  example.com → 2606:2800:220:1:248:1893:25c8:1946 (IPv6)

CNAME (Canonical Name):
  www.example.com → example.com (alias)
  
MX (Mail Exchange):
  example.com → mail.example.com (mail server)

TXT (Text):
  example.com → "v=spf1 include:_spf.google.com ~all" (verification)

NS (Name Server):
  example.com → ns1.cloudflare.com (authoritative DNS)
```

### DNS Configuration Example

```bash
# /etc/hosts (local DNS)
127.0.0.1   localhost
192.168.1.10   api.local
192.168.1.20   db.local

# Query DNS
dig example.com

# Output:
# example.com.  300  IN  A  93.184.216.34
#              (TTL)(Type)(IP)
```

**DNS Caching:**

```
Browser Cache:    1 minute
OS Cache:         1 minute
DNS Resolver:     1 hour (depends on TTL)
Root/TLD DNS:     48 hours

TTL (Time To Live):
  High (3600s = 1 hour): Stable IPs
  Low (60s = 1 minute): During migrations
```

---

## 🔐 Network Security

### Firewalls

```
┌─────────────────────────────────────┐
│           Firewall Rules            │
├─────────────────────────────────────┤
│                                     │
│ Allow:                              │
│  • Port 443 (HTTPS) from 0.0.0.0/0  │
│  • Port 80 (HTTP) from 0.0.0.0/0    │
│  • Port 22 (SSH) from 1.2.3.4/32    │
│  • Port 5432 (PostgreSQL) from VPC  │
│                                     │
│ Deny:                               │
│  • All other traffic                │
│                                     │
└─────────────────────────────────────┘
```

### VPC (Virtual Private Cloud)

```
┌────────────────────────────────────────────────┐
│              VPC (10.0.0.0/16)                 │
├────────────────────────────────────────────────┤
│                                                │
│  ┌──────────────────────────────────────────┐ │
│  │  Public Subnet (10.0.1.0/24)             │ │
│  │  • Internet Gateway                       │ │
│  │  • Load Balancer (10.0.1.10)             │ │
│  │  • Web Servers (10.0.1.20-30)            │ │
│  └──────────────────────────────────────────┘ │
│                                                │
│  ┌──────────────────────────────────────────┐ │
│  │  Private Subnet (10.0.2.0/24)            │ │
│  │  • NAT Gateway (for outbound traffic)     │ │
│  │  • App Servers (10.0.2.20-30)            │ │
│  │  • Databases (10.0.2.40-50)              │ │
│  └──────────────────────────────────────────┘ │
│                                                │
└────────────────────────────────────────────────┘

Public Subnet: Accessible from internet
Private Subnet: Only accessible within VPC
```

### DDoS Protection

**Types of DDoS:**
```
1. Volumetric (Layer 3/4):
   • Floods network with traffic
   • Example: UDP flood, SYN flood
   • Mitigation: Rate limiting, CloudFlare

2. Protocol (Layer 4):
   • Exploits protocol weaknesses
   • Example: SYN flood (half-open connections)
   • Mitigation: SYN cookies

3. Application (Layer 7):
   • Targets application logic
   • Example: HTTP GET flood
   • Mitigation: WAF, CAPTCHA, rate limiting
```

**Rate Limiting:**

```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["100 per hour", "10 per minute"]
)

@app.route('/api/expensive-operation')
@limiter.limit("5 per minute")
def expensive_operation():
    # Expensive computation
    pass
```

---

## 📈 Network Performance Optimization

### Connection Pooling

Reuse connections instead of creating new ones:

```python
import psycopg2
from psycopg2 import pool

# Create connection pool
db_pool = psycopg2.pool.SimpleConnectionPool(
    minconn=1,
    maxconn=20,
    host='db.example.com',
    database='mydb'
)

def query_database(sql):
    # Get connection from pool
    conn = db_pool.getconn()
    
    try:
        cursor = conn.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        return result
    finally:
        # Return connection to pool (don't close!)
        db_pool.putconn(conn)
```

**Benefits:**
- ✅ Faster (no handshake overhead)
- ✅ Lower latency (reuse existing connections)
- ✅ Lower resource usage (fewer connections)

### HTTP Keep-Alive

```python
import requests

# Without keep-alive (default in some libraries)
# Each request creates new TCP connection
for i in range(100):
    requests.get('https://api.example.com/data')
# 100 TCP handshakes = slow

# With keep-alive (session reuses connection)
session = requests.Session()
for i in range(100):
    session.get('https://api.example.com/data')
# 1 TCP handshake = fast
```

### Content Compression

```python
# Enable gzip compression
from flask import Flask
from flask_compress import Compress

app = Flask(__name__)
Compress(app)

@app.route('/api/data')
def get_data():
    # Response automatically compressed
    return jsonify({'data': large_dataset})

# Response headers:
# Content-Encoding: gzip
# Content-Length: 5000 (compressed, was 50000)
```

---

## 🎯 Interview Tips

**Key Points to Cover:**
1. ✅ TCP vs UDP (when to use each)
2. ✅ HTTP methods and status codes
3. ✅ HTTPS/TLS basics
4. ✅ WebSockets for real-time
5. ✅ DNS resolution process

**Common Questions:**
- "How does HTTPS work?" → TLS handshake, certificate verification
- "TCP vs UDP for video streaming?" → UDP (speed > reliability)
- "How would you implement real-time chat?" → WebSockets or polling
- "What happens when you type a URL?" → DNS → TCP → HTTP → rendering

**Red Flags:**
- ❌ Not understanding HTTP status codes
- ❌ Using HTTP instead of HTTPS
- ❌ Not considering network latency in design
- ❌ Ignoring connection pooling

---

**Next:** [Security](09_security.md)
