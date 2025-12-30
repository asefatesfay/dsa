# Back of the Envelope Calculations Guide

A comprehensive step-by-step tutorial for system design capacity estimation.

---

## 📐 Why Back of the Envelope Calculations?

In system design interviews, you need to **quickly estimate**:
- How much storage is needed?
- What bandwidth is required?
- How many servers are needed?
- What response times to expect?

These calculations help you:
1. ✅ Make informed architecture decisions
2. ✅ Identify bottlenecks early
3. ✅ Choose appropriate technologies
4. ✅ Plan for scale

---

## 🔢 Essential Numbers to Memorize

### Time Durations

| Operation | Time | Notes |
|-----------|------|-------|
| L1 cache reference | 0.5 ns | CPU cache |
| L2 cache reference | 7 ns | CPU cache |
| Main memory reference | 100 ns | RAM |
| SSD random read | 150 μs | 150,000 ns |
| HDD seek | 10 ms | 10,000,000 ns |
| Network round trip (same datacenter) | 500 μs | 0.5 ms |
| Network round trip (CA to Netherlands) | 150 ms | |

### Data Sizes

#### Understanding Binary vs Decimal

**Two systems exist:**

1. **Binary (Powers of 2)** - How computers actually work:
   - 1 KiB (Kibibyte) = 2^10 = 1,024 bytes
   - 1 MiB (Mebibyte) = 2^20 = 1,048,576 bytes
   - 1 GiB (Gibibyte) = 2^30 = 1,073,741,824 bytes
   - 1 TiB (Tebibyte) = 2^40 bytes
   - 1 PiB (Pebibyte) = 2^50 bytes

2. **Decimal (Powers of 10)** - Marketing and simplicity:
   - 1 KB (Kilobyte) = 10^3 = 1,000 bytes
   - 1 MB (Megabyte) = 10^6 = 1,000,000 bytes
   - 1 GB (Gigabyte) = 10^9 = 1,000,000,000 bytes
   - 1 TB (Terabyte) = 10^12 = 1,000,000,000,000 bytes
   - 1 PB (Petabyte) = 10^15 = 1,000,000,000,000,000 bytes

**For interviews: Use decimal (powers of 10)** - It's faster and simpler!

#### Visual Comparison Table

| Unit | Powers of 2 (Actual) | Powers of 10 (Interview) | Difference | Real-World Example |
|------|---------------------|--------------------------|------------|-------------------|
| **KB** | 2^10 = 1,024 bytes | 10^3 = 1,000 bytes | ~2% | Short text file, small email |
| **MB** | 2^20 = 1,048,576 bytes | 10^6 = 1,000,000 bytes | ~5% | High-res photo, MP3 song |
| **GB** | 2^30 = 1,073,741,824 bytes | 10^9 = 1,000,000,000 bytes | ~7% | HD movie, smartphone app |
| **TB** | 2^40 = 1,099,511,627,776 bytes | 10^12 = 1,000,000,000,000 bytes | ~10% | External hard drive, 500 HD movies |
| **PB** | 2^50 = 1,125,899,906,842,624 bytes | 10^15 = 1,000,000,000,000,000 bytes | ~13% | Facebook daily uploads, YouTube hourly uploads |

**Key insight:** The difference is small enough that using powers of 10 is acceptable for estimation!

#### Memory Aid: "The Thousand Ladder"

Think of each step as **×1,000** (three zeros):

```
1 Byte
    ↓ ×1,000
1,000 Bytes = 1 KB
    ↓ ×1,000
1,000,000 Bytes = 1,000 KB = 1 MB
    ↓ ×1,000
1,000,000,000 Bytes = 1,000,000 KB = 1,000 MB = 1 GB
    ↓ ×1,000
1,000,000,000,000 Bytes = 1,000,000,000 KB = 1,000,000 MB = 1,000 GB = 1 TB
    ↓ ×1,000
1,000,000,000,000,000 Bytes = 1 PB
```

**Simple pattern:** Each level adds **3 zeros** or **×1,000**

#### Powers of 10 Quick Reference

