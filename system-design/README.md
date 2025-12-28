# System Design Primer - Study Guide

A comprehensive collection of system design concepts, patterns, and real-world architectures for technical interviews and building scalable systems.

## 📚 Table of Contents

### Core Concepts (10 Topics)
1. [**Fundamentals**](01_fundamentals.md) - Performance, Scalability, Latency, Throughput
2. [**Availability & Reliability**](02_availability_reliability.md) - CAP Theorem, Consistency, Replication
3. [**Caching Strategies**](03_caching.md) - Cache Patterns, CDN, Invalidation
4. [**Databases**](04_databases.md) - SQL vs NoSQL, Sharding, Replication, Partitioning
5. [**Load Balancing**](05_load_balancing.md) - Load Balancers, Horizontal Scaling, DNS
6. [**Microservices & APIs**](06_microservices_apis.md) - Service Architecture, REST, RPC, Message Queues
7. [**Storage & File Systems**](07_storage.md) - Object Storage, CDN, Blob Storage, Distributed File Systems
8. [**Networking**](08_networking.md) - TCP/UDP, HTTP/HTTPS, WebSockets, Protocols
9. [**Security**](09_security.md) - Authentication, Authorization, Encryption, Rate Limiting
10. [**Monitoring & Operations**](10_monitoring.md) - Logging, Metrics, Alerting, Debugging

### Real-World System Designs (10 Examples)
11. [**Design URL Shortener**](11_url_shortener.md) - TinyURL, Bit.ly
12. [**Design Social Media Feed**](12_social_feed.md) - Twitter Timeline, Facebook News Feed
13. [**Design Messaging System**](13_messaging_system.md) - WhatsApp, Slack, Chat Applications
14. [**Design Video Streaming**](14_video_streaming.md) - YouTube, Netflix Architecture
15. [**Design E-commerce Platform**](15_ecommerce.md) - Amazon, Shopping Cart, Inventory
16. [**Design Search Engine**](16_search_engine.md) - Google, Elasticsearch, Indexing
17. [**Design Ride-Sharing**](17_ride_sharing.md) - Uber, Lyft, Location Services
18. [**Design Cloud Storage**](18_cloud_storage.md) - Dropbox, Google Drive, File Sync
19. [**Design Rate Limiter**](19_rate_limiter.md) - API Throttling, DDoS Protection
20. [**Design Notification System**](20_notification_system.md) - Push Notifications, Email, SMS

---

## 🎯 Study Plan

### Week 1-2: Fundamentals (Topics 1-3)
- Master scalability concepts
- Understand performance vs scalability
- Learn caching strategies and patterns
- Study CAP theorem and consistency models

### Week 3-4: Core Infrastructure (Topics 4-6)
- Database design and trade-offs
- Load balancing techniques
- Microservices architecture
- API design patterns

### Week 5-6: Advanced Topics (Topics 7-10)
- Storage systems and CDN
- Network protocols
- Security best practices
- Monitoring and observability

### Week 7-10: Real-World Designs (Topics 11-20)
- Practice 2-3 system designs per week
- Focus on requirements gathering
- Practice capacity estimation
- Learn to identify bottlenecks

---

## 🎓 How to Approach System Design Interviews

### Step 1: Clarify Requirements (5-10 minutes)
**Functional Requirements:**
- What features need to be built?
- Who are the users?
- What are the core use cases?

**Non-Functional Requirements:**
- Scale (users, data volume, requests per second)
- Performance expectations (latency, throughput)
- Availability requirements (99.9%, 99.99%?)
- Consistency vs availability trade-offs

**Questions to Ask:**
- How many users? (Active vs registered)
- Read-heavy or write-heavy?
- Data retention period?
- Expected growth rate?

### Step 2: Back-of-the-Envelope Calculations (5 minutes)
Calculate key metrics:
- Storage requirements (per day, per year)
- Bandwidth requirements (read/write)
- Queries per second (QPS)
- Memory for caching

**Example for Twitter:**
```
Assumptions:
- 300M daily active users
- Each user views 50 tweets/day
- Each user posts 2 tweets/day

Read QPS: (300M * 50) / 86400 = ~175K reads/sec
Write QPS: (300M * 2) / 86400 = ~7K writes/sec
Read:Write ratio = 25:1 (read-heavy)
```

### Step 3: High-Level Design (10-15 minutes)
- Draw major components (clients, servers, databases, caches)
- Show data flow between components
- Identify APIs needed
- Define data models

**Key Components to Consider:**
- Client (web, mobile)
- Load balancer
- Application servers
- Cache layer
- Database (primary, replicas)
- Message queues
- Storage services
- CDN

### Step 4: Deep Dive (15-20 minutes)
Focus on 2-3 critical components:
- Database schema design
- Caching strategy
- API design
- Algorithm for core feature

**Common Deep Dive Topics:**
- How to handle hotspots?
- How to partition/shard data?
- How to replicate data?
- How to ensure consistency?
- How to handle failures?

### Step 5: Scale and Optimize (5-10 minutes)
- Identify bottlenecks
- Discuss scaling strategies
- Add redundancy for availability
- Optimize for performance

