# Storage Systems

Storage systems form the backbone of modern applications. Understanding different storage types and when to use them is critical for system design.

---

## 📦 Storage Types Overview

| Type | Use Case | Examples | Access Pattern |
|------|----------|----------|----------------|
| **Block Storage** | Databases, VMs | EBS, SAN | Low-level, high performance |
| **Object Storage** | Media, backups | S3, Blob Storage | HTTP API, scalable |
| **File Storage** | Shared files | EFS, NFS | File system interface |
| **Database** | Structured data | PostgreSQL, MongoDB | Query language |
| **Cache** | Hot data | Redis, Memcached | Key-value, in-memory |

---

## 🗄️ Block Storage

Block storage divides data into fixed-size blocks. Each block has a unique address. The OS treats it as a hard drive.

### Characteristics

**Performance:**
- ✅ Low latency (< 10ms)
- ✅ High IOPS (10,000+ operations/sec)
- ✅ Consistent performance

**Use Cases:**
- Databases (MySQL, PostgreSQL)
- Virtual machines
- High-performance applications

**Examples:**
- AWS EBS (Elastic Block Store)
- Azure Disk Storage
- GCP Persistent Disks
- Physical SAN/NAS

### Block Storage Types

```
┌─────────────────────────────────────┐
│         Block Storage Types         │
├─────────────────────────────────────┤
│                                     │
│  HDD (Hard Disk Drive)              │
│  • Magnetic spinning disks          │
│  • 100-200 IOPS                     │
│  • Low cost ($0.045/GB/month)       │
│  • Use: Backups, logs               │
│                                     │
│  SSD (Solid State Drive)            │
│  • Flash memory                     │
│  • 3,000-16,000 IOPS                │
│  • Medium cost ($0.10/GB/month)     │
│  • Use: General purpose databases   │
│                                     │
│  Provisioned IOPS SSD               │
│  • Guaranteed performance           │
│  • Up to 64,000 IOPS                │
│  • High cost ($0.125/GB/month)      │
│  • Use: High-traffic databases      │
│                                     │
└─────────────────────────────────────┘
```

### Example: Database Setup

```python
# Mount EBS volume to EC2 instance
# 1. Attach volume in AWS console
# 2. Format and mount

import subprocess

def setup_database_storage():
    # Format volume
    subprocess.run(['mkfs', '-t', 'ext4', '/dev/xvdf'])
    
    # Create mount point
    subprocess.run(['mkdir', '-p', '/data/mysql'])
    
    # Mount
    subprocess.run(['mount', '/dev/xvdf', '/data/mysql'])
    
    # Add to /etc/fstab for auto-mount on boot
    with open('/etc/fstab', 'a') as f:
        f.write('/dev/xvdf  /data/mysql  ext4  defaults,nofail  0  2\n')
```

**RAID Configurations:**

```
RAID 0 (Striping):
  • Data split across disks
  • 2x performance
  • 0 redundancy (one disk fails = data loss)
  
RAID 1 (Mirroring):
  • Data copied to multiple disks
  • Redundancy (can lose 1 disk)
  • No performance gain
  
RAID 10 (1+0):
  • Combination of striping and mirroring
  • High performance + redundancy
  • Requires 4+ disks
```

---

## ☁️ Object Storage

Object storage stores data as objects with metadata. Accessed via HTTP API. Infinitely scalable.

### Characteristics

**Scalability:**
- ✅ Unlimited storage
- ✅ Automatic scaling
- ✅ No capacity planning