| Unit | Formula | Zeros | Scientific Notation |
|------|---------|-------|---------------------|
| KB | 10^3 | 1,000 (3 zeros) | 1 × 10^3 |
| MB | 10^6 | 1,000,000 (6 zeros) | 1 × 10^6 |
| GB | 10^9 | 1,000,000,000 (9 zeros) | 1 × 10^9 |
| TB | 10^12 | 1,000,000,000,000 (12 zeros) | 1 × 10^12 |
| PB | 10^15 | 1,000,000,000,000,000 (15 zeros) | 1 × 10^15 |

**Memory trick:** The exponent tells you how many zeros!
- KB = 10^**3** → **3** zeros → 1,000
- MB = 10^**6** → **6** zeros → 1,000,000
- GB = 10^**9** → **9** zeros → 1,000,000,000

#### Conversion Practice

**Converting UP (smaller → larger):**
```
Question: 5,000 KB to MB?
Answer: Divide by 1,000 → 5,000 ÷ 1,000 = 5 MB

Question: 3,000,000 KB to GB?
Answer: Divide by 1,000,000 → 3,000,000 ÷ 1,000,000 = 3 GB
        OR: 3,000,000 KB → 3,000 MB → 3 GB (two steps of ÷1,000)
```

**Converting DOWN (larger → smaller):**
```
Question: 2 GB to MB?
Answer: Multiply by 1,000 → 2 × 1,000 = 2,000 MB

Question: 5 TB to GB?
Answer: Multiply by 1,000 → 5 × 1,000 = 5,000 GB
```

#### Real-World Size Examples

| Size | What It Holds |
|------|---------------|
| **1 KB** | • Half a page of text<br>• Small email with no attachments<br>• Tiny icon (16×16 pixels) |
| **1 MB** | • 1 high-quality photo (compressed)<br>• 1 minute of MP3 music<br>• 500 pages of text<br>• 1 book (average novel) |
| **1 GB** | • 1 hour of SD video<br>• 250 MP3 songs<br>• 500 high-quality photos<br>• 1 small mobile game |
| **1 TB** | • 500 hours of HD video (movies)<br>• 250,000 photos<br>• 200,000 songs<br>• 1,000 hours of music |
| **1 PB** | • 500 million photos<br>• 13.3 years of HD video<br>• 10 billion phone contacts<br>• 20 million filing cabinets of text |

#### Mental Calculation Shortcuts

**Technique 1: Break into smaller steps**
```
Instead of: 200,000,000 KB → ? GB

Do this:
  200,000,000 KB
  → 200,000 MB (÷ 1,000)
  → 200 GB (÷ 1,000)

Much easier mentally!
```

**Technique 2: Move the decimal**
```
5,000 KB to MB?
  5,000. KB → Move decimal 3 places left → 5.000 MB = 5 MB

3,500,000 MB to TB?
  3,500,000. MB → Move 3 places (MB→GB) → 3,500. GB
  3,500. GB → Move 3 places (GB→TB) → 3.5 TB
```

**Technique 3: Use scientific notation**
```
2 × 10^8 bytes to MB?
  MB = 10^6, so divide: 2 × 10^8 ÷ 10^6 = 2 × 10^(8-6) = 2 × 10^2 = 200 MB
```

### Time Conversions

```
1 day = 24 hours = 86,400 seconds ≈ 100,000 seconds (rounded)
1 month = 30 days ≈ 2.5 million seconds
1 year = 365 days ≈ 31.5 million seconds ≈ 32 million seconds
```

### Throughput (Bandwidth)

Throughput measures **how much data flows through your network per second**.

#### Understanding Bits vs Bytes

**Critical distinction:**
- **Bits (b)** - Used for **network speed** (bandwidth, throughput)
- **Bytes (B)** - Used for **file sizes** (storage)

**Conversion:** 1 Byte = 8 bits
```
Therefore: 1 MB/s (Megabyte per second) = 8 Mbps (Megabit per second)
```

#### Network Speed Reference Table

| Bits per second | Bytes per second | Conversion | Real-world context |
|----------------|------------------|------------|-------------------|
| 1 Kbps | 125 B/s | ÷ 8 | Old dial-up modem |
| 1 Mbps | 125 KB/s | ÷ 8 | Basic broadband |
| 10 Mbps | 1.25 MB/s | ÷ 8 | Standard home internet |
| 100 Mbps | 12.5 MB/s | ÷ 8 | Fast home internet |
| 1 Gbps | 125 MB/s | ÷ 8 | Gigabit ethernet, fiber |
| 10 Gbps | 1.25 GB/s | ÷ 8 | Datacenter links |
| 100 Gbps | 12.5 GB/s | ÷ 8 | High-performance datacenter |

