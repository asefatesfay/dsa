# Database Engineering

Database design, optimization, replication, and scaling for high-performance systems.

---

## 📋 Core Database Concepts

### 1. **SQL Query Optimization**

#### Index Strategies
```sql
-- Create indexes for frequently queried columns
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_orders_user_id ON orders(user_id);
CREATE INDEX idx_orders_created_at ON orders(created_at DESC);

-- Composite index for multiple columns (order matters!)
CREATE INDEX idx_orders_user_status ON orders(user_id, status, created_at DESC);

-- Covering index (includes all columns needed by query)
CREATE INDEX idx_orders_covering ON orders(user_id, status) 
INCLUDE (total_amount, created_at);

-- Partial index (only index subset of rows)
CREATE INDEX idx_active_users ON users(email) 
WHERE status = 'active';

-- Full-text search index
CREATE INDEX idx_products_search ON products 
USING GIN(to_tsvector('english', name || ' ' || description));
```

#### Query Optimization Examples
```sql
-- ❌ SLOW - Scans entire table
SELECT * FROM orders WHERE YEAR(created_at) = 2024;

-- ✅ FAST - Uses index on created_at
SELECT * FROM orders 
WHERE created_at >= '2024-01-01' 
  AND created_at < '2025-01-01';

-- ❌ SLOW - Function on indexed column prevents index use
SELECT * FROM users WHERE LOWER(email) = 'user@example.com';

-- ✅ FAST - Use functional index
CREATE INDEX idx_users_email_lower ON users(LOWER(email));
SELECT * FROM users WHERE LOWER(email) = 'user@example.com';

-- ❌ SLOW - OR conditions prevent index use
SELECT * FROM products 
WHERE category = 'electronics' OR category = 'computers';

-- ✅ FAST - Use IN clause
SELECT * FROM products 
WHERE category IN ('electronics', 'computers');

-- ❌ SLOW - SELECT *
SELECT * FROM orders o
JOIN users u ON o.user_id = u.id
WHERE u.email = 'user@example.com';

-- ✅ FAST - Select only needed columns
SELECT o.id, o.total_amount, o.created_at
FROM orders o
JOIN users u ON o.user_id = u.id
WHERE u.email = 'user@example.com';
```

#### EXPLAIN ANALYZE
```sql
-- Analyze query performance
EXPLAIN ANALYZE
SELECT u.name, COUNT(o.id) as order_count, SUM(o.total_amount) as total_spent
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
WHERE u.created_at >= '2024-01-01'
GROUP BY u.id, u.name
HAVING COUNT(o.id) > 5
ORDER BY total_spent DESC
LIMIT 10;

/*
Expected output shows:
- Execution time
- Index usage (Index Scan vs Seq Scan)
- Join methods (Hash Join, Nested Loop, Merge Join)
- Row estimates vs actual
- Buffer usage
*/
```

---

### 2. **Database Design Patterns**

#### Normalization
```sql
-- ❌ Denormalized (1NF violation - repeating groups)
CREATE TABLE orders_bad (
    order_id INT PRIMARY KEY,
    customer_name VARCHAR(100),
    product1 VARCHAR(100),
    price1 DECIMAL(10,2),
    product2 VARCHAR(100),
    price2 DECIMAL(10,2)
);

-- ✅ Properly normalized (3NF)
CREATE TABLE customers (
    customer_id SERIAL PRIMARY KEY,
    customer_name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    product_name VARCHAR(100) NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    category_id INT REFERENCES categories(category_id)
);

CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    customer_id INT REFERENCES customers(customer_id),
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) DEFAULT 'pending'
);

CREATE TABLE order_items (
    order_item_id SERIAL PRIMARY KEY,
    order_id INT REFERENCES orders(order_id),
    product_id INT REFERENCES products(product_id),
    quantity INT NOT NULL,
    unit_price DECIMAL(10,2) NOT NULL
);
```

