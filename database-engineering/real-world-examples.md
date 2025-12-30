# Database Engineering - Real-World Examples

## 🎯 Case Study: Uber's Database Migration

**Challenge:** Migrate from PostgreSQL to MySQL while maintaining 24/7 uptime

**Scale:**
- 1000+ database servers
- Petabytes of data
- Millions of trips per day

**Strategy:**

```
Phase 1: Dual Write (4 weeks)
┌──────────────┐
│ Application  │
└──────┬───────┘
       │
   ┌───┴────┐
   ▼        ▼
┌─────┐  ┌─────┐
│ PG  │  │MySQL│
└─────┘  └─────┘
 (Read)  (Write)

Phase 2: Verification (2 weeks)
- Compare data consistency
- Performance benchmarks
- Load testing

Phase 3: Gradual Read Migration (4 weeks)
- 10% reads from MySQL
- 25% → 50% → 75% → 100%
- Monitor latency/errors

Phase 4: Complete Migration
- All reads/writes to MySQL
- Keep PostgreSQL as backup
- Decommission after 30 days
```

## 🎯 Real Problem: N+1 Query Bug

**Scenario:** User profile page loading in 8 seconds

**Problem Code:**
```python
# Loads 1000+ users
users = User.query.all()

for user in users:
    # N+1 query problem!
    profile = Profile.query.filter_by(user_id=user.id).first()  # 1000 queries
    posts = Post.query.filter_by(user_id=user.id).all()  # 1000 queries
```

**Solution:**
```python
# Single query with joins
users = db.session.query(User)\
    .options(
        joinedload(User.profile),
        joinedload(User.posts)
    )\
    .all()

# Result: 8 seconds → 200ms (40x improvement)
```

## 🎯 Scaling Strategy: Read/Write Split

**Implementation:**

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
import random

class DatabaseRouter:
    def __init__(self):
        # Write to primary
        self.primary = create_engine('postgresql://primary:5432/db')
        
        # Read from replicas
        self.replicas = [
            create_engine('postgresql://replica1:5432/db'),
            create_engine('postgresql://replica2:5432/db'),
            create_engine('postgresql://replica3:5432/db')
        ]
    
    def get_session(self, write=False):
        if write:
            return Session(self.primary)
        else:
            # Load balance across replicas
            return Session(random.choice(self.replicas))

# Usage
router = DatabaseRouter()

# Write operations
with router.get_session(write=True) as session:
    user = User(email='test@example.com')
    session.add(user)
    session.commit()

# Read operations
with router.get_session(write=False) as session:
    users = session.query(User).limit(10).all()
```

## 🎯 Interview Question: Design Database for Twitter

**Requirements:**
- 500M active users
- 500M tweets/day
- Sub-100ms read latency
- Handle trending topics

**Schema Design:**

```sql
-- Sharded by user_id (64 shards)
CREATE TABLE users (
    user_id BIGSERIAL PRIMARY KEY,
    username VARCHAR(15) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    follower_count INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    shard_id INT GENERATED ALWAYS AS (user_id % 64) STORED
);

CREATE INDEX idx_users_shard ON users(shard_id, user_id);

-- Tweets (time-series partitioning)
CREATE TABLE tweets (
    tweet_id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL,
    content VARCHAR(280) NOT NULL,
    like_count INT DEFAULT 0,
    retweet_count INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) PARTITION BY RANGE (created_at);

-- Monthly partitions
CREATE TABLE tweets_2024_12 PARTITION OF tweets
    FOR VALUES FROM ('2024-12-01') TO ('2025-01-01');

-- Hot data in PostgreSQL (last 7 days)
-- Cold data archived to S3 + Athena (>7 days)
```

**Caching Strategy:**

```python
import redis
import json

r = redis.Redis(host='localhost', port=6379)

def get_timeline(user_id, page=1, per_page=20):
    cache_key = f'timeline:{user_id}:{page}'
    
    # Try cache first
    cached = r.get(cache_key)
    if cached:
        return json.loads(cached)
    
    # Cache miss - query database
    tweets = db.query(Tweet)\
        .join(Follow, Follow.following_id == Tweet.user_id)\
        .filter(Follow.follower_id == user_id)\
        .order_by(Tweet.created_at.desc())\
        .offset((page-1) * per_page)\
        .limit(per_page)\
        .all()
    
    # Cache for 5 minutes
    r.setex(cache_key, 300, json.dumps([t.to_dict() for t in tweets]))
    
    return tweets
```

## 📊 Performance Metrics

| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| Query Time | 5000ms | 50ms | 100x |
| Throughput | 100 QPS | 10,000 QPS | 100x |
| Database CPU | 85% | 25% | 3.4x better |
| Cache Hit Rate | 0% | 95% | - |
| Monthly Cost | $12,000 | $3,500 | 70% savings |