**Durability:**
- ✅ 99.999999999% (11 9's) durability
- ✅ Automatic replication
- ✅ Versioning

**Use Cases:**
- Media files (images, videos)
- Backups and archives
- Static website hosting
- Data lakes

**Examples:**
- AWS S3
- Azure Blob Storage
- Google Cloud Storage
- MinIO (self-hosted)

### Object Structure

```
Object = Data + Metadata + Unique Key

Example:
  Key: /users/123/profile.jpg
  Data: <binary image data>
  Metadata:
    - Content-Type: image/jpeg
    - Content-Length: 245678
    - Last-Modified: 2024-01-15T10:00:00Z
    - Custom: user-id=123, uploaded-by=app
```

### S3 Architecture

```
┌────────────────────────────────────────┐
│           S3 Bucket: my-app            │
├────────────────────────────────────────┤
│                                        │
│  /images/                              │
│    ├── product-1.jpg                   │
│    ├── product-2.jpg                   │
│    └── user-avatar-123.png             │
│                                        │
│  /videos/                              │
│    ├── tutorial-1.mp4                  │
│    └── demo.mp4                        │
│                                        │
│  /backups/                             │
│    ├── db-backup-2024-01-15.sql.gz     │
│    └── logs-2024-01-14.tar.gz          │
│                                        │
└────────────────────────────────────────┘

Access:
  https://my-app.s3.amazonaws.com/images/product-1.jpg
```

### Using S3 (Python)

```python
import boto3
from botocore.exceptions import ClientError

s3 = boto3.client('s3')

# Upload file
def upload_file(file_path, bucket, object_key):
    try:
        s3.upload_file(
            file_path,
            bucket,
            object_key,
            ExtraArgs={
                'ContentType': 'image/jpeg',
                'Metadata': {
                    'uploaded-by': 'user-123',
                    'original-name': 'vacation.jpg'
                }
            }
        )
        print(f"Uploaded: {object_key}")
    except ClientError as e:
        print(f"Error: {e}")

# Download file
def download_file(bucket, object_key, file_path):
    s3.download_file(bucket, object_key, file_path)

# Generate presigned URL (temporary access)
def generate_presigned_url(bucket, object_key, expiration=3600):
    url = s3.generate_presigned_url(
        'get_object',
        Params={'Bucket': bucket, 'Key': object_key},
        ExpiresIn=expiration  # 1 hour
    )
    return url

# List objects
def list_objects(bucket, prefix=''):
    response = s3.list_objects_v2(Bucket=bucket, Prefix=prefix)
    for obj in response.get('Contents', []):
        print(f"{obj['Key']} - {obj['Size']} bytes")

# Delete object
def delete_object(bucket, object_key):
    s3.delete_object(Bucket=bucket, Key=object_key)
```

### S3 Storage Classes

```
┌──────────────────────────────────────────────────────┐
│              S3 Storage Classes                      │
├──────────────────────────────────────────────────────┤
│                                                      │
│  Standard (Default)                                  │
│  • Frequently accessed data                          │
│  • $0.023/GB/month                                   │
│  • 99.99% availability                               │
│                                                      │
│  Intelligent-Tiering                                 │
│  • Automatic cost optimization                       │
│  • Moves between tiers based on access              │
│  • $0.023/GB/month + $0.0025/1000 objects           │
│                                                      │
│  Infrequent Access (IA)                              │
│  • Accessed less than once a month                   │
│  • $0.0125/GB/month + retrieval fee                  │
│  • 99.9% availability                                │
│                                                      │
│  Glacier (Archive)                                   │
│  • Long-term archive (retrieval: mins to hours)      │
│  • $0.004/GB/month                                   │
│  • Use: Backups, compliance                          │
│                                                      │
│  Glacier Deep Archive                                │
│  • Lowest cost (retrieval: 12-48 hours)              │
│  • $0.00099/GB/month                                 │
│  • Use: 7-10 year retention                          │
│                                                      │
└──────────────────────────────────────────────────────┘
```

### Lifecycle Policies

Automatically transition objects between storage classes:

```python
lifecycle_policy = {
    'Rules': [
        {
            'Id': 'Move old logs to IA',
            'Status': 'Enabled',
            'Prefix': 'logs/',
            'Transitions': [
                {
                    'Days': 30,
                    'StorageClass': 'STANDARD_IA'
                },
                {
                    'Days': 90,
                    'StorageClass': 'GLACIER'
                }
            ],
            'Expiration': {
                'Days': 365  # Delete after 1 year
            }
        }
    ]
}

s3.put_bucket_lifecycle_configuration(
    Bucket='my-bucket',
    LifecycleConfiguration=lifecycle_policy
)
```

### Multipart Upload (Large Files)

For files > 100 MB:

```python
def multipart_upload(file_path, bucket, object_key):
    # Initiate multipart upload
    response = s3.create_multipart_upload(
        Bucket=bucket,
        Key=object_key
    )
    upload_id = response['UploadId']
    
    # Upload parts (5 MB each)
    part_size = 5 * 1024 * 1024  # 5 MB
    parts = []
    
    with open(file_path, 'rb') as f:
        part_number = 1
        while True:
            data = f.read(part_size)
            if not data:
                break
            
            # Upload part
            response = s3.upload_part(
                Bucket=bucket,
                Key=object_key,
                PartNumber=part_number,
                UploadId=upload_id,
                Body=data
            )
            
            parts.append({
                'PartNumber': part_number,
                'ETag': response['ETag']
            })
            part_number += 1
    
    # Complete upload
    s3.complete_multipart_upload(
        Bucket=bucket,
        Key=object_key,
        UploadId=upload_id,
        MultipartUpload={'Parts': parts}
    )
```

**Benefits:**
- ✅ Upload large files (up to 5 TB)
- ✅ Resume on failure
- ✅ Parallel uploads (faster)

---

## 📁 File Storage

File storage provides a file system interface (folders, files). Shared across multiple servers.

### Characteristics

**Access:**
- ✅ POSIX-compliant file system
- ✅ Hierarchical structure (folders)
- ✅ Concurrent access from multiple servers

**Use Cases:**
- Shared application files
- Content management systems
- Web servers (multiple instances)
- Big data analytics

**Examples:**
- AWS EFS (Elastic File System)
- Azure Files
- Google Filestore
- NFS (Network File System)

### Architecture

```
┌──────────┐      ┌──────────┐      ┌──────────┐
│  Web     │      │  Web     │      │  Web     │
│ Server 1 │      │ Server 2 │      │ Server 3 │
└────┬─────┘      └────┬─────┘      └────┬─────┘
     │                 │                 │
     └────────┬────────┴────────┬────────┘
              │                 │
              ▼                 ▼
        ┌──────────────────────────┐
        │  EFS (Shared Storage)    │
        │  /var/www/uploads/       │
        │  /var/www/static/        │
        └──────────────────────────┘
```

### Using EFS

```bash
# Mount EFS on EC2 instances
# 1. Install NFS client
sudo yum install -y nfs-utils

# 2. Create mount point
sudo mkdir -p /mnt/efs

# 3. Mount EFS
sudo mount -t nfs4 -o nfsvers=4.1 \
  fs-12345678.efs.us-east-1.amazonaws.com:/ /mnt/efs

# 4. Auto-mount on boot (add to /etc/fstab)
echo "fs-12345678.efs.us-east-1.amazonaws.com:/ /mnt/efs nfs4 defaults,_netdev 0 0" | sudo tee -a /etc/fstab
```

```python
# Application using shared storage
def upload_file(file):
    # All web servers write to same location
    file_path = f'/mnt/efs/uploads/{file.filename}'
    file.save(file_path)
    
    return f'https://cdn.example.com/uploads/{file.filename}'

def serve_file(filename):
    # All web servers can read from same location
    file_path = f'/mnt/efs/uploads/{filename}'
    return send_file(file_path)
```

---

## 🌐 Content Delivery Network (CDN)

CDNs cache and serve static content from edge locations close to users.

### Architecture

```
User in Tokyo                  User in New York
     │                              │
     ▼                              ▼
┌─────────┐                    ┌─────────┐
│  CDN    │                    │  CDN    │
│  Edge   │                    │  Edge   │
│  Tokyo  │                    │New York │
└────┬────┘                    └────┬────┘
     │                              │
     └───────────┬──────────────────┘
                 │ Cache MISS
                 ▼
           ┌───────────┐
           │  Origin   │
           │  Server   │
           │  (S3)     │
           └───────────┘
```

### How CDN Works

```
1. User requests: https://cdn.example.com/images/logo.png

2. DNS resolves to nearest CDN edge location

3. CDN checks cache:
   • HIT: Return cached file (fast!)
   • MISS: Fetch from origin, cache, return

4. Subsequent requests served from cache (< 10ms)
```

### CDN Benefits

```
Without CDN:
  User (Tokyo) → Origin (US West) → 200ms latency
  
With CDN:
  User (Tokyo) → CDN Edge (Tokyo) → 10ms latency
  
Benefits:
  ✅ Faster load times (10-20x)
  ✅ Reduced origin load (90% served from cache)
  ✅ DDoS protection (distributed)
  ✅ Lower bandwidth costs
```

### CloudFront Configuration

```python
import boto3

cloudfront = boto3.client('cloudfront')

# Create CDN distribution
distribution_config = {
    'Origins': {
        'Quantity': 1,
        'Items': [{
            'Id': 's3-origin',
            'DomainName': 'my-bucket.s3.amazonaws.com',
            'S3OriginConfig': {
                'OriginAccessIdentity': ''
            }
        }]
    },
    'DefaultCacheBehavior': {
        'TargetOriginId': 's3-origin',
        'ViewerProtocolPolicy': 'redirect-to-https',
        'AllowedMethods': {
            'Quantity': 2,
            'Items': ['GET', 'HEAD']
        },
        'Compress': True,  # Gzip compression
        'MinTTL': 0,
        'DefaultTTL': 86400,  # 24 hours
        'MaxTTL': 31536000    # 1 year
    },
    'Comment': 'CDN for my-app',
    'Enabled': True
}
```

### Cache Control Headers

```python
# Upload to S3 with cache headers
s3.upload_file(
    'logo.png',
    'my-bucket',
    'images/logo.png',
    ExtraArgs={
        'ContentType': 'image/png',
        'CacheControl': 'public, max-age=31536000, immutable',  # 1 year
        'Metadata': {
            'version': '1.0'
        }
    }
)

# Different cache policies:
# Static assets (logo, CSS): max-age=31536000 (1 year)
# HTML: max-age=0, must-revalidate (always check)
# API responses: no-cache (don't cache)
```

### Cache Invalidation

```python
# Invalidate (purge) CDN cache when content changes
def invalidate_cdn_cache(paths):
    cloudfront.create_invalidation(
        DistributionId='E1234567890ABC',
        InvalidationBatch={
            'Paths': {
                'Quantity': len(paths),
                'Items': paths
            },
            'CallerReference': str(time.time())
        }
    )

# Example:
invalidate_cdn_cache(['/images/logo.png', '/css/*'])
```

**Cache Invalidation Strategies:**
```
1. Manual Invalidation:
   • Slow (15-30 minutes)
   • Costs money ($0.005 per path after first 1000)
   
2. Versioned URLs (Recommended):
   • logo.png → logo-v2.png
   • /static/v1/app.js → /static/v2/app.js
   • Old version expires naturally
   • No invalidation needed
   
3. Query String:
   • logo.png?v=2
   • logo.png?hash=abc123
```

---

## 🗂️ Distributed File Systems

For big data and analytics workloads.

### HDFS (Hadoop Distributed File System)

```
Architecture:

┌────────────┐
│ NameNode   │  ← Metadata (file locations)
└─────┬──────┘
      │
      ├──────────┬──────────┬──────────┐
      ▼          ▼          ▼          ▼
┌──────────┐ ┌──────────┐ ┌──────────┐
│DataNode 1│ │DataNode 2│ │DataNode 3│
│ Block 1  │ │ Block 1  │ │ Block 2  │
│ Block 3  │ │ Block 2  │ │ Block 3  │
└──────────┘ └──────────┘ └──────────┘

Replication: 3x (default)
Block size: 128 MB (default)
```

**Example:**
```
File: video.mp4 (500 MB)

Split into blocks:
  • Block 1 (128 MB) → DataNode 1, 2, 3
  • Block 2 (128 MB) → DataNode 2, 3, 4
  • Block 3 (128 MB) → DataNode 3, 4, 5
  • Block 4 (116 MB) → DataNode 4, 5, 1

Benefits:
  ✅ Fault tolerance (3 copies)
  ✅ Parallel processing (MapReduce)
  ✅ Scalable (add more DataNodes)
```

---

## 💡 Storage Selection Guide

### Decision Matrix

```
┌─────────────────────────────────────────────────────────┐
│                 Storage Decision Tree                   │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Need: Database storage?                                │
│    → YES: Block Storage (EBS)                           │
│           • High IOPS, low latency                      │
│           • Provisioned IOPS for production DBs         │
│                                                         │
│  Need: Media files (images/videos)?                     │
│    → YES: Object Storage (S3)                           │
│           • Unlimited scale                             │
│           • + CDN for fast delivery                     │
│           • Lifecycle policies for archival             │
│                                                         │
│  Need: Shared files across servers?                     │
│    → YES: File Storage (EFS)                            │
│           • POSIX file system                           │
│           • Concurrent access                           │
│                                                         │
│  Need: Big data analytics?                              │
│    → YES: Distributed File System (HDFS)                │
│           • Petabyte scale                              │
│           • Parallel processing                         │
│                                                         │
│  Need: Fast access to data?                             │
│    → YES: Cache (Redis/Memcached)                       │
│           • In-memory                                   │
│           • < 1ms latency                               │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### Comparison Table

| Requirement | Block | Object | File | Cache |
|-------------|-------|--------|------|-------|
| **Latency** | < 10ms | 50-200ms | 10-50ms | < 1ms |
| **Throughput** | GB/s | MB/s | GB/s | GB/s |
| **Scalability** | TB | PB+ | PB | GB |
| **Cost ($/GB/mo)** | $0.10 | $0.023 | $0.30 | $0.50+ |
| **Durability** | 99.9% | 99.999999999% | 99.99% | None |
| **Use Case** | Databases | Media | Shared files | Hot data |

---

## 🎯 Interview Tips

**Key Points to Cover:**
1. ✅ Block vs Object vs File storage differences
2. ✅ When to use S3 vs EBS vs EFS
3. ✅ CDN benefits and architecture
4. ✅ Storage classes and lifecycle policies
5. ✅ Multipart upload for large files

**Common Questions:**
- "How would you store user profile pictures?" → S3 + CloudFront CDN
- "How would you store 10TB of logs?" → S3 with lifecycle to Glacier
- "Database keeps running out of disk space?" → EBS volume expansion or sharding
- "Slow image loading for global users?" → CDN with edge caching

**Red Flags:**
- ❌ Using block storage for media files (expensive, not scalable)
- ❌ Not using CDN for static content
- ❌ Storing large files in database (BLOB)
- ❌ Not considering storage costs

---

**Next:** [Networking](08_networking.md)