#### Denormalization for Performance
```sql
-- Strategic denormalization: cache computed values
CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    customer_id INT REFERENCES customers(customer_id),
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    -- Denormalized fields (cached from order_items)
    total_items INT DEFAULT 0,
    total_amount DECIMAL(10,2) DEFAULT 0.00,
    status VARCHAR(20) DEFAULT 'pending'
);

-- Trigger to maintain denormalized data
CREATE OR REPLACE FUNCTION update_order_totals()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE orders
    SET 
        total_items = (
            SELECT COALESCE(SUM(quantity), 0)
            FROM order_items
            WHERE order_id = NEW.order_id
        ),
        total_amount = (
            SELECT COALESCE(SUM(quantity * unit_price), 0)
            FROM order_items
            WHERE order_id = NEW.order_id
        )
    WHERE order_id = NEW.order_id;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER order_items_after_insert_update
AFTER INSERT OR UPDATE ON order_items
FOR EACH ROW
EXECUTE FUNCTION update_order_totals();
```

---

### 3. **Transactions & Concurrency**

#### ACID Properties
```python
import psycopg2
from decimal import Decimal

def transfer_money(from_account_id: int, to_account_id: int, amount: Decimal):
    """
    Transfer money between accounts with ACID guarantees:
    - Atomicity: Either both debit and credit happen, or neither
    - Consistency: Account balances remain valid
    - Isolation: Concurrent transfers don't interfere
    - Durability: Committed transfers survive crashes
    """
    conn = psycopg2.connect(DATABASE_URL)
    
    try:
        with conn:
            with conn.cursor() as cur:
                # Set isolation level
                conn.set_isolation_level(
                    psycopg2.extensions.ISOLATION_LEVEL_SERIALIZABLE
                )
                
                # Check source account balance (with row lock)
                cur.execute("""
                    SELECT balance 
                    FROM accounts 
                    WHERE account_id = %s 
                    FOR UPDATE
                """, (from_account_id,))
                
                balance = cur.fetchone()[0]
                if balance < amount:
                    raise ValueError("Insufficient funds")
                
                # Debit from source
                cur.execute("""
                    UPDATE accounts 
                    SET balance = balance - %s,
                        updated_at = CURRENT_TIMESTAMP
                    WHERE account_id = %s
                """, (amount, from_account_id))
                
                # Credit to destination
                cur.execute("""
                    UPDATE accounts 
                    SET balance = balance + %s,
                        updated_at = CURRENT_TIMESTAMP
                    WHERE account_id = %s
                """, (amount, to_account_id))
                
                # Record transaction
                cur.execute("""
                    INSERT INTO transactions (from_account, to_account, amount, status)
                    VALUES (%s, %s, %s, 'completed')
                """, (from_account_id, to_account_id, amount))
                
                # Commit happens automatically at end of 'with' block
                
    except psycopg2.Error as e:
        # Rollback happens automatically on exception
        print(f"Transaction failed: {e}")
        raise
    finally:
        conn.close()
```

#### Isolation Levels
```sql
-- READ UNCOMMITTED (dirty reads possible)
SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED;

-- READ COMMITTED (default in PostgreSQL, prevents dirty reads)
SET TRANSACTION ISOLATION LEVEL READ COMMITTED;

-- REPEATABLE READ (prevents non-repeatable reads)
SET TRANSACTION ISOLATION LEVEL REPEATABLE READ;

-- SERIALIZABLE (strictest, prevents phantom reads)
SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;

-- Example: Prevent double booking with SERIALIZABLE
BEGIN TRANSACTION ISOLATION LEVEL SERIALIZABLE;

SELECT COUNT(*) FROM bookings 
WHERE room_id = 101 
  AND booking_date = '2024-12-30'
  AND status != 'cancelled';

-- If count = 0, room is available
INSERT INTO bookings (room_id, booking_date, guest_id, status)
VALUES (101, '2024-12-30', 12345, 'confirmed');

COMMIT;
```