**Memory trick:** Divide bits by 8 to get bytes (or multiply bytes by 8 to get bits)

#### Visual Understanding: Bits vs Bytes

```
Network advertises: 1 Gbps (Gigabit per second)
Actual download speed: 125 MB/s (Megabytes per second)

Why? 1 Gb = 1,000 Mb = 1,000,000 Kb = 1,000,000,000 bits
      1,000,000,000 bits ÷ 8 = 125,000,000 Bytes = 125 MB
```

#### Common Throughput Calculations

**Scenario 1: Calculate bandwidth from file size and time**
```
Question: Streaming 1 GB file in 10 seconds, what bandwidth?

Answer:
  1 GB in 10 seconds
  = 1,000 MB / 10 seconds
  = 100 MB/s (Megabytes per second)
  = 100 × 8 = 800 Mbps (Megabits per second)
```

**Scenario 2: Calculate bandwidth from requests per second**
```
Question: 10,000 requests/sec, each response is 200 KB. What bandwidth?

Answer:
  10,000 requests/sec × 200 KB
  = 2,000,000 KB/sec
  = 2,000 MB/sec
  = 2 GB/sec (Gigabytes per second)
  = 2 × 8 = 16 Gbps (Gigabits per second)
```

**Scenario 3: How many requests can bandwidth support?**
```
Question: 10 Gbps link, each request is 500 KB. How many requests/sec?

Answer:
  10 Gbps = 10 ÷ 8 = 1.25 GB/s = 1,250 MB/s
  1,250 MB/s ÷ 0.5 MB per request
  = 2,500 requests/sec
```

#### Shortcut for Interviews

**Quick conversion (Gbps ↔ GB/s):**
```
Gbps → GB/s: Divide by 8
  80 Gbps → 80 ÷ 8 = 10 GB/s

GB/s → Gbps: Multiply by 8
  5 GB/s → 5 × 8 = 40 Gbps
```

**Rule of thumb:** 
- 1 Gbps ≈ 125 MB/s ≈ 0.125 GB/s
- 10 Gbps ≈ 1.25 GB/s
- 100 Gbps ≈ 12.5 GB/s

#### Practice Problems: Throughput

**Problem 1:**
50,000 images/sec, each 200 KB. What's the bandwidth?

<details>
<summary>Solution</summary>

```
50,000 requests/sec × 200 KB
= 10,000,000 KB/sec
= 10,000 MB/sec
= 10 GB/sec
= 10 × 8 = 80 Gbps
```
</details>

**Problem 2:**
You have a 40 Gbps link. Each video stream needs 5 Mbps. How many concurrent streams?

<details>
<summary>Solution</summary>

```
40 Gbps = 40,000 Mbps
40,000 Mbps ÷ 5 Mbps per stream
= 8,000 concurrent streams
```
</details>

**Problem 3:**
Downloading 500 MB at 100 Mbps. How long does it take?

<details>
<summary>Solution</summary>

```
100 Mbps = 100 ÷ 8 = 12.5 MB/s
500 MB ÷ 12.5 MB/s = 40 seconds
```
</details>

#### Common Interview Bandwidths

| Service Type | Typical Bandwidth |
|-------------|-------------------|
| Single HD video stream | 5 Mbps |
| Single 4K video stream | 25 Mbps |
| Photo upload (2 MB) | Need 16 Mbps for 1/sec |
| API response (10 KB) | Need 80 Kbps for 10/sec |
| Database query result (1 MB) | Need 8 Mbps for 1/sec |
| Large file download (100 MB) | Need 800 Mbps for 1/sec |

#### Why This Matters in System Design

**Example mistake:**
```
❌ "We transfer 100 GB/sec, so we need 100 Gbps"
✅ "We transfer 100 GB/sec, so we need 100 × 8 = 800 Gbps"

Forgetting the 8× conversion can make designs fail!
```

**Example calculation:**
```
Instagram uploads: 2,000 photos/sec × 2 MB = 4 GB/sec
Bandwidth needed: 4 GB/sec × 8 = 32 Gbps

With peak traffic (3×): 32 × 3 = 96 Gbps ingress bandwidth
```

