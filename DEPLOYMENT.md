# Deployment Guide - Quiz Authoring Platform

This guide covers deploying your Quiz Authoring Platform to AWS EC2 with Docker, Nginx, and optional domain setup.

## 🎯 Overview

We'll deploy a containerized version of the application with:
- **AWS EC2**: Cloud hosting
- **Docker**: Application containerization  
- **Nginx**: Reverse proxy and static file serving
- **Uvicorn**: ASGI server for FastAPI
- **SQLite**: Database (can be upgraded to PostgreSQL for production)

## 📋 Prerequisites

- AWS account with EC2 access
- SSH client installed
- Domain name (optional, for custom URL)
- Basic command line knowledge

## 🚀 Step 1: Launch EC2 Instance

### 1.1 Create EC2 Instance

1. Log into AWS Console → EC2 Dashboard
2. Click "Launch Instance"
3. **Configure:**
   - **Name**: quiz-platform-server
   - **AMI**: Ubuntu Server 22.04 LTS (Free tier eligible)
   - **Instance Type**: t2.micro (Free tier) or t2.small (recommended)
   - **Key Pair**: Create new or select existing (save .pem file)
   - **Network Settings**:
     - Allow SSH (port 22) from your IP
     - Allow HTTP (port 80) from anywhere
     - Allow HTTPS (port 443) from anywhere
   - **Storage**: 8-20 GB (default is fine)

4. Click "Launch Instance"
5. Wait for instance to be "Running"
6. Note down the **Public IPv4 Address**

### 1.2 Connect to EC2

```bash
# Set permissions on your key file
chmod 400 your-key.pem

# SSH into instance
ssh -i your-key.pem ubuntu@YOUR_EC2_PUBLIC_IP
```

## 🛠️ Step 2: Install Dependencies on EC2

### 2.1 Update System

```bash
sudo apt update
sudo apt upgrade -y
```

### 2.2 Install Docker

```bash
# Install Docker
sudo apt install -y docker.io

# Start Docker service
sudo systemctl start docker
sudo systemctl enable docker

# Add user to docker group (to run without sudo)
sudo usermod -aG docker ubuntu

# Log out and back in for group changes to take effect
exit
# Then reconnect via SSH
```

### 2.3 Install Docker Compose

```bash
sudo apt install -y docker-compose
```

### 2.4 Install Git

```bash
sudo apt install -y git
```

## 📦 Step 3: Deploy Application

### 3.1 Transfer Code to EC2

**Option A: Via Git (Recommended)**

```bash
# Clone your repository
git clone YOUR_REPOSITORY_URL
cd quiz-platform
```

**Option B: Via SCP (if no Git repo)**

From your local machine:

```bash
# Compress project
tar -czf quiz-platform.tar.gz quiz-platform/

# Transfer to EC2
scp -i your-key.pem quiz-platform.tar.gz ubuntu@YOUR_EC2_PUBLIC_IP:~

# SSH to EC2 and extract
ssh -i your-key.pem ubuntu@YOUR_EC2_PUBLIC_IP
tar -xzf quiz-platform.tar.gz
cd quiz-platform
```

### 3.2 Create Dockerfile

Create `Dockerfile` in project root:

```dockerfile
# Multi-stage build for frontend
FROM node:18 AS frontend-build
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ ./
RUN npm run build

# Python backend
FROM python:3.11-slim
WORKDIR /app

# Install backend dependencies
COPY backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY backend/ ./

# Copy built frontend
COPY --from=frontend-build /app/frontend/dist /app/static

# Expose port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 3.3 Create docker-compose.yml

```yaml
version: '3.8'

services:
  app:
    build: .
    container_name: quiz-platform
    ports:
      - "8000:8000"
    volumes:
      - ./data:/app/data
    environment:
      - DATABASE_URL=sqlite:///./data/quiz_platform.db
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    container_name: quiz-nginx
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./frontend/dist:/usr/share/nginx/html:ro
    depends_on:
      - app
    restart: unless-stopped
```

### 3.4 Create Nginx Configuration

Create `nginx.conf`:

```nginx
events {
    worker_connections 1024;
}