#### Optimistic vs Pessimistic Locking
```sql
-- Pessimistic locking (FOR UPDATE)
BEGIN;
SELECT * FROM inventory WHERE product_id = 123 FOR UPDATE;
UPDATE inventory SET quantity = quantity - 5 WHERE product_id = 123;
COMMIT;

-- Optimistic locking (version column)
CREATE TABLE inventory (
    product_id INT PRIMARY KEY,
    quantity INT NOT NULL,
    version INT DEFAULT 0
);

-- Application code checks version
UPDATE inventory 
SET quantity = quantity - 5,
    version = version + 1
WHERE product_id = 123 
  AND version = 7;  -- Only update if version hasn't changed

-- Check affected rows; if 0, version changed (conflict)
```

---

### 4. **Replication & High Availability**

#### PostgreSQL Streaming Replication
```bash
# Primary server configuration (postgresql.conf)
wal_level = replica
max_wal_senders = 10
wal_keep_size = 1GB
synchronous_commit = on
synchronous_standby_names = 'replica1'

# pg_hba.conf (allow replication connections)
host replication replicator 10.0.1.0/24 md5
```

```bash
# Replica server setup
pg_basebackup -h primary.db.internal -D /var/lib/postgresql/data \
  -U replicator -v -P --wal-method=stream

# standby.signal file (marks as replica)
touch /var/lib/postgresql/data/standby.signal

# postgresql.conf on replica
primary_conninfo = 'host=primary.db.internal port=5432 user=replicator password=xxx'
hot_standby = on
```

#### Connection Pooling (PgBouncer)
```ini
; pgbouncer.ini
[databases]
mydb = host=localhost port=5432 dbname=mydb

[pgbouncer]
listen_addr = 0.0.0.0
listen_port = 6432
auth_type = md5
auth_file = /etc/pgbouncer/userlist.txt
pool_mode = transaction
max_client_conn = 1000
default_pool_size = 25
reserve_pool_size = 5
reserve_pool_timeout = 3
server_lifetime = 3600
server_idle_timeout = 600
```

---

### 5. **Sharding & Partitioning**

#### Table Partitioning
```sql
-- Range partitioning by date
CREATE TABLE orders (
    order_id BIGSERIAL,
    customer_id INT,
    order_date DATE NOT NULL,
    total_amount DECIMAL(10,2),
    status VARCHAR(20)
) PARTITION BY RANGE (order_date);

-- Create partitions
CREATE TABLE orders_2024_q1 PARTITION OF orders
    FOR VALUES FROM ('2024-01-01') TO ('2024-04-01');

CREATE TABLE orders_2024_q2 PARTITION OF orders
    FOR VALUES FROM ('2024-04-01') TO ('2024-07-01');

CREATE TABLE orders_2024_q3 PARTITION OF orders
    FOR VALUES FROM ('2024-07-01') TO ('2024-10-01');

CREATE TABLE orders_2024_q4 PARTITION OF orders
    FOR VALUES FROM ('2024-10-01') TO ('2025-01-01');

-- Indexes on partitions
CREATE INDEX ON orders_2024_q1 (customer_id);
CREATE INDEX ON orders_2024_q2 (customer_id);

-- Query automatically uses correct partition
SELECT * FROM orders WHERE order_date = '2024-06-15';
```

#### Hash Partitioning
```sql
-- Distribute users across shards by user_id hash
CREATE TABLE users (
    user_id BIGSERIAL,
    email VARCHAR(255),
    created_at TIMESTAMP
) PARTITION BY HASH (user_id);

CREATE TABLE users_0 PARTITION OF users
    FOR VALUES WITH (MODULUS 4, REMAINDER 0);

CREATE TABLE users_1 PARTITION OF users
    FOR VALUES WITH (MODULUS 4, REMAINDER 1);

CREATE TABLE users_2 PARTITION OF users
    FOR VALUES WITH (MODULUS 4, REMAINDER 2);

CREATE TABLE users_3 PARTITION OF users
    FOR VALUES WITH (MODULUS 4, REMAINDER 3);
```