**Scaling Techniques:**
- Horizontal scaling (add more servers)
- Vertical scaling (bigger machines)
- Database sharding
- Read replicas
- Caching layers
- Asynchronous processing
- CDN for static content

### Step 6: Trade-offs and Alternatives (Ongoing)
Always discuss:
- Why you chose SQL vs NoSQL
- Consistency vs availability trade-offs
- Synchronous vs asynchronous processing
- Cost implications
- Maintenance complexity

---

## 🔑 Key Principles

### 1. Everything is a Trade-off
- Consistency vs Availability
- Latency vs Throughput
- Cost vs Performance
- Simplicity vs Flexibility

### 2. Start Simple, Then Scale
- Begin with monolith
- Identify bottlenecks
- Scale specific components
- Don't over-engineer

### 3. Numbers to Remember
```
Operation                           Time
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
L1 cache reference                  0.5 ns
L2 cache reference                  7 ns
Main memory reference               100 ns
SSD random read                     150 μs
Read 1MB sequentially from SSD      1 ms
Disk seek                           10 ms
Read 1MB sequentially from disk     30 ms
Send packet CA → Netherlands → CA   150 ms

Storage
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1 KB = 1,024 bytes
1 MB = 1,024 KB = ~1 million bytes
1 GB = 1,024 MB = ~1 billion bytes
1 TB = 1,024 GB = ~1 trillion bytes
1 PB = 1,024 TB = ~1,000 trillion bytes

Availability
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
99.9% (three 9s)  = 8h 45min downtime/year
99.99% (four 9s)  = 52min downtime/year
99.999% (five 9s) = 5min downtime/year
```

### 4. Common Patterns
- **Load Balancing:** Distribute traffic across servers
- **Caching:** Store frequently accessed data
- **Sharding:** Partition data across databases
- **Replication:** Copy data for availability
- **Queue:** Asynchronous processing
- **CDN:** Serve static content from edge locations

---

## 📊 Capacity Estimation Template

### Storage Calculation
```
Daily new users: X
Data per user: Y KB
Daily storage: X * Y KB

Annual storage: Daily * 365
With replication (3x): Annual * 3
```

### Bandwidth Calculation
```
Requests per second: R
Average request size: S bytes
Bandwidth: R * S bytes/sec

Convert to Gbps: (R * S * 8) / 10^9
```

### Memory for Caching (80-20 Rule)
```
Total daily requests: T
20% are unique: T * 0.2
Cache size per request: C KB
Memory needed: T * 0.2 * C KB
```

---

## 🎯 Interview Tips

### Do's ✅
- Ask clarifying questions upfront
- State assumptions explicitly
- Think out loud
- Draw diagrams
- Discuss trade-offs
- Start simple, then optimize
- Consider failure scenarios
- Mention monitoring/alerting

### Don'ts ❌
- Jump into coding immediately
- Make assumptions without stating them
- Over-engineer from the start
- Ignore the interviewer's hints
- Focus only on happy path
- Forget about non-functional requirements
- Design in complete silence
- Skip capacity estimation

---

## 📚 Resources

### Primary Resource
- **System Design Primer:** https://github.com/donnemartin/system-design-primer
  - Comprehensive guide with real-world examples
  - Covers all fundamental topics
  - Includes Anki flashcards for study

### Additional Resources
- **Grokking System Design:** educative.io
- **System Design Interview by Alex Xu:** Book series
- **High Scalability Blog:** highscalability.com
- **Engineering Blogs:** Netflix, Uber, Airbnb, Facebook

### Practice Platforms
- **LeetCode System Design:** Premium subscription
- **Pramp:** Mock interviews with peers
- **Interviewing.io:** Practice with engineers

---

## 🏗️ Real-World Company Architectures

Study these to understand practical implementations:
- **Netflix:** Video streaming at scale
- **Uber:** Real-time location services
- **Instagram:** Photo storage and social features
- **Twitter:** Timeline and feed generation
- **WhatsApp:** Real-time messaging
- **Amazon:** E-commerce and recommendations
- **Google:** Search and distributed systems

---

## 🚀 Getting Started

1. **Week 1-2:** Read through fundamentals (Topics 1-3)
2. **Week 3-4:** Study core infrastructure (Topics 4-6)
3. **Week 5-6:** Learn advanced topics (Topics 7-10)
4. **Week 7-10:** Practice system designs (Topics 11-20)
5. **Ongoing:** Review Anki flashcards daily
6. **Practice:** Mock interviews weekly

---

## 💡 Common Interview Questions

1. Design a URL shortening service (like TinyURL)
2. Design a social network feed (like Twitter/Facebook)
3. Design a messaging system (like WhatsApp)
4. Design a video streaming service (like YouTube)
5. Design a web crawler
6. Design a key-value store
7. Design a recommendation system
8. Design a ride-sharing service (like Uber)
9. Design a file storage system (like Dropbox)
10. Design a search autocomplete system

---

**Good luck with your system design preparation! 🎓**

> "The purpose of abstraction is not to be vague, but to create a new semantic level in which one can be absolutely precise." - Edsger Dijkstra
