# System Design Fundamentals

Core concepts that form the foundation of scalable system design.

---

## 📋 Table of Contents
1. [Performance vs Scalability](#performance-vs-scalability)
2. [Latency vs Throughput](#latency-vs-throughput)
3. [Horizontal vs Vertical Scaling](#horizontal-vs-vertical-scaling)
4. [Stateless vs Stateful Architecture](#stateless-vs-stateful-architecture)
5. [Back-of-the-Envelope Calculations](#back-of-the-envelope-calculations)

---

## Performance vs Scalability

### Performance Problem
**Definition:** System is slow for a single user.

**Characteristics:**
- Single request takes too long
- Poor resource utilization
- Inefficient algorithms
- Not optimized queries

**Solutions:**
- Optimize code and algorithms
- Add indexes to databases
- Reduce network calls
- Use efficient data structures
- Profile and identify bottlenecks

**Example:**
```
User makes a request → Takes 5 seconds to respond
Problem: The system itself is slow
```

### Scalability Problem
**Definition:** System is fast for one user but slow under load.

**Characteristics:**
- Works well with low traffic
- Degrades with more users
- Resource contention
- Bottlenecks under load

**Solutions:**
- Horizontal scaling (add more servers)
- Load balancing
- Caching
- Database replication
- Asynchronous processing

**Example:**
```
1 user → Fast (100ms)
1000 users → Slow (10 seconds)
Problem: System doesn't scale
```

### Key Insight
> **Performance** = How fast the system processes a single task  
> **Scalability** = How the system handles increased load

---

## Latency vs Throughput

### Latency
**Definition:** Time to perform an action or produce a result.

**Measured In:**
- Milliseconds (ms)
- Seconds (s)

**Types:**
- **Network Latency:** Time for data to travel
- **Processing Latency:** Time to process request
- **Database Latency:** Time for query execution

**Examples:**
```
API Response Time: 50ms
Database Query: 10ms
Network Round Trip: 100ms
```

**Factors Affecting Latency:**
- Physical distance (network hops)
- Server processing time
- Database query complexity
- Network bandwidth
- Queueing delays

### Throughput
**Definition:** Number of operations completed per unit time.

**Measured In:**
- Requests per second (RPS)
- Queries per second (QPS)
- Transactions per second (TPS)
- Bytes per second (Bps)

**Examples:**
```
API Server: 10,000 RPS
Database: 50,000 QPS
Network: 1 Gbps = 125 MB/s
```

**Factors Affecting Throughput:**
- Number of servers
- Parallel processing capability
- Resource contention
- Bottlenecks in the system

### The Trade-off

**Goal:** Maximize throughput with acceptable latency

**Relationship:**
- Low latency doesn't guarantee high throughput
- High throughput can increase latency (queueing)
- Optimize for what matters to your use case

**Use Cases:**
```
Low Latency Priority:
- Online gaming
- Real-time trading
- Video calls
- User interactions

High Throughput Priority:
- Batch processing
- Data analytics
- Log processing
- Background jobs
```

---

## Horizontal vs Vertical Scaling

### Vertical Scaling (Scale Up)
**Definition:** Add more resources to a single machine.

**Approach:**
- Increase CPU cores
- Add more RAM
- Use faster SSD/NVMe
- Upgrade network card

**Advantages:**
✅ Simple to implement  
✅ No code changes needed  
✅ Less operational complexity  
✅ Data consistency easier  
✅ No network latency between components  

**Disadvantages:**
❌ Hardware limits (can't scale infinitely)  
❌ Single point of failure  
❌ Downtime during upgrades  
❌ More expensive per unit  
❌ No redundancy  

**Example:**
```
Before: 4 CPU cores, 16GB RAM
After:  32 CPU cores, 256GB RAM

Use Cases:
- Databases requiring ACID
- Legacy applications
- Small to medium traffic
```

### Horizontal Scaling (Scale Out)
**Definition:** Add more machines to distribute load.

**Approach:**
- Add more servers
- Distribute requests
- Use load balancing
- Partition data

**Advantages:**
✅ Near-infinite scaling  
✅ High availability (redundancy)  
✅ Fault tolerance  
✅ Cost-effective (commodity hardware)  
✅ No downtime during scaling  

**Disadvantages:**
❌ Complex architecture  
❌ Requires load balancing  
❌ Data consistency challenges  
❌ Network overhead  
❌ Increased operational complexity  

**Example:**
```
Before: 1 server handling 1K RPS
After:  10 servers handling 10K RPS

Use Cases:
- Web applications
- Microservices
- High-traffic systems
- Cloud-native applications
```

### When to Use Each?

**Vertical Scaling:**
- Small to medium applications
- Databases (PostgreSQL, MySQL)
- Monolithic applications
- Quick initial solution
- Budget constraints initially

**Horizontal Scaling:**
- Large-scale applications
- Microservices architecture
- NoSQL databases (Cassandra, MongoDB)
- Cloud deployments
- Long-term growth strategy

---

## Stateless vs Stateful Architecture

### Stateless Services
**Definition:** Each request is independent; no session data stored on server.

**Characteristics:**
- No memory of previous requests
- Session data stored externally (cache, database)
- Any server can handle any request
- Easily scalable

**Advantages:**
✅ Easy horizontal scaling  
✅ Simple load balancing  
✅ High availability  
✅ Fault tolerance  
✅ No sticky sessions needed  

**Disadvantages:**
❌ External storage needed for sessions  
❌ Slight performance overhead (fetch session data)  
❌ More network calls  

**Example Architecture:**
```
User Request
    ↓
Load Balancer (Round Robin)
    ↓
Server 1, 2, or 3 (any server)
    ↓
Redis (shared session store)
    ↓
Database
```

**Code Example (Node.js):**
```javascript
// Stateless API - no server-side session storage
app.get('/api/user/:id', async (req, res) => {
  // Authenticate via JWT token (stateless)
  const token = req.headers.authorization;
  const user = verifyJWT(token);
  
  // Fetch data from database
  const data = await db.getUser(req.params.id);
  
  res.json(data);
  // No session data stored on this server
});
```

### Stateful Services
**Definition:** Server maintains session state between requests.

**Characteristics:**
- Remembers previous interactions
- Session data stored in server memory
- Requests must go to same server (sticky sessions)
- More complex to scale

**Advantages:**
✅ Better performance (data in memory)  
✅ Simpler application logic  
✅ Fewer external dependencies  
✅ Lower latency  

**Disadvantages:**
❌ Difficult to scale horizontally  
❌ Requires sticky sessions (load balancer complexity)  
❌ Single point of failure  
❌ Session loss if server crashes  
❌ Uneven load distribution  

**Example Architecture:**
```
User Request
    ↓
Load Balancer (Sticky Sessions)
    ↓
Same Server Every Time
    ↓
Server Memory (session data)
    ↓
Database
```

**Code Example (Node.js):**
```javascript
// Stateful API - server-side session storage
app.get('/api/cart', (req, res) => {
  // Session stored in server memory
  const cart = req.session.cart || [];
  
  res.json({ items: cart });
  // If user hits different server, session is lost
});
```

### Hybrid Approach
**Best Practice:** Stateless application tier with stateful data tier

```
Stateless Layer:
- API servers
- Web servers
- Microservices

Stateful Layer:
- Databases
- Cache (Redis)
- Message queues
```

---

## Back-of-the-Envelope Calculations

### Why Important?
- Understand system scale
- Make informed design decisions
- Identify bottlenecks early
- Estimate resource requirements

### Key Numbers to Remember

**Latencies:**
```
L1 cache reference:           0.5 ns
L2 cache reference:           7 ns
Main memory reference:        100 ns
SSD random read:              150 μs (150,000 ns)
Disk seek:                    10 ms (10,000,000 ns)
Network within datacenter:    0.5 ms
Network cross-continent:      150 ms
```

**Time Conversions:**
```
1 second = 1,000 milliseconds (ms)
1 millisecond = 1,000 microseconds (μs)
1 microsecond = 1,000 nanoseconds (ns)
```

**Data Sizes:**
```
1 Byte = 8 bits
1 KB = 1,024 Bytes ≈ 10³ bytes
1 MB = 1,024 KB ≈ 10⁶ bytes
1 GB = 1,024 MB ≈ 10⁹ bytes
1 TB = 1,024 GB ≈ 10¹² bytes
1 PB = 1,024 TB ≈ 10¹⁵ bytes
```

**Availability:**
```
99% (two 9s)    = 3.65 days downtime/year
99.9% (three 9s)  = 8.76 hours downtime/year
99.99% (four 9s)  = 52.6 minutes downtime/year
99.999% (five 9s) = 5.26 minutes downtime/year
```

### Calculation Examples

#### Example 1: Twitter-like System
**Requirements:**
- 300 million daily active users (DAU)
- Each user posts 2 tweets per day
- Each user views 50 tweets per day
- Each tweet is 280 characters (280 bytes)
- Keep tweets for 5 years

**Write Traffic:**
```
Write QPS = (300M users × 2 tweets) / 86,400 seconds
          = 600M / 86,400
          ≈ 7,000 writes/second

Peak QPS (assume 2x average) = 14,000 writes/second
```

**Read Traffic:**
```
Read QPS = (300M users × 50 tweets) / 86,400 seconds
         = 15B / 86,400
         ≈ 174,000 reads/second

Peak QPS = 348,000 reads/second
```

**Storage:**
```
Daily: 600M tweets × 280 bytes = 168 GB/day
5 years: 168 GB × 365 × 5 = 306 TB

With metadata (2x) = 612 TB
With replication (3x) = 1.8 PB
```

**Bandwidth:**
```
Write: 7K QPS × 280 bytes = 1.96 MB/s
Read: 174K QPS × 280 bytes = 48.7 MB/s
Total: ~50 MB/s ≈ 400 Mbps
```

#### Example 2: URL Shortener
**Requirements:**
- 100 million new URLs per month
- Read:Write ratio = 100:1
- Keep URLs for 10 years

**Write Traffic:**
```
Write QPS = 100M / (30 days × 86,400 seconds)
          = 100M / 2,592,000
          ≈ 40 writes/second
```

**Read Traffic:**
```
Read QPS = 40 × 100 = 4,000 reads/second
```

**Storage:**
```
Total URLs over 10 years:
= 100M/month × 12 months × 10 years
= 12 billion URLs

Per URL storage:
- Original URL: 500 bytes (average)
- Short code: 7 bytes
- Metadata: 100 bytes
Total: ~600 bytes

Total storage: 12B × 600 bytes = 7.2 TB
With overhead: ~10 TB
```

**Memory for Caching (80-20 rule):**
```
Daily reads: 4,000 × 86,400 = 345M reads
20% hot URLs: 345M × 0.2 = 69M URLs
Cache size: 69M × 600 bytes = 41.4 GB
```

#### Example 3: Video Streaming (YouTube-like)
**Requirements:**
- 1 billion users
- 5% upload videos daily
- Average video: 50 MB, 3 minutes
- Videos watched: 5 per user per day

**Upload Traffic:**
```
Daily uploads: 1B × 5% = 50M videos
Storage per day: 50M × 50 MB = 2.5 PB/day
Upload bandwidth: 2.5 PB / 86,400 = 29 GB/s
```

**View Traffic:**
```
Daily views: 1B × 5 = 5B views
Streaming bandwidth: 5B × 50 MB = 250 PB/day
                    = 250 PB / 86,400
                    = 2.9 TB/s
```

### Calculation Templates

**QPS Calculation:**
```
QPS = Daily Active Users × Actions per User / 86,400 seconds
Peak QPS = Average QPS × 2 (or more)
```

**Storage Calculation:**
```
Daily Storage = Records per Day × Size per Record
Annual Storage = Daily Storage × 365
With Replication = Annual Storage × Replication Factor
```

**Bandwidth Calculation:**
```
Bandwidth (Bps) = QPS × Average Request Size
Bandwidth (bps) = Bandwidth (Bps) × 8
```

**Memory Calculation:**
```
Cache Size = Hot Data Size
Hot Data (80-20 rule) = Total Data × 0.2
```

---

## 💡 Key Takeaways

1. **Performance ≠ Scalability:** A fast system isn't necessarily scalable
2. **Optimize for Your Use Case:** Low latency vs high throughput depends on needs
3. **Start Vertical, Think Horizontal:** Begin simple, scale as needed
4. **Stateless is Scalable:** Design stateless services for easy horizontal scaling
5. **Estimate Early:** Back-of-envelope calculations guide design decisions
6. **Trade-offs Everywhere:** Every decision has pros and cons

---

## 🎯 Interview Tips

When discussing fundamentals in interviews:

1. **Clarify Requirements:**
   - "Are we optimizing for latency or throughput?"
   - "What's the expected scale?"
   - "Is this read-heavy or write-heavy?"

2. **Show Calculations:**
   - Always do back-of-envelope math
   - State assumptions clearly
   - Round numbers for simplicity

3. **Discuss Trade-offs:**
   - "We could use vertical scaling initially, but horizontal for long-term growth"
   - "Stateless design enables easy scaling but requires external session storage"

4. **Scale Gradually:**
   - Start with simple design
   - Identify bottlenecks
   - Scale specific components

---

**Next:** [Availability & Reliability](02_availability_reliability.md)