---

### 6. **NoSQL Databases**

#### MongoDB Design Patterns
```javascript
// Embedding (1-to-few relationship)
{
  _id: ObjectId("..."),
  username: "john_doe",
  email: "john@example.com",
  addresses: [
    {
      type: "home",
      street: "123 Main St",
      city: "Seattle",
      zip: "98101"
    },
    {
      type: "work",
      street: "456 Office Blvd",
      city: "Seattle",
      zip: "98102"
    }
  ]
}

// Referencing (1-to-many relationship)
// User document
{
  _id: ObjectId("user123"),
  username: "john_doe",
  email: "john@example.com"
}

// Order documents (reference user)
{
  _id: ObjectId("order456"),
  user_id: ObjectId("user123"),
  items: [...],
  total: 99.99
}

// Indexing for performance
db.users.createIndex({ email: 1 }, { unique: true });
db.orders.createIndex({ user_id: 1, created_at: -1 });
db.products.createIndex({ name: "text", description: "text" });

// Aggregation pipeline
db.orders.aggregate([
  // Filter by date range
  {
    $match: {
      created_at: {
        $gte: ISODate("2024-01-01"),
        $lt: ISODate("2025-01-01")
      }
    }
  },
  // Join with users
  {
    $lookup: {
      from: "users",
      localField: "user_id",
      foreignField: "_id",
      as: "user"
    }
  },
  // Unwind array
  { $unwind: "$user" },
  // Group and calculate
  {
    $group: {
      _id: "$user_id",
      username: { $first: "$user.username" },
      total_orders: { $sum: 1 },
      total_spent: { $sum: "$total" }
    }
  },
  // Sort by total spent
  { $sort: { total_spent: -1 } },
  // Limit results
  { $limit: 10 }
]);
```

#### Redis Caching Patterns
```python
import redis
import json
from datetime import timedelta

r = redis.Redis(host='localhost', port=6379, db=0)

# Cache-aside pattern
def get_user(user_id: int):
    cache_key = f"user:{user_id}"
    
    # Try cache first
    cached = r.get(cache_key)
    if cached:
        return json.loads(cached)
    
    # Cache miss - fetch from database
    user = db.query(User).get(user_id)
    
    # Store in cache (expire after 1 hour)
    r.setex(cache_key, timedelta(hours=1), json.dumps(user.to_dict()))
    
    return user

# Write-through cache
def update_user(user_id: int, data: dict):
    # Update database
    db.query(User).filter_by(id=user_id).update(data)
    db.commit()
    
    # Update cache
    cache_key = f"user:{user_id}"
    user = db.query(User).get(user_id)
    r.setex(cache_key, timedelta(hours=1), json.dumps(user.to_dict()))

# Distributed locking
def acquire_lock(lock_name: str, timeout: int = 10):
    lock_key = f"lock:{lock_name}"
    identifier = str(uuid.uuid4())
    
    # Try to acquire lock with NX (only if not exists)
    acquired = r.set(lock_key, identifier, nx=True, ex=timeout)
    
    return identifier if acquired else None

def release_lock(lock_name: str, identifier: str):
    lock_key = f"lock:{lock_name}"
    
    # Use Lua script for atomic check-and-delete
    lua_script = """
    if redis.call("get", KEYS[1]) == ARGV[1] then
        return redis.call("del", KEYS[1])
    else
        return 0
    end
    """
    
    return r.eval(lua_script, 1, lock_key, identifier)

# Leaderboard with sorted sets
def add_score(user_id: int, score: int):
    r.zadd("leaderboard", {user_id: score})

def get_top_users(limit: int = 10):
    return r.zrevrange("leaderboard", 0, limit - 1, withscores=True)

def get_user_rank(user_id: int):
    return r.zrevrank("leaderboard", user_id)
```

---

## 🎯 Performance Benchmarking

