# Design Rate Limiter

Design a rate limiting system to control API request rates per user/IP.

---

## 📋 Requirements

### Functional Requirements
1. **Rate Limiting:** Limit requests per user/IP
2. **Multiple Rules:** Different limits for different endpoints
3. **Time Windows:** Per second, minute, hour, day
4. **Distributed:** Work across multiple servers
5. **Response Headers:** Return limit info in headers
6. **Flexible:** Easy to configure and update rules

### Non-Functional Requirements
1. **Low Latency:** < 10ms overhead
2. **High Throughput:** Handle millions of requests/sec
3. **Accurate:** No significant over/under counting
4. **Fault Tolerant:** Continue working if nodes fail
5. **Scalable:** Horizontal scaling

---

## 📊 Capacity Estimation

### Traffic

```
API requests: 10 million/second
Rate limit checks: 10M/sec (one per request)

Per check:
  • Key: 50 bytes (user_id or IP)
  • Counter data: 16 bytes
  • Metadata: 16 bytes
  Total: ~82 bytes

Memory (Redis):
  Active users: 10 million
  Memory: 10M × 82 bytes = 820 MB
```

### Response Time

```
Target latency: < 10ms per check
Redis latency: 1-2ms (in-memory)
Network latency: 1-3ms
Processing: 1-2ms
Total: ~5-7ms ✅
```

---

## 🏗️ Algorithms

### 1. Fixed Window Counter

**Concept:**
- Divide time into fixed windows (e.g., 1 minute)
- Count requests in current window
- Reset counter at window boundary

**Implementation:**

```python
import redis
import time

class FixedWindowRateLimiter:
    def __init__(self, redis_client):
        self.redis = redis_client
    
    def is_allowed(self, user_id, limit=100, window_seconds=60):
        """
        Check if request is allowed
        
        Args:
            user_id: Unique identifier
            limit: Max requests per window
            window_seconds: Window size in seconds
        
        Returns:
            (allowed, remaining, reset_time)
        """
        # Current window timestamp
        current_window = int(time.time() / window_seconds)
        
        # Key for this window
        key = f'rate_limit:{user_id}:{current_window}'
        
        # Get current count
        count = self.redis.get(key)
        
        if count is None:
            # First request in this window
            self.redis.setex(key, window_seconds, 1)
            return (True, limit - 1, (current_window + 1) * window_seconds)
        
        count = int(count)
        
        if count < limit:
            # Increment counter
            self.redis.incr(key)
            return (True, limit - count - 1, (current_window + 1) * window_seconds)
        
        # Rate limit exceeded
        return (False, 0, (current_window + 1) * window_seconds)

# Usage
limiter = FixedWindowRateLimiter(redis_client)

def api_endpoint():
    user_id = request.user_id
    
    allowed, remaining, reset_time = limiter.is_allowed(user_id, limit=100, window_seconds=60)
    
    # Add rate limit headers
    response.headers['X-RateLimit-Limit'] = '100'
    response.headers['X-RateLimit-Remaining'] = str(remaining)
    response.headers['X-RateLimit-Reset'] = str(reset_time)
    
    if not allowed:
        return jsonify({'error': 'Rate limit exceeded'}), 429
    
    # Process request
    return jsonify({'data': '...'})
```

**Pros:**
- ✅ Simple to implement
- ✅ Memory efficient
- ✅ Fast (single Redis operation)

**Cons:**
- ❌ Burst at window boundaries (2x limit possible)
- ❌ Unfair for users at window edges

**Burst Problem:**
```
Window 1 (0-60s):    |----99 requests at 59s----|
Window 2 (60-120s):  |----100 requests at 60s---|
Total: 199 requests in 2 seconds! (Should be 100)
```

---

### 2. Sliding Window Log

**Concept:**
- Store timestamp of each request
- Count requests in sliding time window
- Remove old timestamps

**Implementation:**

