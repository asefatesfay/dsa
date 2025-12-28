# Databases

Understanding database types, scaling strategies, and design patterns.

---

## 📋 Table of Contents
1. [SQL vs NoSQL](#sql-vs-nosql)
2. [Database Scaling Patterns](#database-scaling-patterns)
3. [SQL Database Concepts](#sql-database-concepts)
4. [NoSQL Database Types](#nosql-database-types)
5. [Database Selection Guide](#database-selection-guide)

---

## SQL vs NoSQL

### SQL (Relational Databases)

**Structure:**
- Tables with rows and columns
- Fixed schema
- Relationships via foreign keys
- ACID transactions

**Popular Databases:**
- PostgreSQL
- MySQL
- Oracle
- SQL Server
- MariaDB

**Advantages:**
✅ ACID guarantees (consistency)  
✅ Structured data with relationships  
✅ Complex queries with JOINs  
✅ Mature tools and ecosystem  
✅ Data integrity enforcement  
✅ Standardized query language (SQL)  

**Disadvantages:**
❌ Rigid schema (migrations required)  
❌ Vertical scaling limitations  
❌ Complex horizontal scaling  
❌ Performance issues with massive scale  

**Use Cases:**
- Financial systems (banking, payments)
- E-commerce (orders, inventory)
- CRM systems
- Traditional business applications
- Any application requiring ACID

### NoSQL (Non-Relational Databases)

**Structure:**
- Flexible schema
- Various data models (key-value, document, column, graph)
- Eventual consistency (typically)
- BASE properties

**Advantages:**
✅ Flexible schema  
✅ Horizontal scaling (sharding)  
✅ High performance for specific use cases  
✅ Handle unstructured data  
✅ Better for massive scale  

**Disadvantages:**
❌ Eventual consistency (by default)  
❌ No standardized query language  
❌ Limited JOIN support  
❌ Less mature ecosystem  
❌ Application-level data integrity  

---

## Database Scaling Patterns

### 1. Replication

**Master-Slave (Read Replicas):**

```
         Master (Write)
            ↓
     Async Replication
     ↙      ↓      ↘
Slave 1  Slave 2  Slave 3
(Read)   (Read)   (Read)
```

**Implementation:**
```sql
-- PostgreSQL replication setup
-- On master:
CREATE USER replicator REPLICATION LOGIN ENCRYPTED PASSWORD 'password';

-- On slave:
-- Set primary_conninfo in postgresql.conf
primary_conninfo = 'host=master port=5432 user=replicator password=password'
```

**Benefits:**
- Scale read traffic
- Backup/disaster recovery
- Analytics without affecting production
- Geographic distribution

**Challenges:**
- Replication lag (eventual consistency)
- Write scalability still limited
- Failover complexity

### 2. Sharding (Horizontal Partitioning)

**Concept:** Split data across multiple database servers.

**Sharding Strategies:**

#### A. Range-Based Sharding
```
Shard 1: Users A-J
Shard 2: Users K-T
Shard 3: Users U-Z
```

**Advantages:**
- Simple to implement
- Easy to add shards

**Disadvantages:**
- Uneven distribution (hotspots)
- Certain ranges get more traffic

#### B. Hash-Based Sharding
```
shard_id = hash(user_id) % num_shards

Example:
user_123 → hash(123) % 4 = 3 → Shard 3
user_456 → hash(456) % 4 = 0 → Shard 0
```

**Advantages:**
- Even distribution
- No hotspots

**Disadvantages:**
- Difficult to add/remove shards (rehashing)
- Range queries difficult

#### C. Consistent Hashing
```
Hash ring: 0 ───────────────────── 2^32-1
           ↑                      ↑
        Shard 1              Shard 2
           
Key maps to first shard clockwise
```

**Advantages:**
- Minimal data movement when scaling
- Even distribution

**Disadvantages:**
- More complex implementation

#### D. Geographic Sharding
```
US Users → US Database
EU Users → EU Database
Asia Users → Asia Database
```

**Advantages:**
- Lower latency (data near users)
- Compliance (GDPR)

**Disadvantages:**
- Cross-shard queries difficult
- Uneven distribution

**Implementation Example:**
```python
class ShardManager:
    def __init__(self, num_shards):
        self.num_shards = num_shards
        self.shards = [DatabaseConnection(f"shard_{i}") 
                       for i in range(num_shards)]
    
    def get_shard(self, user_id):
        shard_id = hash(user_id) % self.num_shards
        return self.shards[shard_id]
    
    def query_user(self, user_id):
        shard = self.get_shard(user_id)
        return shard.query("SELECT * FROM users WHERE id = ?", user_id)
    
    def query_all_users(self):
        # Fan-out query to all shards
        results = []
        for shard in self.shards:
            results.extend(shard.query("SELECT * FROM users"))
        return results
```

**Challenges with Sharding:**
- Cross-shard queries (JOINs)
- Cross-shard transactions
- Resharding (adding/removing shards)
- Uneven data distribution
- Increased operational complexity

### 3. Federation (Functional Partitioning)

**Concept:** Split databases by function/feature.

```
Users DB      Products DB    Orders DB
   ↓              ↓             ↓
user_service  product_service  order_service
```

**Benefits:**
- Independent scaling per service
- Clear boundaries
- Smaller databases (faster)
- Team ownership

**Challenges:**
- Cross-database queries
- Transactions across databases
- Data duplication

### 4. Denormalization

**Concept:** Add redundant data to avoid JOINs.

**Normalized (3NF):**
```sql
Orders Table:
order_id | user_id | product_id | quantity
1        | 100     | 500        | 2

Users Table:
user_id | name
100     | John

Products Table:
product_id | name    | price
500        | Widget  | 10.00

-- Query requires 2 JOINs
SELECT o.order_id, u.name, p.name, p.price, o.quantity
FROM orders o
JOIN users u ON o.user_id = u.user_id
JOIN products p ON o.product_id = p.product_id
```

**Denormalized:**
```sql
Orders Table:
order_id | user_id | user_name | product_id | product_name | price | quantity
1        | 100     | John      | 500        | Widget       | 10.00 | 2

-- Query: no JOINs needed
SELECT * FROM orders WHERE order_id = 1
```

**Trade-offs:**
- **Faster reads** (no JOINs)
- **Slower writes** (update multiple places)
- **More storage** (redundant data)
- **Consistency challenges** (keep copies in sync)

### 5. Database Connection Pooling

**Problem:** Creating database connections is expensive (100-300ms).

**Solution:** Reuse connections via pooling.

```python
# Without pooling (slow)
for request in requests:
    conn = create_db_connection()  # Expensive!
    result = conn.query("SELECT ...")
    conn.close()

# With pooling (fast)
pool = ConnectionPool(min=10, max=100)

for request in requests:
    conn = pool.get_connection()  # Fast (reuse)
    result = conn.query("SELECT ...")
    pool.release(conn)
```

**Configuration:**
```python
# PostgreSQL with psycopg2
pool = psycopg2.pool.ThreadedConnectionPool(
    minconn=10,    # Always keep 10 connections
    maxconn=100,   # Maximum 100 connections
    host='localhost',
    database='mydb'
)
```

**Benefits:**
- Lower latency (no connection overhead)
- Better resource utilization
- Handle traffic bursts

---

## SQL Database Concepts

### ACID Properties

**Atomicity:**
- Transaction is all-or-nothing
- If any part fails, entire transaction rolls back

```sql
BEGIN TRANSACTION;
UPDATE accounts SET balance = balance - 100 WHERE id = 1;  -- Debit
UPDATE accounts SET balance = balance + 100 WHERE id = 2;  -- Credit
-- If either fails, both rollback
COMMIT;
```

**Consistency:**
- Database remains in valid state
- Constraints always enforced

```sql
-- Balance cannot be negative
ALTER TABLE accounts ADD CONSTRAINT check_balance CHECK (balance >= 0);

-- This will fail if balance < 100
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
```

**Isolation:**
- Concurrent transactions don't interfere
- Appears as if transactions run sequentially

**Isolation Levels:**
```
READ UNCOMMITTED: Can read uncommitted changes (dirty reads)
READ COMMITTED:   Only read committed changes (most common)
REPEATABLE READ:  Same query returns same result
SERIALIZABLE:     Strongest isolation (like sequential execution)

Trade-off: Isolation ↑  Performance ↓
```

**Durability:**
- Committed data survives crashes
- Written to persistent storage (disk)

### Indexing

**B-Tree Index (Default):**
```sql
CREATE INDEX idx_users_email ON users(email);

-- Fast lookup
SELECT * FROM users WHERE email = 'john@example.com';
-- Uses index: O(log n)

-- Without index: O(n) full table scan
```

**Composite Index:**
```sql
CREATE INDEX idx_orders_user_date ON orders(user_id, created_at);

-- Uses index efficiently
SELECT * FROM orders WHERE user_id = 123 AND created_at > '2024-01-01';

-- Also uses index (leftmost prefix)
SELECT * FROM orders WHERE user_id = 123;

-- Doesn't use index (missing leftmost column)
SELECT * FROM orders WHERE created_at > '2024-01-01';
```

**Index Trade-offs:**
- **Faster reads:** O(log n) vs O(n)
- **Slower writes:** Must update index
- **More storage:** Index size ~= table size

**When to Index:**
✅ Columns in WHERE clauses  
✅ Columns in JOIN conditions  
✅ Columns in ORDER BY  
✅ Foreign keys  

**When NOT to Index:**
❌ Small tables (full scan is fast)  
❌ Columns with low cardinality (gender: M/F)  
❌ Write-heavy tables  
❌ Columns rarely queried  

### Query Optimization

**Example: Slow Query**
```sql
-- Slow: Full table scan + JOIN
SELECT u.name, COUNT(*) as order_count
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
WHERE u.created_at > '2024-01-01'
GROUP BY u.id
ORDER BY order_count DESC
LIMIT 10;
```

**Optimization Steps:**

1. **Add Index:**
```sql
CREATE INDEX idx_users_created ON users(created_at);
CREATE INDEX idx_orders_user ON orders(user_id);
```

2. **Use EXPLAIN:**
```sql
EXPLAIN ANALYZE
SELECT ...;

-- Look for:
-- - "Seq Scan" → needs index
-- - High "cost"
-- - Large "rows" estimates
```

3. **Rewrite Query:**
```sql
-- Better: Filter first, then JOIN
WITH active_users AS (
    SELECT id, name 
    FROM users 
    WHERE created_at > '2024-01-01'
)
SELECT u.name, COUNT(*) as order_count
FROM active_users u
LEFT JOIN orders o ON u.id = o.user_id
GROUP BY u.id
ORDER BY order_count DESC
LIMIT 10;
```

---

## NoSQL Database Types

### 1. Key-Value Stores

**Data Model:**
```
Key        →  Value
"user:123" →  {"name": "John", "email": "john@example.com"}
"session:abc" → "user_id=123&expires=..."
```

**Operations:**
```python
# Redis example
redis.set("user:123", json.dumps(user_data))
redis.get("user:123")
redis.delete("user:123")
redis.expire("session:abc", 3600)  # TTL
```

**Characteristics:**
- O(1) reads/writes
- Simple data model
- No complex queries
- Often in-memory

**Popular Databases:**
- Redis
- Memcached
- DynamoDB (also document)
- Riak

**Use Cases:**
- Caching
- Session storage
- Real-time analytics
- Leaderboards

### 2. Document Stores

**Data Model:**
```json
{
  "_id": "123",
  "name": "John Doe",
  "email": "john@example.com",
  "address": {
    "street": "123 Main St",
    "city": "NYC"
  },
  "orders": [
    {"id": "1", "total": 50.00},
    {"id": "2", "total": 75.00}
  ]
}
```

**Queries:**
```javascript
// MongoDB example
db.users.find({ "address.city": "NYC" })
db.users.find({ "orders.total": { $gt: 100 } })
db.users.updateOne(
  { "_id": "123" },
  { $push: { orders: newOrder } }
)
```

**Characteristics:**
- Flexible schema
- Nested documents
- Rich queries
- Secondary indexes

**Popular Databases:**
- MongoDB
- CouchDB
- Elasticsearch (search + document)
- DynamoDB

**Use Cases:**
- Content management
- User profiles
- Product catalogs
- Mobile app backends

### 3. Wide-Column Stores

**Data Model:**
```
Row Key: user_123
  Column Family: profile
    name: "John"
    email: "john@example.com"
  Column Family: activity
    last_login: "2024-01-15"
    total_orders: 42
```

**Characteristics:**
- Column-oriented storage
- Fast aggregations
- Compression
- Horizontal scaling

**Popular Databases:**
- Cassandra
- HBase
- BigTable (Google)

**Use Cases:**
- Time-series data
- Analytics
- IoT sensor data
- Event logging

**Example Query (Cassandra):**
```sql
CREATE TABLE users (
    user_id UUID PRIMARY KEY,
    name TEXT,
    email TEXT,
    created_at TIMESTAMP
);

-- Fast by primary key
SELECT * FROM users WHERE user_id = 123;

-- Requires secondary index or allows filtering
SELECT * FROM users WHERE name = 'John';
```

### 4. Graph Databases

**Data Model:**
```
Nodes: (Person), (Movie), (Company)
Edges: [:ACTED_IN], [:DIRECTED], [:WORKS_AT]

(John)-[:ACTED_IN]->(Movie1)
(John)-[:FRIENDS_WITH]->(Jane)
(Jane)-[:WORKS_AT]->(Company1)
```

**Queries (Neo4j Cypher):**
```cypher
// Find John's friends
MATCH (john:Person {name: 'John'})-[:FRIENDS_WITH]->(friend)
RETURN friend

// Find friends of friends
MATCH (john:Person {name: 'John'})-[:FRIENDS_WITH*2]->(fof)
RETURN fof

// Recommendation: movies friends watched
MATCH (john:Person {name: 'John'})-[:FRIENDS_WITH]->(friend)
      -[:WATCHED]->(movie)
WHERE NOT (john)-[:WATCHED]->(movie)
RETURN movie, COUNT(*) as friend_count
ORDER BY friend_count DESC
```

**Characteristics:**
- Native graph storage
- Fast traversals
- Relationship-focused
- Complex queries simplified

**Popular Databases:**
- Neo4j
- Amazon Neptune
- JanusGraph
- ArangoDB

**Use Cases:**
- Social networks
- Recommendation engines
- Fraud detection
- Knowledge graphs

---

## Database Selection Guide

### Decision Tree

```
Need ACID transactions? 
├─ YES → SQL (PostgreSQL, MySQL)
└─ NO → Continue

Need complex queries/JOINs?
├─ YES → SQL
└─ NO → Continue

Massive scale (billions of records)?
├─ YES → NoSQL
└─ NO → SQL works

Flexible schema needed?
├─ YES → NoSQL (MongoDB)
└─ NO → SQL

What's your access pattern?

├─ Key-value lookups → Redis, DynamoDB
├─ Document storage → MongoDB, CouchDB
├─ Time-series/Analytics → Cassandra, InfluxDB
├─ Graph relationships → Neo4j
└─ Full-text search → Elasticsearch
```

### Use Case Matrix

| Use Case | Best Database | Why |
|----------|---------------|-----|
| Banking | PostgreSQL | ACID, transactions |
| E-commerce | PostgreSQL + Redis | ACID + caching |
| Social Media Feed | Cassandra | Massive scale, writes |
| User Profiles | MongoDB | Flexible schema |
| Real-time Analytics | Cassandra | Time-series |
| Recommendation | Neo4j | Graph relationships |
| Search | Elasticsearch | Full-text search |
| Session Storage | Redis | Fast, TTL support |
| Content Management | MongoDB | Document model |
| IoT Sensors | InfluxDB | Time-series |

### Polyglot Persistence

**Concept:** Use multiple databases for different needs.

**Example E-commerce Architecture:**
```
User Service:
  - PostgreSQL (user accounts, ACID)
  - Redis (sessions, cache)

Product Service:
  - Elasticsearch (search)
  - MongoDB (product catalog)

Order Service:
  - PostgreSQL (orders, transactions)
  
Analytics:
  - Cassandra (clickstream, time-series)
  
Recommendations:
  - Neo4j (user-product graph)
```

---

## 💡 Key Takeaways

1. **SQL for ACID:** Use when consistency is critical
2. **NoSQL for Scale:** Use when horizontal scaling needed
3. **Shard Carefully:** Plan sharding strategy early
4. **Denormalize for Reads:** Trade storage for performance
5. **Index Wisely:** Balance read vs write performance
6. **Connection Pooling:** Always use for production
7. **Polyglot Persistence:** Different databases for different needs

---

## 🎯 Interview Tips

**Common Questions:**
- "SQL or NoSQL for this system?"
- "How would you scale the database?"
- "How do you handle transactions across services?"

**Strong Answer Framework:**
1. **Clarify requirements:** ACID needed? Scale? Access patterns?
2. **Start simple:** Single database initially
3. **Scale gradually:** Read replicas → Sharding
4. **Discuss trade-offs:** Consistency vs availability
5. **Mention monitoring:** Track query performance, slow queries

**Example:**
"For an e-commerce system, I'd use PostgreSQL for orders (ACID required) with read replicas for scaling reads. For product catalog, MongoDB works well due to flexible schema. I'd add Redis for caching frequently accessed products. As we scale, I'd shard users by user_id using consistent hashing to avoid hotspots."

---

**Next:** [Load Balancing](05_load_balancing.md)