### Load Testing with pgbench
```bash
# Initialize test database
pgbench -i -s 50 mydb

# Run benchmark (10 clients, 100 transactions each)
pgbench -c 10 -t 100 mydb

# Custom SQL script
cat > test.sql << EOF
\set user_id random(1, 1000000)
SELECT * FROM users WHERE user_id = :user_id;
EOF

pgbench -c 50 -T 60 -f test.sql mydb
```

---

## 🚫 Common Database Problems & Solutions

### Problem 1: Deadlocks

**Scenario:** E-commerce inventory system experiencing deadlocks

```sql
-- Transaction 1
BEGIN;
UPDATE inventory SET quantity = quantity - 1 WHERE product_id = 100;
UPDATE inventory SET quantity = quantity - 1 WHERE product_id = 200;
COMMIT;

-- Transaction 2 (running simultaneously)
BEGIN;
UPDATE inventory SET quantity = quantity - 1 WHERE product_id = 200;
UPDATE inventory SET quantity = quantity - 1 WHERE product_id = 100;
COMMIT;

-- Result: DEADLOCK!
```

**Solution:** Always acquire locks in consistent order

```sql
-- Both transactions now lock in ascending product_id order
BEGIN;
UPDATE inventory SET quantity = quantity - 1 
WHERE product_id IN (100, 200)
ORDER BY product_id;  -- Consistent lock ordering
COMMIT;
```

### Problem 2: Table Bloat

**Symptom:** Table size keeps growing even after deleting rows

```bash
# Check table bloat
SELECT 
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename) - 
                   pg_relation_size(schemaname||'.'||tablename)) AS bloat
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;
```

**Solution:**

```sql
-- Gentle approach (online, doesn't lock)
VACUUM ANALYZE photos;

-- Aggressive approach (locks table, reclaims space immediately)
VACUUM FULL photos;

-- Automate with pg_cron
CREATE EXTENSION pg_cron;
SELECT cron.schedule('vacuum-photos', '0 3 * * 0', 'VACUUM ANALYZE photos');
```

### Problem 3: Missing Index Detection

```sql
-- Find queries doing sequential scans
SELECT 
    schemaname,
    tablename,
    seq_scan,
    seq_tup_read,
    idx_scan,
    seq_tup_read / seq_scan as avg_seq_read
FROM pg_stat_user_tables
WHERE seq_scan > 0
ORDER BY seq_tup_read DESC
LIMIT 20;

-- Find unused indexes (candidates for removal)
SELECT 
    schemaname,
    tablename,
    indexname,
    idx_scan,
    pg_size_pretty(pg_relation_size(indexrelid)) as index_size
FROM pg_stat_user_indexes
WHERE idx_scan = 0
    AND indexrelname NOT LIKE '%pkey%'
ORDER BY pg_relation_size(indexrelid) DESC;
```

### Problem 4: Connection Pool Exhaustion

```python
# Bad: Creating connection per request
def get_user(user_id):
    conn = psycopg2.connect(DATABASE_URL)  # New connection every time!
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    user = cursor.fetchone()
    conn.close()
    return user

# Good: Use connection pooling
from psycopg2.pool import ThreadedConnectionPool

pool = ThreadedConnectionPool(
    minconn=5,
    maxconn=20,
    dsn=DATABASE_URL
)

def get_user(user_id):
    conn = pool.getconn()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        return cursor.fetchone()
    finally:
        pool.putconn(conn)

# Even better: Use SQLAlchemy with pool
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool

engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,  # Verify connection health
    pool_recycle=3600    # Recycle connections after 1 hour
)
```

### Problem 5: Slow COUNT(*) Queries