```python
import time

class SlidingWindowLogRateLimiter:
    def __init__(self, redis_client):
        self.redis = redis_client
    
    def is_allowed(self, user_id, limit=100, window_seconds=60):
        """
        Check using sliding window log
        More accurate but higher memory
        """
        key = f'rate_limit:{user_id}'
        current_time = time.time()
        window_start = current_time - window_seconds
        
        # Remove old entries (outside window)
        self.redis.zremrangebyscore(key, 0, window_start)
        
        # Count requests in current window
        count = self.redis.zcard(key)
        
        if count < limit:
            # Add current request timestamp
            self.redis.zadd(key, {current_time: current_time})
            
            # Set expiry
            self.redis.expire(key, window_seconds)
            
            return (True, limit - count - 1, int(current_time + window_seconds))
        
        return (False, 0, int(window_start + window_seconds))

# Example timeline
# User makes requests at: 10s, 20s, 30s, 40s, 50s
# At 70s, sliding window [10s-70s] includes all 5 requests
# At 75s, sliding window [15s-75s] includes 4 requests (10s removed)
```

**Pros:**
- ✅ Very accurate
- ✅ No burst problem

**Cons:**
- ❌ High memory (stores every request)
- ❌ Slower (multiple Redis operations)

---

### 3. Sliding Window Counter (Hybrid)

**Concept:**
- Combine fixed window + sliding window
- Use weighted count from previous and current window
- Balance accuracy and efficiency

**Implementation:**

```python
class SlidingWindowCounterRateLimiter:
    def __init__(self, redis_client):
        self.redis = redis_client
    
    def is_allowed(self, user_id, limit=100, window_seconds=60):
        """
        Hybrid approach: more accurate than fixed window,
        more efficient than sliding log
        """
        current_time = time.time()
        current_window = int(current_time / window_seconds)
        previous_window = current_window - 1
        
        # Keys
        current_key = f'rate_limit:{user_id}:{current_window}'
        previous_key = f'rate_limit:{user_id}:{previous_window}'
        
        # Get counts
        current_count = int(self.redis.get(current_key) or 0)
        previous_count = int(self.redis.get(previous_key) or 0)
        
        # Calculate position in current window (0.0 to 1.0)
        window_position = (current_time % window_seconds) / window_seconds
        
        # Weighted count
        # If 30% into current window, use 70% of previous + 100% of current
        weighted_count = (previous_count * (1 - window_position)) + current_count
        
        if weighted_count < limit:
            # Increment current window
            self.redis.incr(current_key)
            self.redis.expire(current_key, window_seconds * 2)
            
            return (True, int(limit - weighted_count - 1), 
                   (current_window + 1) * window_seconds)
        
        return (False, 0, (current_window + 1) * window_seconds)

# Example:
# Window 1 (0-60s): 80 requests
# Window 2 (60-120s): 50 requests so far
# At 90s (50% into window 2):
#   weighted_count = 80 * 0.5 + 50 = 40 + 50 = 90
```

**Pros:**
- ✅ Good accuracy (better than fixed window)
- ✅ Memory efficient (only 2 counters)
- ✅ Fast (2 Redis reads, 1 write)

**Cons:**
- ⚠️ Approximation (not 100% accurate)

---

### 4. Token Bucket (Recommended)

**Concept:**
- Bucket holds tokens
- Tokens added at fixed rate
- Request consumes token
- If no tokens, request rejected

**Implementation:**