http {
    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    upstream backend {
        server app:8000;
    }

    server {
        listen 80;
        server_name YOUR_DOMAIN_OR_IP;

        # Frontend static files
        location / {
            root /usr/share/nginx/html;
            try_files $uri $uri/ /index.html;
        }

        # Backend API
        location /api/ {
            proxy_pass http://backend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        # API docs
        location /api/docs {
            proxy_pass http://backend;
            proxy_set_header Host $host;
        }

        location /api/redoc {
            proxy_pass http://backend;
            proxy_set_header Host $host;
        }
    }
}
```

Replace `YOUR_DOMAIN_OR_IP` with your EC2 public IP or domain name.

### 3.5 Build and Run

```bash
# Build and start containers
docker-compose up -d --build

# Check status
docker-compose ps

# View logs
docker-compose logs -f
```

Your application should now be accessible at `http://YOUR_EC2_PUBLIC_IP`

## 🔐 Step 4: SSL/HTTPS Setup (Optional but Recommended)

### 4.1 Install Certbot

```bash
sudo apt install -y certbot python3-certbot-nginx
```

### 4.2 Obtain SSL Certificate

```bash
# Stop nginx temporarily
docker-compose stop nginx

# Get certificate
sudo certbot certonly --standalone -d your-domain.com

# Start nginx
docker-compose start nginx
```

### 4.3 Update Nginx for HTTPS

Update `nginx.conf`:

```nginx
server {
    listen 80;
    server_name your-domain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl;
    server_name your-domain.com;

    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;

    # ... rest of your nginx config
}
```

Update `docker-compose.yml` to mount certificates:

```yaml
nginx:
  # ... other config
  volumes:
    - /etc/letsencrypt:/etc/letsencrypt:ro
```

Restart:

```bash
docker-compose restart nginx
```

## 🔧 Step 5: Maintenance & Monitoring

### View Application Logs

```bash
# All logs
docker-compose logs -f

# Backend only
docker-compose logs -f app

# Nginx only
docker-compose logs -f nginx
```

### Restart Application

```bash
docker-compose restart
```

### Update Application

```bash
# Pull latest changes (if using Git)
git pull

# Rebuild and restart
docker-compose up -d --build
```

### Stop Application

```bash
docker-compose down
```

### Backup Database

```bash
# Copy database file
cp data/quiz_platform.db data/quiz_platform_backup_$(date +%Y%m%d).db
```

## 🌐 Step 6: Domain Setup (Optional)

### 6.1 Point Domain to EC2

1. Go to your domain registrar (GoDaddy, Namecheap, etc.)
2. Add an **A Record**:
   - **Host**: @ (or your subdomain)
   - **Points to**: Your EC2 Public IP
   - **TTL**: Automatic or 300

3. Wait for DNS propagation (5-30 minutes)

### 6.2 Update Backend CORS

Update `backend/main.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://your-domain.com",
        "https://your-domain.com"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

Rebuild:

```bash
docker-compose up -d --build
```

## ✅ Verification Checklist

- [ ] EC2 instance is running
- [ ] Can SSH into EC2
- [ ] Docker and Docker Compose installed
- [ ] Application containers are running (`docker-compose ps`)
- [ ] Can access application via `http://YOUR_EC2_IP`
- [ ] Can create a quiz via the UI
- [ ] Can view and delete quizzes
- [ ] API docs accessible at `http://YOUR_EC2_IP/api/docs`
- [ ] (Optional) HTTPS working with valid SSL certificate
- [ ] (Optional) Domain pointing to application

## 🐛 Troubleshooting

### Can't connect to EC2
- Check Security Group allows HTTP (80) and HTTPS (443)
- Verify instance is running
- Check public IP is correct

### Docker errors
```bash
# Check Docker status
sudo systemctl status docker

# Restart Docker
sudo systemctl restart docker
```

### Application not accessible
```bash
# Check if containers are running
docker-compose ps

# Check logs for errors
docker-compose logs

# Restart application
docker-compose restart
```

### Database errors
```bash
# Check if data directory exists
ls -la data/

# Create if missing
mkdir -p data
```

## 📊 Cost Estimation

**AWS Free Tier (First Year):**
- t2.micro instance: Free for 750 hours/month
- Data transfer: 15 GB/month free

**After Free Tier:**
- t2.micro: ~$8-10/month
- t2.small: ~$16-20/month
- Additional costs: Data transfer, storage (minimal)

## 🎉 Deployment Complete!

Your Quiz Authoring Platform is now live and publicly accessible!

**Next Steps:**
- Monitor application logs regularly
- Set up automated backups
- Consider upgrading to PostgreSQL for production
- Implement user authentication if needed
- Set up monitoring (CloudWatch, etc.)

---

**Questions or Issues?** Check the main [README.md](./README.md) or AWS documentation.