```sql
-- Slow on large tables (scans entire table)
SELECT COUNT(*) FROM users;  -- 30 seconds on 100M rows

-- Solution 1: Use approximate count
SELECT reltuples::bigint AS estimate
FROM pg_class
WHERE relname = 'users';  -- Instant, ~5% accuracy

-- Solution 2: Cache count in Redis
RED> INCR user_count  # When inserting user
RED> GET user_count   # When reading count

-- Solution 3: Maintain counter table
CREATE TABLE counters (
    table_name VARCHAR(50) PRIMARY KEY,
    count BIGINT DEFAULT 0,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE OR REPLACE FUNCTION update_user_count()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        UPDATE counters SET count = count + 1 WHERE table_name = 'users';
    ELSIF TG_OP = 'DELETE' THEN
        UPDATE counters SET count = count - 1 WHERE table_name = 'users';
    END IF;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;
```

---

## 🎯 Real Interview Questions

### Q1: Design a database schema for Twitter

**Requirements:**
- Users can post tweets (280 chars)
- Users can follow other users
- Users can like and retweet
- Feed shows tweets from followed users
- Handle 500M users, 500M tweets/day

**Answer:**

```sql
-- Users table (sharded by user_id)
CREATE TABLE users (
    user_id BIGSERIAL PRIMARY KEY,
    username VARCHAR(15) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    bio VARCHAR(160),
    follower_count INT DEFAULT 0,
    following_count INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Shard key for routing
    shard_id INT GENERATED ALWAYS AS (user_id % 64) STORED
);
CREATE INDEX idx_users_shard ON users(shard_id, user_id);

-- Tweets table (sharded by user_id for co-location)
CREATE TABLE tweets (
    tweet_id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL,
    content VARCHAR(280) NOT NULL,
    like_count INT DEFAULT 0,
    retweet_count INT DEFAULT 0,
    reply_count INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    shard_id INT GENERATED ALWAYS AS (user_id % 64) STORED
);
CREATE INDEX idx_tweets_user_time ON tweets(user_id, created_at DESC);
CREATE INDEX idx_tweets_shard ON tweets(shard_id, user_id);

-- Follows table (sharded by follower_id)
CREATE TABLE follows (
    follower_id BIGINT NOT NULL,
    following_id BIGINT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    PRIMARY KEY (follower_id, following_id),
    shard_id INT GENERATED ALWAYS AS (follower_id % 64) STORED
);
CREATE INDEX idx_follows_following ON follows(following_id, follower_id);

-- Likes table (Cassandra for write-heavy workload)
-- Schema in Cassandra:
CREATE TABLE likes (
    tweet_id BIGINT,
    user_id BIGINT,
    created_at TIMESTAMP,
    PRIMARY KEY (tweet_id, user_id)
) WITH CLUSTERING ORDER BY (user_id ASC);

-- Feed timeline (Redis Sorted Set)
-- Key: feed:{user_id}
-- Score: timestamp
-- Value: tweet_id

-- Example feed population (fan-out on write for users with <10K followers)
ZADD feed:12345 1640000000 tweet_100
ZADD feed:12345 1640000001 tweet_101
```

**Architecture Decision:**
- **Hot data (last 7 days):** PostgreSQL shards
- **Cold data (>7 days):** Cassandra or S3 + Athena
- **Feed cache:** Redis sorted sets
- **Celebrities (>1M followers):** Fan-out on read instead of write
- **Search:** Elasticsearch
- **Analytics:** Snowflake data warehouse

### Q2: How would you migrate 1TB database with zero downtime?

**Answer:**

```bash
# Phase 1: Set up replication (Debezium or AWS DMS)
# Old DB -> Kafka -> New DB

# Phase 2: Backfill historical data
pg_dump -h old-db -U admin -d mydb \
  --schema-only > schema.sql

psql -h new-db -U admin -d mydb < schema.sql

pg_dump -h old-db -U admin -d mydb \
  --data-only --disable-triggers \
  | psql -h new-db -U admin -d mydb

# Phase 3: Verify data consistency
SELECT COUNT(*), MAX(id), MIN(id), 
       SUM(CAST(id AS BIGINT)) as checksum
FROM users;
-- Compare results from both databases

# Phase 4: Dual writes
# Application writes to BOTH old and new DB
# Reads still from old DB

# Phase 5: Switch reads to new DB
# Monitor for 24-48 hours

# Phase 6: Decommission old DB
```