```python
import time

class TokenBucketRateLimiter:
    def __init__(self, redis_client):
        self.redis = redis_client
    
    def is_allowed(self, user_id, capacity=100, refill_rate=10):
        """
        Token bucket algorithm
        
        Args:
            user_id: Unique identifier
            capacity: Bucket size (max burst)
            refill_rate: Tokens added per second
        
        Returns:
            (allowed, tokens_remaining)
        """
        key = f'rate_limit:{user_id}'
        current_time = time.time()
        
        # Get bucket state (using Lua script for atomicity)
        lua_script = """
        local key = KEYS[1]
        local capacity = tonumber(ARGV[1])
        local refill_rate = tonumber(ARGV[2])
        local current_time = tonumber(ARGV[3])
        
        -- Get current state
        local bucket = redis.call('HMGET', key, 'tokens', 'last_refill')
        local tokens = tonumber(bucket[1])
        local last_refill = tonumber(bucket[2])
        
        -- Initialize if not exists
        if tokens == nil then
            tokens = capacity
            last_refill = current_time
        end
        
        -- Calculate new tokens (refill)
        local time_passed = current_time - last_refill
        local tokens_to_add = time_passed * refill_rate
        tokens = math.min(capacity, tokens + tokens_to_add)
        
        -- Check if request allowed
        if tokens >= 1 then
            tokens = tokens - 1
            redis.call('HMSET', key, 'tokens', tokens, 'last_refill', current_time)
            redis.call('EXPIRE', key, 3600)
            return {1, tokens}  -- Allowed
        else
            redis.call('HMSET', key, 'tokens', tokens, 'last_refill', current_time)
            redis.call('EXPIRE', key, 3600)
            return {0, tokens}  -- Not allowed
        end
        """
        
        result = self.redis.eval(
            lua_script,
            1,  # Number of keys
            key,
            capacity,
            refill_rate,
            current_time
        )
        
        allowed = result[0] == 1
        tokens_remaining = result[1]
        
        return (allowed, tokens_remaining)

# Usage with burst handling
limiter = TokenBucketRateLimiter(redis_client)

def api_endpoint():
    # Allow burst of 100, but sustained rate of 10/sec
    allowed, remaining = limiter.is_allowed(
        request.user_id,
        capacity=100,
        refill_rate=10
    )
    
    response.headers['X-RateLimit-Remaining'] = str(int(remaining))
    
    if not allowed:
        return jsonify({'error': 'Rate limit exceeded'}), 429
    
    return jsonify({'data': '...'})
```

**Pros:**
- ✅ Smooth rate limiting
- ✅ Allows burst traffic (up to capacity)
- ✅ Fair over time

**Cons:**
- ⚠️ Slightly more complex

---

### 5. Leaky Bucket

**Concept:**
- Requests enter bucket
- Processed at fixed rate (leak)
- If bucket full, reject request

```python
class LeakyBucketRateLimiter:
    def __init__(self, redis_client):
        self.redis = redis_client
    
    def is_allowed(self, user_id, capacity=100, leak_rate=10):
        """
        Leaky bucket algorithm
        Processes requests at fixed rate
        """
        key = f'rate_limit:{user_id}'
        current_time = time.time()
        
        lua_script = """
        local key = KEYS[1]
        local capacity = tonumber(ARGV[1])
        local leak_rate = tonumber(ARGV[2])
        local current_time = tonumber(ARGV[3])
        
        local bucket = redis.call('HMGET', key, 'level', 'last_leak')
        local level = tonumber(bucket[1]) or 0
        local last_leak = tonumber(bucket[2]) or current_time
        
        -- Leak (process requests)
        local time_passed = current_time - last_leak
        local leaked = time_passed * leak_rate
        level = math.max(0, level - leaked)
        
        -- Add new request
        if level < capacity then
            level = level + 1
            redis.call('HMSET', key, 'level', level, 'last_leak', current_time)
            redis.call('EXPIRE', key, 3600)
            return {1, capacity - level}
        else
            redis.call('HMSET', key, 'level', level, 'last_leak', current_time)
            return {0, 0}
        end
        """
        
        result = self.redis.eval(lua_script, 1, key, capacity, leak_rate, current_time)
        
        return (result[0] == 1, result[1])
```

**Token Bucket vs Leaky Bucket:**
- Token Bucket: Allows burst (up to capacity), then sustained rate
- Leaky Bucket: Enforces strict output rate, smooths bursts

---

## 🔧 Production Implementation

### Distributed Rate Limiter