---

---

## 🎓 Learning Strategy: Practice Exercises

Before jumping into the full example, **practice these mini-exercises** to build intuition:

### Exercise Set 1: Basic Conversions

Convert these (answers below):
1. 5,000 KB = ? MB
2. 3,000 MB = ? GB
3. 2,000,000 KB = ? GB
4. 500 GB = ? TB
5. 10 TB = ? GB

<details>
<summary>Answers</summary>

1. 5,000 KB = 5 MB (÷ 1,000)
2. 3,000 MB = 3 GB (÷ 1,000)
3. 2,000,000 KB = 2,000 MB = 2 GB (÷ 1,000 twice)
4. 500 GB = 0.5 TB (÷ 1,000)
5. 10 TB = 10,000 GB (× 1,000)

</details>

### Exercise Set 2: Real-World Estimation

Estimate storage needed:
1. Store 1 million photos, each 200 KB
2. Store 500,000 videos, each 50 MB
3. Store 10 billion text messages, each 100 bytes
4. Store 1 million user profiles, each 5 KB

<details>
<summary>Answers with work shown</summary>

1. **1 million photos × 200 KB**
   - = 1,000,000 × 200 KB
   - = 200,000,000 KB
   - = 200,000 MB
   - = 200 GB

2. **500,000 videos × 50 MB**
   - = 500,000 × 50 MB
   - = 25,000,000 MB
   - = 25,000 GB
   - = 25 TB

3. **10 billion messages × 100 bytes**
   - = 10,000,000,000 × 100 bytes
   - = 1,000,000,000,000 bytes
   - = 1,000 GB (÷ 1,000,000,000)
   - = 1 TB

4. **1 million profiles × 5 KB**
   - = 1,000,000 × 5 KB
   - = 5,000,000 KB
   - = 5,000 MB
   - = 5 GB

</details>

### Exercise Set 3: Speed Calculations

Calculate requests per second:
1. 100 million requests per day
2. 5 billion reads per day
3. 1 million writes per day
4. 500,000 uploads per day

<details>
<summary>Answers with work shown</summary>

**Reminder:** 1 day ≈ 100,000 seconds (rounded from 86,400)

1. **100 million per day**
   - = 100,000,000 / 100,000
   - = 1,000 requests/sec

2. **5 billion per day**
   - = 5,000,000,000 / 100,000
   - = 50,000 reads/sec

3. **1 million per day**
   - = 1,000,000 / 100,000
   - = 10 writes/sec

4. **500,000 per day**
   - = 500,000 / 100,000
   - = 5 uploads/sec

</details>

---

## 🎯 Real World Example: Instagram-like Photo Sharing App

Now let's design a photo-sharing service like Instagram and estimate its capacity requirements using what you learned!

### Step 1: Define Requirements & Assumptions

**Functional Requirements:**
- Users can upload photos
- Users can view photos (feed)
- Users can like and comment

**Traffic Assumptions:**
```
Total users: 500 million
Daily active users (DAU): 100 million (20% of total)
Each user uploads: 2 photos per day (on average)
Each user views: 50 photos per day (on average)
```

**Data Assumptions:**
```
Average photo size: 2 MB (before compression)
After compression: 200 KB per photo
Thumbnail size: 20 KB
Metadata per photo: 500 bytes (JSON: user_id, caption, timestamp, likes, etc.)
```

---

## 📊 Step 2: Calculate Daily Traffic (QPS - Queries Per Second)

### Photo Uploads

```
Daily uploads = 100 million users × 2 photos/user
             = 200 million photos/day

Uploads per second = 200,000,000 / 86,400 seconds
                   ≈ 200,000,000 / 100,000  (round for simplicity)
                   = 2,000 uploads/second
                   
Peak traffic (3x average) = 2,000 × 3 = 6,000 uploads/second
```

**Key insight:** Design for peak traffic, not average!

### Photo Views (Reads)

```
Daily views = 100 million users × 50 photos/user
            = 5 billion views/day
            = 5,000,000,000 / 100,000 seconds
            = 50,000 views/second

Peak: 50,000 × 3 = 150,000 reads/second
```

### Read:Write Ratio

```
Reads: 50,000/sec
Writes: 2,000/sec
Ratio: 50,000 / 2,000 = 25:1

This is a read-heavy system → Use caching heavily!
```