**Python Implementation:**

```python
class DualWriteDatabase:
    def __init__(self, old_db, new_db):
        self.old_db = old_db
        self.new_db = new_db
        self.write_to_new = True  # Feature flag
    
    def write(self, query, params):
        # Always write to old DB (source of truth)
        result = self.old_db.execute(query, params)
        
        if self.write_to_new:
            try:
                # Also write to new DB
                self.new_db.execute(query, params)
            except Exception as e:
                # Log error but don't fail request
                logger.error(f"New DB write failed: {e}")
        
        return result
    
    def read(self, query, params):
        # Read from old DB initially
        if not self.read_from_new:
            return self.old_db.execute(query, params)
        
        # After verification, switch to new DB
        return self.new_db.execute(query, params)
```

### Q3: Database is slow. How do you troubleshoot?

**Systematic Approach:**

```sql
-- Step 1: Check current queries
SELECT 
    pid,
    now() - query_start as duration,
    state,
    query
FROM pg_stat_activity
WHERE state != 'idle'
    AND query NOT ILIKE '%pg_stat_activity%'
ORDER BY duration DESC;

-- Step 2: Find blocking queries
SELECT 
    blocked_locks.pid AS blocked_pid,
    blocked_activity.usename AS blocked_user,
    blocking_locks.pid AS blocking_pid,
    blocking_activity.usename AS blocking_user,
    blocked_activity.query AS blocked_statement,
    blocking_activity.query AS blocking_statement
FROM pg_catalog.pg_locks blocked_locks
JOIN pg_catalog.pg_stat_activity blocked_activity ON blocked_activity.pid = blocked_locks.pid
JOIN pg_catalog.pg_locks blocking_locks ON blocking_locks.locktype = blocked_locks.locktype
JOIN pg_catalog.pg_stat_activity blocking_activity ON blocking_activity.pid = blocking_locks.pid
WHERE NOT blocked_locks.granted
    AND blocking_locks.granted;

-- Step 3: Check slow queries log
SELECT 
    calls,
    total_exec_time,
    mean_exec_time,
    max_exec_time,
    query
FROM pg_stat_statements
ORDER BY mean_exec_time DESC
LIMIT 20;

-- Step 4: Check table/index statistics
SELECT 
    schemaname,
    tablename,
    last_vacuum,
    last_autovacuum,
    last_analyze,
    last_autoanalyze,
    n_dead_tup
FROM pg_stat_user_tables
WHERE n_dead_tup > 10000
ORDER BY n_dead_tup DESC;

-- Step 5: Check cache hit ratio
SELECT 
    sum(heap_blks_read) as heap_read,
    sum(heap_blks_hit) as heap_hit,
    sum(heap_blks_hit) / (sum(heap_blks_hit) + sum(heap_blks_read)) as ratio
FROM pg_statio_user_tables;
-- Should be > 0.99 (99% cache hit rate)
```

**Checklist:**
1. ☐ Check CPU, memory, disk I/O on server
2. ☐ Identify slow queries with EXPLAIN ANALYZE
3. ☐ Check for missing indexes
4. ☐ Look for table bloat (vacuum needed)
5. ☐ Check connection pool settings
6. ☐ Verify cache hit ratio
7. ☐ Check for lock contention
8. ☐ Review recent config changes
9. ☐ Check application query patterns
10. ☐ Consider read replicas if read-heavy

---

## 📚 Learning Resources

**Books:**
- "Database Internals" - Alex Petrov
- "Designing Data-Intensive Applications" - Martin Kleppmann
- "High Performance MySQL" - Baron Schwartz

**Certifications:**
- MongoDB Certified Developer
- PostgreSQL Certified Professional
- AWS Certified Database - Specialty

**Practice:**
- Set up replication clusters
- Implement sharding strategies
- Optimize slow queries
- Design schema for high-scale applications
