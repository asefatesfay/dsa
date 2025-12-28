# Caching Strategies

Improve performance and reduce load using effective caching patterns.

---

## 📋 Table of Contents
1. [Why Caching?](#why-caching)
2. [Cache Levels](#cache-levels)
3. [Cache Update Strategies](#cache-update-strategies)
4. [Cache Eviction Policies](#cache-eviction-policies)
5. [Content Delivery Network (CDN)](#content-delivery-network-cdn)
6. [Common Pitfalls](#common-pitfalls)

---

## Why Caching?

### Benefits

**Performance:**
- **RAM vs Disk:** 100ns vs 10ms (100,000x faster)
- **Cache vs Database:** Single-digit ms vs 100+ ms
- **Reduces latency** for end users
- **Improves throughput** of the system

**Cost Reduction:**
- Fewer database queries → Lower DB costs
- Reduced bandwidth → Lower network costs
- Fewer backend servers needed

**Scalability:**
- Handle more requests with same infrastructure
- Absorb traffic spikes
- Reduce load on databases

### When to Use Caching

✅ **Good for Caching:**
- Frequently accessed data
- Expensive computations
- Rarely changing data
- Read-heavy workloads

❌ **Bad for Caching:**
- Frequently changing data
- Critical data requiring strong consistency
- Unique per-user data (large working set)
- Data larger than memory

### Cache Hit Ratio

**Formula:**
```
Cache Hit Ratio = Cache Hits / Total Requests

Example:
1000 requests, 800 from cache
Hit Ratio = 800/1000 = 80%
```

**Impact:**
```
Without Cache:
- All requests hit DB
- Latency: 100ms/request
- DB Load: 1000 QPS

With 80% Cache Hit:
- 800 from cache (5ms)
- 200 from DB (100ms)
- Average: (800×5 + 200×100)/1000 = 24ms
- DB Load: 200 QPS (5x reduction)
```

**Goal:** Aim for 80%+ cache hit ratio for most applications.

---

## Cache Levels

### 1. Client-Side Caching

**Location:** Browser, mobile app, client device

**Types:**
- **Browser Cache:** HTTP caching headers
- **Application Cache:** IndexedDB, LocalStorage
- **Service Workers:** Offline-first PWAs

**Advantages:**
✅ Fastest (no network call)  
✅ Reduces server load  
✅ Works offline  

**Disadvantages:**
❌ No control over client  
❌ Limited storage  
❌ Stale data risk  

**Example HTTP Headers:**
```http
# Cache for 1 hour
Cache-Control: public, max-age=3600

# Never cache (dynamic data)
Cache-Control: no-cache, no-store, must-revalidate

# Cache forever (with content hash in filename)
Cache-Control: public, max-age=31536000, immutable
```

**Use Cases:**
- Static assets (JS, CSS, images)
- Public data
- User preferences

### 2. CDN (Edge) Caching

**Location:** Edge servers close to users

**How It Works:**
```
User (London) → CDN Edge (London) → Origin (US)
                     ↓
                 Cache Hit!
                 (No origin call)
```

**Advantages:**
✅ Reduced latency (geographically close)  
✅ Reduced origin load  
✅ DDoS protection  
✅ High bandwidth  

**Disadvantages:**
❌ Cost  
❌ Cache invalidation complexity  
❌ Configuration complexity  

**Use Cases:**
- Static content (images, videos, CSS, JS)
- Public APIs
- Large files
- Popular content

**Popular CDNs:**
- CloudFlare
- AWS CloudFront
- Fastly
- Akamai

### 3. Web Server Caching

**Location:** Reverse proxy / Load balancer

**Technologies:**
- Varnish
- Nginx
- HAProxy

**How It Works:**
```
Client → Nginx (cache) → App Servers
              ↓
          Cache Hit
         (No app call)
```

**Advantages:**
✅ Reduce application load  
✅ SSL termination  
✅ Serve static files directly  

**Example Nginx Config:**
```nginx
proxy_cache_path /var/cache/nginx levels=1:2 keys_zone=my_cache:10m max_size=10g inactive=60m;

server {
    location /api/products {
        proxy_cache my_cache;
        proxy_cache_valid 200 60m;
        proxy_cache_use_stale error timeout updating;
        proxy_pass http://backend;
    }
}
```

### 4. Application-Level Caching

**Location:** In-memory cache within app servers

**Technologies:**
- Redis
- Memcached
- Application memory (HashMap)

**Advantages:**
✅ Full control over caching logic  
✅ Low latency  
✅ Flexible data structures (Redis)  

**Disadvantages:**
❌ Single point of failure (if not clustered)  
❌ Memory limitations  
❌ Cache warming required  

**Use Cases:**
- Session data
- User profiles
- Frequently accessed objects
- Computed results

### 5. Database Caching

**Location:** Database layer

**Types:**
- **Query Result Cache:** Cache query results
- **Buffer Pool:** Cache frequently accessed pages
- **Materialized Views:** Pre-computed query results

**MySQL Query Cache:**
```sql
# Caches identical queries
SELECT * FROM users WHERE id = 123;

# Invalidated when table changes
UPDATE users SET name = 'John' WHERE id = 123;
```

**Advantages:**
✅ Built-in (no additional infrastructure)  
✅ Automatically managed  

**Disadvantages:**
❌ Limited control  
❌ Invalidated on any table change  
❌ Can hurt performance if misused  

---

## Cache Update Strategies

### 1. Cache-Aside (Lazy Loading)

**How It Works:**
```
1. App checks cache
2. Cache miss → Load from DB
3. Store in cache
4. Return to client
```

**Read Flow:**
```python
def get_user(user_id):
    # Try cache first
    user = cache.get(f"user:{user_id}")
    
    if user is None:
        # Cache miss - load from database
        user = db.query("SELECT * FROM users WHERE id = ?", user_id)
        
        # Store in cache for next time
        if user:
            cache.set(f"user:{user_id}", user, ttl=3600)
    
    return user
```

**Write Flow:**
```python
def update_user(user_id, data):
    # Update database
    db.query("UPDATE users SET ... WHERE id = ?", user_id, data)
    
    # Invalidate cache
    cache.delete(f"user:{user_id}")
    
    # Next read will reload from DB
```

**Advantages:**
✅ Only cache requested data  
✅ Cache failures don't break the app  
✅ Simple to implement  

**Disadvantages:**
❌ Cache miss penalty (3 operations: check, query, set)  
❌ Stale data until TTL expires  
❌ Cold start problem  

**Use Cases:**
- Read-heavy workloads
- Most web applications
- User profiles, product catalogs

### 2. Write-Through

**How It Works:**
```
1. Write to cache and DB simultaneously
2. Only return success after both complete
```

**Write Flow:**
```python
def update_user(user_id, data):
    # Write to cache first
    cache.set(f"user:{user_id}", data)
    
    # Write to database (synchronous)
    db.query("UPDATE users SET ... WHERE id = ?", user_id, data)
    
    # Both must succeed
    return success
```

**Read Flow:**
```python
def get_user(user_id):
    # Always read from cache
    return cache.get(f"user:{user_id}")
```

**Advantages:**
✅ Cache always consistent with DB  
✅ No stale data  
✅ Read performance (always in cache)  

**Disadvantages:**
❌ Higher write latency (2 operations)  
❌ Wasted cache space (rarely accessed data)  
❌ Cache failure blocks writes  

**Use Cases:**
- Write-light, read-heavy
- Consistency critical
- Financial data

### 3. Write-Behind (Write-Back)

**How It Works:**
```
1. Write to cache immediately
2. Return success
3. Asynchronously write to DB (batched)
```

**Write Flow:**
```python
def update_user(user_id, data):
    # Write to cache
    cache.set(f"user:{user_id}", data)
    
    # Queue for async DB write
    write_queue.add({
        'type': 'update_user',
        'user_id': user_id,
        'data': data
    })
    
    return success  # Return immediately

# Background worker
def process_write_queue():
    while True:
        batch = write_queue.get_batch(100)
        db.batch_update(batch)
```

**Advantages:**
✅ Very fast writes  
✅ Batch writes to DB (efficient)  
✅ Reduces DB load  

**Disadvantages:**
❌ Risk of data loss (cache failure before DB write)  
❌ Complex to implement  
❌ Eventual consistency  

**Use Cases:**
- Write-heavy workloads
- Gaming (leaderboards, scores)
- Analytics (metrics, counters)
- Social media (likes, views)

### 4. Refresh-Ahead

**How It Works:**
```
1. Predict what will be accessed
2. Refresh cache before expiration
3. User always gets fresh data from cache
```

**Implementation:**
```python
def get_popular_products():
    products = cache.get("popular_products")
    
    # Check if about to expire (< 10% TTL remaining)
    ttl_remaining = cache.ttl("popular_products")
    if ttl_remaining < 360:  # < 10% of 1 hour
        # Trigger async refresh
        background_refresh("popular_products")
    
    return products

def background_refresh(key):
    # Load fresh data from DB
    data = db.query("SELECT * FROM products ORDER BY popularity DESC LIMIT 100")
    
    # Update cache
    cache.set(key, data, ttl=3600)
```

**Advantages:**
✅ Always low latency  
✅ No cache miss penalty  
✅ Reduced load on DB  

**Disadvantages:**
❌ Wasted resources if prediction wrong  
❌ Added complexity  
❌ Difficult to implement well  

**Use Cases:**
- Predictable access patterns
- Popular items (trending products)
- Dashboard data
- Homepage content

---

## Cache Eviction Policies

### Why Eviction?

Cache memory is limited. When full, decide which items to remove.

### 1. LRU (Least Recently Used)

**Algorithm:**
- Track last access time for each item
- Evict item that hasn't been accessed longest

**Data Structure:** HashMap + Doubly Linked List

**Time Complexity:** O(1) for get and put

**Implementation:**
```python
class LRUCache:
    def __init__(self, capacity):
        self.cache = {}  # key -> node
        self.capacity = capacity
        self.head = Node(0, 0)  # dummy head
        self.tail = Node(0, 0)  # dummy tail
        self.head.next = self.tail
        self.tail.prev = self.head
    
    def get(self, key):
        if key in self.cache:
            node = self.cache[key]
            self._remove(node)
            self._add(node)  # Move to head (most recent)
            return node.value
        return None
    
    def put(self, key, value):
        if key in self.cache:
            self._remove(self.cache[key])
        
        node = Node(key, value)
        self._add(node)
        self.cache[key] = node
        
        if len(self.cache) > self.capacity:
            # Remove LRU (tail)
            lru = self.tail.prev
            self._remove(lru)
            del self.cache[lru.key]
```

**Advantages:**
✅ Good for most use cases  
✅ Simple to understand  
✅ Adapts to access patterns  

**Disadvantages:**
❌ Doesn't consider frequency  
❌ One-time accesses pollute cache  

**Use Cases:**
- General purpose caching
- Redis default
- Most web applications

### 2. LFU (Least Frequently Used)

**Algorithm:**
- Track access count for each item
- Evict item with lowest access count

**Advantages:**
✅ Keeps popular items  
✅ Resists cache pollution  

**Disadvantages:**
❌ More complex  
❌ Doesn't adapt quickly to changing patterns  
❌ New items hard to cache  

**Use Cases:**
- Long-running caches
- Stable access patterns
- CDN caching

### 3. FIFO (First In First Out)

**Algorithm:**
- Evict oldest item regardless of usage

**Advantages:**
✅ Simple implementation  
✅ Fair eviction  

**Disadvantages:**
❌ Doesn't consider usage  
❌ Can evict frequently used items  

**Use Cases:**
- Simple caching scenarios
- Time-series data

### 4. TTL (Time To Live)

**Algorithm:**
- Each item has expiration time
- Automatically removed after TTL

**Implementation:**
```python
cache.set("user:123", user_data, ttl=3600)  # Expires in 1 hour
```

**Advantages:**
✅ Automatic invalidation  
✅ Prevents stale data  
✅ Simple to reason about  

**Disadvantages:**
❌ Popular items still expire  
❌ Thundering herd problem  

**Best Practice:** Combine with other policies (LRU + TTL)

---

## Content Delivery Network (CDN)

### What is a CDN?

**Definition:** Geographically distributed network of servers that cache content close to users.

### How CDN Works

```
User in Tokyo requests image
    ↓
CDN Edge Server (Tokyo)
    ↓
Cache Hit? → YES → Serve from Tokyo (10ms)
         → NO  → Fetch from Origin (US) (200ms)
                 Cache in Tokyo
                 Serve to user
                 Next request: Cache Hit!
```

### Push CDN

**Concept:** You upload content to CDN proactively

**Process:**
```
1. Build/deploy application
2. Upload assets to CDN
3. CDN distributes to edge servers
4. Content available globally
```

**Advantages:**
✅ Control over what's cached  
✅ Content immediately available  
✅ Good for infrequently changing content  

**Disadvantages:**
❌ Manual upload process  
❌ Storage costs even if not accessed  
❌ Need to manage versions  

**Use Cases:**
- Static websites
- Marketing sites
- Documentation
- Software downloads

### Pull CDN

**Concept:** CDN fetches content on first request

**Process:**
```
1. User requests content
2. CDN checks cache
3. If miss → Fetch from origin
4. Cache and serve
5. Subsequent requests: Cache hit
```

**Advantages:**
✅ Automatic caching  
✅ Only caches popular content  
✅ Less storage costs  

**Disadvantages:**
❌ First request slower (cache miss)  
❌ Origin must be accessible  

**Use Cases:**
- Dynamic websites
- User-generated content
- High-traffic applications

### CDN Caching Strategies

**Cache Headers:**
```http
# Cache static assets forever (with versioned filenames)
Cache-Control: public, max-age=31536000, immutable
# File: style.abc123.css

# Cache but revalidate
Cache-Control: public, max-age=3600, must-revalidate

# Don't cache
Cache-Control: no-store, no-cache
```

**Cache Key:**
```
Default: URL
Custom: URL + Query params + Headers + Cookies

Example:
URL: /api/products
Query: ?category=electronics&page=1
Header: Accept-Language: en
Cache Key: /api/products?category=electronics&page=1&lang=en
```

**Cache Invalidation:**
```
1. Purge: Delete from cache immediately
2. Refresh: Fetch fresh copy from origin
3. Ban: Invalidate by pattern (e.g., /images/*)
4. TTL Expiration: Wait for natural expiration
```

---

## Common Pitfalls

### 1. Cache Stampede (Thundering Herd)

**Problem:**
```
1. Popular item expires
2. 1000 requests hit at once
3. All miss cache
4. All query DB simultaneously
5. DB overloaded
```

**Solution: Cache Locking**
```python
def get_with_lock(key):
    value = cache.get(key)
    if value is not None:
        return value
    
    # Try to acquire lock
    if cache.set_nx(f"lock:{key}", "1", ttl=10):
        # Got lock - fetch from DB
        value = db.query(key)
        cache.set(key, value, ttl=3600)
        cache.delete(f"lock:{key}")
        return value
    else:
        # Someone else fetching - wait and retry
        time.sleep(0.1)
        return get_with_lock(key)
```

**Solution: Probabilistic Early Expiration:**
```python
def get_with_early_refresh(key, ttl=3600):
    value, expiry = cache.get_with_expiry(key)
    
    if value is None:
        return refresh_cache(key, ttl)
    
    # Probabilistically refresh before expiration
    time_left = expiry - time.now()
    if random() < 1.0 - (time_left / ttl):
        # Refresh in background
        background_refresh(key, ttl)
    
    return value
```

### 2. Cache Penetration

**Problem:**
```
Attacker requests non-existent keys
→ Always cache miss
→ Always hits DB
→ DB overloaded
```

**Solution: Cache Null Values**
```python
def get_user(user_id):
    user = cache.get(f"user:{user_id}")
    
    if user == "NULL":  # Cached null
        return None
    
    if user is None:
        user = db.query("SELECT * FROM users WHERE id = ?", user_id)
        if user is None:
            # Cache the fact that user doesn't exist
            cache.set(f"user:{user_id}", "NULL", ttl=60)
        else:
            cache.set(f"user:{user_id}", user, ttl=3600)
    
    return user
```

**Solution: Bloom Filter**
```python
# Check if key might exist before querying
if not bloom_filter.might_contain(user_id):
    return None  # Definitely doesn't exist

# Might exist - check cache/DB
return get_user(user_id)
```

### 3. Stale Data

**Problem:** Cache serves outdated data after DB update

**Solution: Cache Invalidation**
```python
def update_user(user_id, data):
    # Update DB
    db.query("UPDATE users SET ... WHERE id = ?", user_id, data)
    
    # Invalidate cache
    cache.delete(f"user:{user_id}")
    
    # Or update cache immediately
    # cache.set(f"user:{user_id}", data, ttl=3600)
```

**Solution: TTL**
```python
# Set appropriate TTL based on data freshness requirements
cache.set(key, value, ttl=300)  # 5 minutes for frequently changing
cache.set(key, value, ttl=86400)  # 24 hours for stable data
```

### 4. Cache Size Issues

**Problem:** Cache grows too large, evicts important data

**Solution: Partition by Type**
```
User Cache: Max 1GB, LRU
Product Cache: Max 5GB, LRU
Session Cache: Max 2GB, TTL
```

**Solution: Monitor Hit Ratio**
```python
# If hit ratio drops, increase cache size or optimize
hit_ratio = cache_hits / total_requests
if hit_ratio < 0.7:
    alert("Cache hit ratio low!")
```

---

## 💡 Key Takeaways

1. **Cache Everywhere:** Client, CDN, server, app, database
2. **Pick Right Strategy:** Cache-aside for most cases, write-through for consistency
3. **Eviction Policy Matters:** LRU for general use, combine with TTL
4. **Invalidation is Hard:** Simplest approach: delete on write
5. **Monitor Hit Ratio:** Aim for 80%+ for good ROI
6. **Handle Edge Cases:** Stampede, penetration, stale data

---

## 🎯 Interview Tips

**Common Questions:**
- "How would you implement caching for this system?"
- "What caching strategy would you use?"
- "How do you handle cache invalidation?"

**Strong Answer Template:**
```
1. Identify what to cache (frequently accessed, expensive)
2. Choose caching layer (CDN, Redis, etc.)
3. Pick update strategy (cache-aside, write-through)
4. Handle invalidation (TTL, explicit delete)
5. Monitor metrics (hit ratio, latency)
6. Discuss trade-offs (consistency vs performance)
```

---

**Next:** [Databases](04_databases.md)