---

## 💾 Step 3: Calculate Storage Requirements

### Photo Storage

**Daily storage:**
```
Photos per day: 200 million
Size per photo: 200 KB (compressed)
Thumbnail size: 20 KB

Daily storage = 200M × (200 KB + 20 KB)
              = 200M × 220 KB
              = 200,000,000 × 220,000 bytes
              = 44,000,000,000,000 bytes
              = 44 TB/day
```

**Yearly storage:**
```
44 TB/day × 365 days = 16,060 TB/year ≈ 16 PB/year
```

**5-year projection:**
```
16 PB/year × 5 years = 80 PB total storage needed
```

**With redundancy (3x replication):**
```
80 PB × 3 = 240 PB
```

### Metadata Storage

```
Per photo metadata: 500 bytes
Daily photos: 200 million

Daily metadata = 200M × 500 bytes
               = 100,000,000,000 bytes
               = 100 GB/day
               = 36.5 TB/year

This is negligible compared to photo storage (16 PB/year)!
```

---

## 🌐 Step 4: Calculate Bandwidth Requirements

Bandwidth is how much data needs to flow through your network.

### Upload Bandwidth (Ingress)

```
Uploads per second: 2,000 photos/sec (average), 6,000/sec (peak)
Size per upload: 2 MB (original, before compression)

Average bandwidth = 2,000 uploads/sec × 2 MB
                  = 4,000 MB/sec
                  = 4 GB/sec
                  = 32 Gbps (Gigabits per second)

Peak bandwidth = 6,000 × 2 MB = 12 GB/sec = 96 Gbps
```

### Download Bandwidth (Egress)

```
Views per second: 50,000 photos/sec (average), 150,000/sec (peak)
Size per view: 200 KB (compressed)

Average bandwidth = 50,000 × 200 KB
                  = 10,000,000 KB/sec
                  = 10 GB/sec
                  = 80 Gbps

Peak bandwidth = 150,000 × 200 KB = 30 GB/sec = 240 Gbps
```

**With CDN caching (90% cache hit rate):**
```
Origin bandwidth = 240 Gbps × 0.1 (10% cache miss)
                 = 24 Gbps

CDN dramatically reduces origin server load!
```

### Thumbnail Bandwidth

```
Each feed view loads thumbnails first: 20 KB each
Feed requests: 50,000/sec × 20 photos per feed = 1,000,000 thumbnails/sec

Thumbnail bandwidth = 1,000,000 × 20 KB
                    = 20,000,000 KB/sec
                    = 20 GB/sec
                    = 160 Gbps

With 95% CDN cache hit: 160 × 0.05 = 8 Gbps origin
```

---

## ⚡ Step 5: Calculate Response Time Requirements

### Database Query Time

**Fetch user feed (50 photos):**
```
Database query: 10-50 ms (to get photo IDs from relational DB)
Cache hit (Redis): 1-5 ms

For 50,000 requests/sec:
  - Using cache: 5 ms latency → Can serve 200 requests per connection
  - Need concurrent connections: 50,000 / 200 = 250 connections
  - Redis can handle 100K ops/sec → Need 1 server
```

### CDN Response Time

```
CDN edge cache hit: 20-50 ms (nearest edge location)
CDN miss (origin): 100-300 ms

With 90% cache hit:
  - 90% users get: 50 ms response
  - 10% users get: 200 ms response
  Average: (0.9 × 50) + (0.1 × 200) = 45 + 20 = 65 ms ✅
```

### Upload Processing Time

```
Client → Upload Service: 100 ms (network)
Upload → S3: 200 ms (multipart upload)
Generate thumbnail: 100 ms (resize operation)
Update database: 10 ms
Total: ~410 ms for upload to complete

This is acceptable for uploads (not real-time critical).
```

---

## 🖥️ Step 6: Calculate Server Requirements

### Application Servers

**Assumptions:**
- Each server handles 1,000 requests/sec
- Need to handle 150,000 reads/sec (peak)

```
Number of servers = 150,000 / 1,000 = 150 servers

With 50% buffer for failover: 150 × 1.5 = 225 servers
```

### Database Servers

**Write load:**
```
2,000 writes/sec (photo metadata)
Modern database (PostgreSQL) handles: 10,000 writes/sec

Number of write servers: 1 primary + 1 standby = 2 servers
```

