# Availability & Reliability

Understanding availability, consistency, and reliability patterns for distributed systems.

---

## 📋 Table of Contents
1. [CAP Theorem](#cap-theorem)
2. [Consistency Patterns](#consistency-patterns)
3. [Availability Patterns](#availability-patterns)
4. [Replication Strategies](#replication-strategies)
5. [Fault Tolerance](#fault-tolerance)

---

## CAP Theorem

### The Three Guarantees

**Consistency (C):**
- Every read receives the most recent write or an error
- All nodes see the same data at the same time
- Linearizability

**Availability (A):**
- Every request receives a response (success or failure)
- System is operational and responsive
- No guarantee it's the most recent data

**Partition Tolerance (P):**
- System continues despite network partitions
- Communication breaks between nodes
- Must be supported in distributed systems

### The Trade-off

**Key Insight:** In a distributed system, you can only guarantee **2 out of 3** properties.

Since network partitions **will** happen, you must choose between **C** and **A**.

```
Network is reliable → Can have C + A
Network has partitions → Choose C or A (must have P)
```

### CP Systems (Consistency + Partition Tolerance)

**Behavior:**
- Waits for partition to resolve before responding
- Returns error or timeout if data might be stale
- Sacrifices availability for consistency

**Use Cases:**
- Financial transactions
- Inventory management
- Banking systems
- Booking systems

**Examples:**
- MongoDB (with appropriate settings)
- HBase
- Redis (with specific configurations)
- Traditional RDBMS with strict ACID

**Example Scenario:**
```
Situation: Network partition between data centers

Response:
- Block writes to maintain consistency
- Return error: "Service temporarily unavailable"
- Wait until partition heals
- Ensure no conflicting updates

User Experience:
❌ "Error: Cannot process request. Please try again."
✅ When it works, data is always correct
```

### AP Systems (Availability + Partition Tolerance)

**Behavior:**
- Always accepts reads/writes
- Returns best available data (might be stale)
- Resolves conflicts later (eventual consistency)
- Sacrifices consistency for availability

**Use Cases:**
- Social media feeds
- View counts
- Analytics data
- Caching layers
- DNS

**Examples:**
- Cassandra
- DynamoDB
- Riak
- CouchDB

**Example Scenario:**
```
Situation: Network partition between data centers

Response:
- Continue accepting reads/writes
- Return potentially stale data
- Resolve conflicts after partition heals
- Use conflict resolution (last-write-wins, vector clocks)

User Experience:
✅ System always responds
❌ Might see slightly outdated data temporarily
```

### Choosing Between CP and AP

**Choose CP when:**
- Data correctness is critical
- Can tolerate downtime
- Strong consistency required
- Financial/booking systems

**Choose AP when:**
- Availability is critical
- Can tolerate eventual consistency
- User experience > perfect accuracy
- Social media, analytics

**Example Comparison:**

| Scenario | CP or AP? | Why? |
|----------|-----------|------|
| Bank account balance | CP | Must be accurate |
| Twitter follower count | AP | Slight delay acceptable |
| Seat booking | CP | No double-booking |
| Facebook likes | AP | Eventual consistency fine |
| Stock trading | CP | Accuracy critical |
| News feed | AP | Availability matters more |

---

## Consistency Patterns

### 1. Strong Consistency

**Definition:**
- After a write completes, all subsequent reads return that value
- Linearizability guarantee
- Most restrictive, highest latency

**How It Works:**
```
Write to Node A → Replicate to B, C, D → Confirm all synced → Return success
Read from any node → Always returns latest value
```

**Advantages:**
✅ Simple reasoning (like single database)  
✅ No conflicts  
✅ Always correct data  

**Disadvantages:**
❌ Higher latency (wait for all replicas)  
❌ Lower availability (if replica down, can't write)  
❌ Poor performance for geo-distributed systems  

**Use Cases:**
- Banking transactions
- Inventory systems
- Booking platforms
- ACID databases

**Implementation:**
- Synchronous replication
- Two-phase commit (2PC)
- Consensus algorithms (Paxos, Raft)

### 2. Eventual Consistency

**Definition:**
- After a write, replicas eventually converge
- Reads might return stale data temporarily
- Given enough time, all replicas will be consistent

**How It Works:**
```
Write to Node A → Return success immediately → Async replicate to B, C, D
Read from any node → Might get old value for brief period
Eventually → All nodes have same value
```

**Advantages:**
✅ High availability  
✅ Low latency  
✅ Works across geo-distributed systems  
✅ Can tolerate network partitions  

**Disadvantages:**
❌ Complex application logic  
❌ Temporary inconsistencies  
❌ Conflict resolution needed  

**Use Cases:**
- Social media feeds
- DNS
- Shopping cart (temporary)
- Analytics dashboards
- Caching layers

**Implementation:**
- Asynchronous replication
- Anti-entropy protocols
- Read repair
- Gossip protocols

### 3. Weak Consistency

**Definition:**
- No guarantee when read will see a write
- Best-effort approach
- Acceptable for certain use cases

**How It Works:**
```
Write → Might propagate, might not
Read → Get whatever is available
No guarantees on freshness
```

**Advantages:**
✅ Highest performance  
✅ Lowest latency  
✅ Maximum availability  

**Disadvantages:**
❌ No consistency guarantees  
❌ Data might be lost  
❌ Complex error handling  

**Use Cases:**
- Real-time multiplayer games
- Voice/video calls (VoIP)
- Live streaming
- Memcached
- Real-time analytics

### 4. Causal Consistency

**Definition:**
- Preserves causally related operations
- If A causes B, all nodes see A before B
- Concurrent operations can be seen differently

**Example:**
```
Good (causal order preserved):
User posts comment → Reply to comment
All users see: Post → Reply (in order)

Acceptable (concurrent):
User A posts → User B posts (different topics)
Some see: A → B
Others see: B → A
```

**Use Cases:**
- Social media comments/replies
- Collaborative editing
- Message threads

---

## Availability Patterns

### 1. Failover

**Definition:** Automatically switch to backup system when primary fails.

#### Active-Passive (Master-Slave)

**Architecture:**
```
Primary (Active)          Backup (Passive/Standby)
    ↓                            ↓
Handles all traffic       Monitors primary
                         Ready to take over
```

**How It Works:**
1. Primary handles all requests
2. Backup monitors primary via heartbeat
3. If heartbeat fails → Backup takes over
4. Backup assumes primary's IP address

**Advantages:**
✅ Simple architecture  
✅ Single source of truth  
✅ No split-brain problem  

**Disadvantages:**
❌ Passive node wastes resources  
❌ Failover time (30s - 2min)  
❌ Potential data loss if replication lagged  

**Use Cases:**
- Databases (PostgreSQL with streaming replication)
- Critical single services
- Stateful applications

#### Active-Active (Master-Master)

**Architecture:**
```
Primary 1 (Active)     Primary 2 (Active)
    ↓                      ↓
Both handle traffic    Both handle traffic
         ↓                 ↓
      Load Balancer
```

**How It Works:**
1. Both nodes actively handle traffic
2. Load balancer distributes requests
3. If one fails → Other handles 100% traffic
4. Bi-directional replication

**Advantages:**
✅ Better resource utilization  
✅ No failover delay  
✅ Higher throughput  

**Disadvantages:**
❌ Complex conflict resolution  
❌ Potential for split-brain  
❌ More difficult to manage  

**Use Cases:**
- Web/app servers (stateless)
- NoSQL databases
- High-traffic applications

### 2. Replication

**Definition:** Maintain multiple copies of data for availability and performance.

#### Benefits:
- **Availability:** If one node fails, others continue
- **Performance:** Read from nearest/least loaded node
- **Disaster Recovery:** Backup in different locations

#### Types:
See [Replication Strategies](#replication-strategies) section below.

### 3. Availability in Numbers

**Calculating Downtime:**

| Availability | Downtime per Year | Downtime per Month | Downtime per Week |
|--------------|-------------------|-------------------|-------------------|
| 90% (one 9) | 36.5 days | 3 days | 16.8 hours |
| 99% (two 9s) | 3.65 days | 7.2 hours | 1.68 hours |
| 99.9% (three 9s) | 8.76 hours | 43.8 minutes | 10.1 minutes |
| 99.99% (four 9s) | 52.6 minutes | 4.3 minutes | 1.01 minutes |
| 99.999% (five 9s) | 5.26 minutes | 25.9 seconds | 6.05 seconds |

**Calculating Combined Availability:**

**In Sequence (decreases):**
```
System A: 99.9% availability
System B: 99.9% availability
Combined: 99.9% × 99.9% = 99.8%

Formula: Total = A × B × C × ...
```

**In Parallel (increases):**
```
System A: 99.9% availability
System B: 99.9% availability
Combined: 1 - (1 - 0.999) × (1 - 0.999) = 99.9999%

Formula: Total = 1 - (1-A) × (1-B) × (1-C) × ...
```

**Example:**
```
Web Server → App Server → Database
(99.9%)      (99.9%)      (99.9%)

Sequential availability: 99.7%

With load balancer (2 app servers in parallel):
App tier: 1 - (0.001)² = 99.9999%
Total: 99.9% × 99.9999% × 99.9% = 99.8%
```

---

## Replication Strategies

### 1. Master-Slave (Primary-Replica)

**Architecture:**
```
     Master (Writes)
        ↓
    Replication
     ↙    ↓    ↘
Slave1  Slave2  Slave3
(Reads) (Reads) (Reads)
```

**Write Flow:**
1. All writes go to master
2. Master logs changes
3. Slaves replicate from master's log
4. Slaves become eventually consistent

**Read Flow:**
- Reads can go to master or any slave
- Slaves might have slightly stale data

**Advantages:**
✅ Simple architecture  
✅ Scales read traffic  
✅ Backup for disaster recovery  
✅ Analytics on slave without affecting master  

**Disadvantages:**
❌ Single point of failure (master)  
❌ Replication lag (seconds)  
❌ Doesn't scale writes  
❌ Manual failover often required  

**Use Cases:**
- MySQL, PostgreSQL
- MongoDB
- Redis
- Read-heavy applications

**Replication Modes:**

**Synchronous:**
```
Client → Master → Wait for Slave ACK → Respond to Client
Pros: No data loss
Cons: Higher latency, slave failure blocks writes
```

**Asynchronous:**
```
Client → Master → Respond to Client → Replicate to Slave
Pros: Lower latency
Cons: Potential data loss if master fails
```

**Semi-Synchronous:**
```
Wait for at least one slave ACK, others async
Balance between performance and durability
```

### 2. Master-Master (Multi-Master)

**Architecture:**
```
Master 1  ←→  Master 2
   ↓             ↓
Bidirectional Replication
```

**How It Works:**
- Both masters accept writes
- Changes replicate bi-directionally
- Conflict resolution required

**Advantages:**
✅ Scales writes  
✅ High availability (either can fail)  
✅ Better resource utilization  
✅ No failover needed  

**Disadvantages:**
❌ Complex conflict resolution  
❌ Potential for data conflicts  
❌ Difficult to maintain consistency  
❌ Split-brain scenarios  

**Conflict Resolution Strategies:**

**Last Write Wins (LWW):**
```
Both masters write to same key
Winner: Most recent timestamp
Problem: Clock skew, lost updates
```

**Version Vectors:**
```
Track causality of updates
Detect true conflicts
Application resolves conflicts
```

**Application-Level:**
```
Business logic determines resolution
Example: Shopping cart merge
```

**Use Cases:**
- Geo-distributed systems
- Cassandra, DynamoDB
- CouchDB
- Systems requiring high write availability

### 3. Leaderless Replication (Quorum)

**Architecture:**
```
    Client
  ↙  ↓  ↘
Node1 Node2 Node3
(All equal, no leader)
```

**How It Works:**
- Write to multiple nodes (W nodes)
- Read from multiple nodes (R nodes)
- Quorum: W + R > N (N = total nodes)

**Example (N=3, W=2, R=2):**
```
Write:
- Send to all 3 nodes
- Wait for 2 ACKs → Success
- 3rd updates eventually

Read:
- Query 2 nodes
- Return most recent value
- Guaranteed to get latest (W+R > N)
```

**Advantages:**
✅ No single point of failure  
✅ High availability  
✅ Tunable consistency  
✅ Handles network partitions well  

**Disadvantages:**
❌ Read/write latency (multiple nodes)  
❌ Complex conflict resolution  
❌ More network traffic  

**Quorum Configurations:**

```
Strong Consistency:
W + R > N
Example: N=5, W=3, R=3

High Availability Writes:
W=1, R=N
Fast writes, slower reads

High Availability Reads:
W=N, R=1
Fast reads, slower writes

Balanced:
W=R=(N+1)/2
```

**Use Cases:**
- Cassandra
- DynamoDB
- Riak
- Distributed databases

---

## Fault Tolerance

### Types of Failures

**Hardware Failures:**
- Server crashes
- Disk failures
- Network issues
- Power outages

**Software Failures:**
- Bugs and crashes
- Memory leaks
- Deadlocks
- Corrupted data

**Human Errors:**
- Misconfigurations
- Accidental deletions
- Deployment errors

### Fault Tolerance Techniques

#### 1. Redundancy

**Server Redundancy:**
```
Multiple servers behind load balancer
One fails → Others continue
```

**Data Redundancy:**
```
Replicate data across nodes
One node fails → Read from replicas
```

**Network Redundancy:**
```
Multiple network paths
Multiple data centers
```

#### 2. Health Checks

**Active Health Checks:**
```
Load balancer pings servers every 5 seconds
No response → Mark unhealthy → Stop sending traffic
Response returns → Mark healthy → Resume traffic
```

**Passive Health Checks:**
```
Monitor actual requests
Multiple failures → Mark unhealthy
Successful requests → Mark healthy
```

#### 3. Circuit Breaker Pattern

**States:**
```
Closed → Normal operation
Open → Failures detected, stop trying
Half-Open → Test if service recovered
```

**How It Works:**
```python
# Pseudocode
if circuit_breaker.is_open():
    return fallback_response()

try:
    response = call_service()
    circuit_breaker.record_success()
    return response
except ServiceError:
    circuit_breaker.record_failure()
    if circuit_breaker.should_open():
        circuit_breaker.open()
    return fallback_response()
```

#### 4. Graceful Degradation

**Concept:** System continues with reduced functionality

**Examples:**
```
Full service: HD video
Degraded: SD video
Worst case: Audio only

Full service: Personalized recommendations
Degraded: Popular items
Worst case: Static list
```

#### 5. Retry Logic

**Exponential Backoff:**
```python
def retry_with_backoff(func, max_retries=5):
    for attempt in range(max_retries):
        try:
            return func()
        except TransientError:
            if attempt == max_retries - 1:
                raise
            wait_time = (2 ** attempt) + random_jitter()
            sleep(wait_time)
```

**Retry Guidelines:**
- Retry transient errors (network, timeout)
- Don't retry client errors (400, 401, 404)
- Add jitter to prevent thundering herd
- Set maximum retry limit

---

## 💡 Key Takeaways

1. **CAP Theorem:** Choose consistency or availability during partitions
2. **Eventual Consistency:** Acceptable for many use cases, enables high availability
3. **Replication:** Multiple strategies with different trade-offs
4. **Availability Math:** Combined systems reduce availability (sequential)
5. **Fault Tolerance:** Assume failures will happen, design for resilience

---

## 🎯 Interview Tips

**Common Questions:**
- "How would you ensure 99.99% availability?"
- "What consistency model would you choose and why?"
- "How do you handle database replication lag?"

**Strong Answers:**
1. Explain trade-offs clearly
2. Match consistency to use case
3. Discuss failure scenarios
4. Quantify availability goals

**Example Response:**
```
"For a banking system, I'd choose CP (consistency over availability)
with master-slave replication and synchronous replication to at least
one replica. This ensures no data loss. We'd achieve 99.99% availability
through:
- Redundant servers in multiple AZs
- Automatic failover with health checks
- Circuit breakers for dependent services
- Regular disaster recovery testing"
```

---

**Next:** [Caching Strategies](03_caching.md)