```python
from flask import Flask, request, jsonify
import redis

app = Flask(__name__)
redis_client = redis.Redis(host='localhost', port=6379)

# Rate limit configuration
RATE_LIMITS = {
    '/api/search': {'limit': 100, 'window': 60},      # 100 req/min
    '/api/upload': {'limit': 10, 'window': 3600},     # 10 req/hour
    '/api/login': {'limit': 5, 'window': 300},        # 5 req/5min
    'default': {'limit': 1000, 'window': 60}          # Default
}

def get_rate_limit_key(user_id, endpoint):
    """Generate rate limit key"""
    return f'rate_limit:{user_id}:{endpoint}'

def check_rate_limit(user_id, endpoint):
    """
    Check if request should be rate limited
    Returns: (allowed, remaining, reset_time)
    """
    config = RATE_LIMITS.get(endpoint, RATE_LIMITS['default'])
    
    limiter = TokenBucketRateLimiter(redis_client)
    
    allowed, remaining = limiter.is_allowed(
        user_id=user_id,
        capacity=config['limit'],
        refill_rate=config['limit'] / config['window']
    )
    
    reset_time = int(time.time() + config['window'])
    
    return (allowed, remaining, reset_time, config['limit'])

# Middleware
@app.before_request
def rate_limit_middleware():
    """Apply rate limiting to all requests"""
    # Skip for health check
    if request.path == '/health':
        return
    
    # Get user ID (from auth token or IP)
    user_id = getattr(request, 'user_id', None) or request.remote_addr
    endpoint = request.path
    
    # Check rate limit
    allowed, remaining, reset_time, limit = check_rate_limit(user_id, endpoint)
    
    # Add headers
    @after_this_request
    def add_rate_limit_headers(response):
        response.headers['X-RateLimit-Limit'] = str(limit)
        response.headers['X-RateLimit-Remaining'] = str(int(remaining))
        response.headers['X-RateLimit-Reset'] = str(reset_time)
        return response
    
    if not allowed:
        return jsonify({
            'error': 'Rate limit exceeded',
            'message': f'Try again in {reset_time - int(time.time())} seconds'
        }), 429

# Hierarchical rate limiting
def check_hierarchical_rate_limit(user_id):
    """
    Multiple rate limits: per-second, per-minute, per-hour
    """
    limits = [
        ('second', 10, 1),
        ('minute', 100, 60),
        ('hour', 1000, 3600)
    ]
    
    for window_name, limit, window_seconds in limits:
        key = f'rate_limit:{user_id}:{window_name}'
        
        allowed, remaining, reset_time = FixedWindowRateLimiter(redis_client).is_allowed(
            key, limit, window_seconds
        )
        
        if not allowed:
            return (False, window_name, reset_time)
    
    return (True, None, None)
```

### Rate Limiting by IP and User

```python
def get_identifier():
    """
    Get rate limit identifier
    Priority: User ID > API Key > IP Address
    """
    # Authenticated user
    if hasattr(request, 'user_id'):
        return f'user:{request.user_id}'
    
    # API key
    api_key = request.headers.get('X-API-Key')
    if api_key:
        return f'api_key:{api_key}'
    
    # IP address
    # Handle proxies (X-Forwarded-For)
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    ip = ip.split(',')[0].strip()  # Get first IP
    return f'ip:{ip}'
```

### Dynamic Rate Limits

```python
# Store rate limits in database
def get_user_rate_limit(user_id):
    """
    Get custom rate limit for user
    Premium users get higher limits
    """
    user = db.query("SELECT plan FROM users WHERE user_id = ?", user_id)
    
    limits = {
        'free': {'limit': 100, 'window': 60},
        'pro': {'limit': 1000, 'window': 60},
        'enterprise': {'limit': 10000, 'window': 60}
    }
    
    return limits.get(user.plan, limits['free'])
```

---

## 💡 Algorithm Comparison

| Algorithm | Accuracy | Memory | Complexity | Burst Handling |
|-----------|----------|--------|------------|----------------|
| Fixed Window | ⚠️ Low | ✅ Minimal | ✅ Simple | ❌ Poor |
| Sliding Log | ✅ Perfect | ❌ High | ⚠️ Medium | ✅ Good |
| Sliding Counter | ✅ Good | ✅ Low | ✅ Simple | ✅ Good |
| Token Bucket | ✅ Good | ✅ Low | ⚠️ Medium | ✅ Excellent |
| Leaky Bucket | ✅ Good | ✅ Low | ⚠️ Medium | ⚠️ Smooths |

**Recommendation:** Token Bucket (best balance)

---

## 🎯 Interview Tips

**Key Points to Cover:**
1. ✅ Token bucket algorithm (recommended)
2. ✅ Distributed system (Redis)
3. ✅ Multiple time windows (second/minute/hour)
4. ✅ Rate limit headers
5. ✅ Hierarchical limits (per-user, per-IP, per-endpoint)

**Common Follow-ups:**
- "Which algorithm?" → Token bucket (handles burst, fair)
- "How to distribute?" → Redis with Lua scripts (atomic)
- "How to handle bursts?" → Token bucket capacity
- "How to scale?" → Redis cluster, multiple rate limits

---

**Next:** [Design Notification System](20_notification_system.md)