**Read load:**
```
50,000 reads/sec
Each read replica handles: 10,000 reads/sec

Number of read replicas = 50,000 / 10,000 = 5 replicas
```

### Cache Servers (Redis)

**Cache memory calculation:**
```
Cache hot data: Recent 10% of photos (most frequently accessed)
Total photos: 200M/day × 365 days × 5 years = 365 billion photos
Hot photos: 365B × 0.1 = 36.5 billion

Memory per cache entry:
  - Photo ID: 8 bytes
  - URL: 100 bytes
  - Metadata: 200 bytes
  Total: ~300 bytes

Cache memory = 36.5B × 300 bytes = 10.95 TB

Redis typical size: 256 GB per instance
Number of Redis servers = 10.95 TB / 256 GB = 43 servers

With replication (2x): 43 × 2 = 86 Redis servers
```

### Storage Servers (Object Storage - S3)

```
5-year storage: 80 PB
S3 is managed, but for estimation:
  - Assume 100 TB per storage node
  - Number of nodes: 80 PB / 100 TB = 800 nodes
  - With 3x replication: 2,400 nodes

In practice, use managed S3 and pay per GB stored.
```

---

## 📈 Step 7: Cost Estimation

Let's estimate AWS costs for this system.

### Storage Costs (S3)

```
S3 Standard pricing: $0.023 per GB per month

5-year storage: 80 PB = 80,000,000 GB
Monthly cost: 80,000,000 × $0.023 = $1,840,000/month
Yearly cost: $1,840,000 × 12 = $22,080,000/year

Optimization: Use S3 Glacier for old photos (< 1 year)
  - Glacier: $0.004 per GB per month
  - 70% of photos → Glacier after 3 months
  - New cost: $8 million/year (savings: $14 million!)
```

### Bandwidth Costs (Data Transfer)

```
Egress (outbound): 30 GB/sec average
Daily: 30 GB/sec × 86,400 sec = 2,592,000 GB = 2.59 PB/day
Monthly: 2.59 PB × 30 = 77.7 PB/month

AWS data transfer (>500 TB/month): $0.05 per GB
Monthly cost: 77,700,000 GB × $0.05 = $3,885,000/month

With CDN (CloudFront): $0.02 per GB
Monthly cost: 77,700,000 × $0.02 = $1,554,000/month
Yearly: $18,648,000/year
```

### Compute Costs (EC2)

```
Application servers: 225 servers × $100/month = $22,500/month
Database servers: 7 servers × $500/month = $3,500/month
Redis servers: 86 servers × $200/month = $17,200/month

Monthly compute: $43,200/month
Yearly: $518,400/year
```

### Total Cost

```
Storage: $8,000,000/year
Bandwidth: $18,648,000/year
Compute: $518,400/year
Total: ~$27 million/year

Per user cost: $27M / 500M users = $0.054/user/year ≈ 5 cents per user
```

---

## 🎓 Step 8: Optimization Strategies

Based on our calculations, here are optimization opportunities:

### 1. Reduce Storage Costs

**Problem:** 80 PB storage is expensive ($22M/year).

**Solutions:**
```
✅ Compress photos more aggressively: 200 KB → 100 KB (50% savings = $11M)
✅ Use tiered storage (S3 → Glacier): Save $14M/year
✅ Deduplicate similar photos: Save 5-10%
✅ Delete photos with 0 views after 2 years: Save 10-20%
```

### 2. Reduce Bandwidth Costs

**Problem:** 240 Gbps peak egress is expensive ($18M/year).

**Solutions:**
```
✅ Aggressive CDN caching: 90% → 95% hit rate (save $3M)
✅ Lazy load images (only load visible photos): Save 30%
✅ Serve different resolutions based on device: Save 20%
✅ Use WebP format instead of JPEG: Save 25-30% size
```

### 3. Optimize Database

**Problem:** 50,000 reads/sec requires 5 read replicas.

**Solutions:**
```
✅ Cache aggressively in Redis: Reduce DB reads by 80%
✅ Use database sharding: Distribute load across multiple DBs
✅ Denormalize data: Store feed data in NoSQL (Cassandra)
✅ Use read-through cache: Fetch from DB only on cache miss
```

### 4. Improve Response Time

**Problem:** 65 ms average latency.

**Solutions:**
```
✅ Increase CDN cache hit rate: 90% → 98% (reduce to 30 ms)
✅ Use image sprites for thumbnails: Single request for multiple images
✅ Implement lazy loading: Load images as user scrolls
✅ Use HTTP/2 multiplexing: Parallel image loads
✅ Optimize database queries: Add indexes, query optimization
```

---

## 🧮 Quick Estimation Cheat Sheet

### Traffic Estimation

```
Daily Active Users (DAU) → Actions per user → Total daily actions
→ Divide by 100,000 (seconds in a day) → Actions per second
→ Multiply by 3 for peak traffic
```

**Example:**
```
100M users × 2 posts/day = 200M posts/day
200M / 100K = 2,000 posts/sec
Peak: 2,000 × 3 = 6,000 posts/sec
```

### Storage Estimation

```
Daily data = Items per day × Size per item
Yearly = Daily × 365
Multi-year = Yearly × Years
With replication = Total × Replication factor
```

**Example:**
```
200M photos/day × 200 KB = 40 TB/day
40 TB × 365 = 14.6 TB/year ≈ 15 PB/year
15 PB × 5 years = 75 PB
With 3x replication: 75 × 3 = 225 PB
```

### Bandwidth Estimation

```
Requests per second × Data per request = Bandwidth (MB/sec)
Convert: MB/sec → GB/sec (÷ 1,000) → Gbps (× 8)
```

**Example:**
```
50,000 requests/sec × 200 KB = 10,000 MB/sec = 10 GB/sec
10 GB/sec × 8 = 80 Gbps
With CDN (10% origin): 80 × 0.1 = 8 Gbps
```

### Server Estimation

```
Total requests per second / Requests per server = Number of servers
Add 50% buffer for failover and maintenance
```

**Example:**
```
150,000 requests/sec / 1,000 per server = 150 servers
With buffer: 150 × 1.5 = 225 servers
```

---

## 💡 Common Mistakes to Avoid

### 1. ❌ Not Considering Peak Traffic

```
Wrong: Average traffic = 2,000/sec → Design for 2,000/sec
Right: Peak traffic = 2,000 × 3 = 6,000/sec → Design for 6,000/sec

Systems must handle peak loads, not just averages!
```

### 2. ❌ Ignoring Read:Write Ratio

```
Wrong: Treat all requests equally
Right: Identify if system is read-heavy or write-heavy

Read-heavy (Instagram): Cache aggressively, use CDN, read replicas
Write-heavy (Analytics): Optimize writes, use write buffers, batch processing
```

### 3. ❌ Forgetting Data Replication

```
Wrong: 80 PB storage needed
Right: 80 PB × 3 (replication) = 240 PB actual storage

Always account for redundancy (typically 3x for critical data)!
```

### 4. ❌ Not Planning for Growth

```
Wrong: Design for current scale only
Right: Design for 10x growth over 5 years

Current: 100M DAU → Plan for: 1B DAU
```

### 5. ❌ Unrealistic Assumptions

```
Wrong: Assume 100% cache hit rate
Right: Realistic cache hit: 80-95%

Wrong: Assume 0 latency within datacenter
Right: Account for network latency: 0.5-2 ms
```

---

## 🎯 Interview Tips

### 1. Start with Clarifying Questions

```
✅ "How many users?"
✅ "Daily active users?"
✅ "Average actions per user?"
✅ "Data size per action?"
✅ "Read vs write ratio?"
✅ "Latency requirements?"
```

### 2. State Your Assumptions Clearly

```
"I'm assuming 100 million daily active users..."
"Let's assume each photo is 200 KB after compression..."
"For simplicity, I'll use 100,000 seconds in a day..."
```

### 3. Round Numbers Aggressively

```
✅ 86,400 seconds ≈ 100,000 seconds
✅ 1.5 million ≈ 2 million
✅ 31.5 million seconds ≈ 30 million seconds

Speed matters more than precision!
```

### 4. Show Your Work

```
Don't just say "We need 50 servers"

Say: "150,000 requests/sec ÷ 1,000 requests per server = 150 servers
      With 50% buffer: 150 × 1.5 = 225 servers"
```

### 5. Validate Your Numbers

```
After calculating, do a sanity check:
  - Does 240 Gbps bandwidth seem reasonable? YES (major service)
  - Does 80 PB storage seem reasonable? YES (billions of photos)
  - Does $27M/year cost seem reasonable? YES (500M users is huge)
```

---

## 📚 Practice Problems

### Problem 1: Twitter-like Service

**Requirements:**
- 500M users, 100M DAU
- Each user posts 2 tweets/day
- Each user reads 50 tweets/day
- Tweet size: 140 chars = 280 bytes (UTF-8)
- Image attached: 20% of tweets, 500 KB each

**Calculate:**
1. Tweets per second (average and peak)
2. Daily storage
3. 5-year storage
4. Bandwidth requirements
5. Number of servers needed

<details>
<summary>Click to see solution</summary>

**1. Tweets per second:**
```
Daily tweets = 100M × 2 = 200M tweets/day
Per second = 200M / 100K = 2,000 tweets/sec
Peak = 2,000 × 3 = 6,000 tweets/sec
```

**2. Daily storage:**
```
Text: 200M × 280 bytes = 56 GB
Images: 200M × 0.2 × 500 KB = 20 TB
Total: ~20 TB/day
```

**3. 5-year storage:**
```
20 TB/day × 365 × 5 = 36.5 PB
With 3x replication: 109.5 PB
```

**4. Bandwidth:**
```
Reads = 100M × 50 = 5B reads/day = 50K reads/sec
Peak = 150K reads/sec
Bandwidth = 150K × 500 KB (avg with images) = 75 GB/sec = 600 Gbps
With 90% CDN cache: 60 Gbps origin
```

**5. Servers:**
```
150K reads/sec / 1,000 per server = 150 servers
With buffer: 225 servers
```

</details>

### Problem 2: YouTube-like Video Service

**Requirements:**
- 2B users, 500M DAU
- 500M videos total
- Average video: 10 minutes, 50 MB
- Each user watches 30 minutes/day (3 videos)
- 100 videos uploaded per minute

**Calculate:**
1. Daily video uploads and storage
2. Bandwidth for streaming
3. Storage for 1 year
4. CDN requirements

<details>
<summary>Click to see solution</summary>

**1. Daily uploads:**
```
100 videos/min × 60 min × 24 hours = 144,000 videos/day
Storage: 144K × 50 MB = 7.2 TB/day
```

**2. Streaming bandwidth:**
```
Views: 500M users × 3 videos = 1.5B views/day
Per second: 1.5B / 100K = 15,000 views/sec
Peak: 45,000 views/sec
Bandwidth: 45K × 5 Mbps (streaming bitrate) = 225 Gbps
```

**3. 1-year storage:**
```
7.2 TB/day × 365 = 2,628 TB = 2.6 PB/year
Multiple qualities (360p, 720p, 1080p): 2.6 × 3 = 7.8 PB
With replication: 7.8 × 3 = 23.4 PB
```

**4. CDN:**
```
225 Gbps peak
With 95% CDN cache hit: 225 × 0.05 = 11.25 Gbps origin
CDN edge capacity: 225 Gbps
```

</details>

---

## 🎬 Conclusion

Back of the envelope calculations are essential for:
- ✅ Making informed design decisions
- ✅ Identifying potential bottlenecks
- ✅ Choosing the right technologies
- ✅ Planning infrastructure capacity
- ✅ Estimating costs

**Key takeaways:**
1. 📊 Always calculate QPS (queries per second)
2. 💾 Estimate storage with growth over time
3. 🌐 Account for bandwidth (ingress and egress)
4. ⚡ Consider response time requirements
5. 🖥️ Calculate server and infrastructure needs
6. 💰 Estimate costs to justify decisions

**Remember:** In interviews, the process matters more than perfect accuracy. Show your thinking, state assumptions, and validate results!

---

## 📖 Additional Resources

**Books:**
- "Designing Data-Intensive Applications" by Martin Kleppmann
- "System Design Interview" by Alex Xu

**Practice:**
- Work through all 20 system design problems in this repository
- Calculate capacity for each design
- Compare your estimates with real-world systems

**Real-world numbers:**
- Instagram: 2B users, 95M photos/day
- Twitter: 500M tweets/day
- YouTube: 500 hours of video uploaded per minute
- Netflix: 200M subscribers, 1B hours watched per week

Good luck with your system design interviews! 🚀
