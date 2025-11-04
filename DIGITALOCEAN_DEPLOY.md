# DigitalOcean Droplet Deployment Guide

## 🐳 Docker Deployment on DigitalOcean

### Prerequisites
- DigitalOcean droplet with Docker installed
- Existing Node.js app running (if applicable)
- MongoDB connection string ready

## 📦 Files for Deployment

1. **`Dockerfile`** - Builds the FastAPI application
2. **`docker-compose.yml`** - Orchestrates the service
3. **`.env.example`** - Template for environment variables

## 🚀 Deployment Steps

### Step 1: Prepare Your Droplet

SSH into your DigitalOcean droplet:
```bash
ssh root@your-droplet-ip
```

Ensure Docker and Docker Compose are installed:
```bash
# Check Docker
docker --version
docker-compose --version

# If not installed:
apt-get update
apt-get install -y docker.io docker-compose
```

### Step 2: Clone/Upload Your Code

If using Git:
```bash
cd /path/to/your/apps
git clone your-repo-url
cd ai_health_integrated_system
```

Or upload files via SCP:
```bash
# From your local machine
scp -r . root@your-droplet-ip:/path/to/apps/ai-health-api
```

### Step 3: Set Up Environment Variables

Create `.env` file:
```bash
nano .env
```

Add:
```env
MONGO_URI=mongodb://your-mongodb-connection-string
DB_NAME=dagg_api
GOOGLE_API_KEY=your_google_api_key
CEREBRAS_API_KEY=your_cerebras_api_key
PORT=8000
```

### Step 4: Build and Run with Docker Compose

```bash
# Build the image
docker-compose build

# Start the service
docker-compose up -d

# Check logs
docker-compose logs -f

# Check if running
docker-compose ps
```

### Step 5: Configure Nginx (If needed)

If you have Nginx for your Node.js app, add a new location:

```nginx
# /etc/nginx/sites-available/default
server {
    # ... existing Node.js config ...

    # FastAPI service
    location /api/ {
        proxy_pass http://localhost:8000/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Then reload Nginx:
```bash
nginx -t
systemctl reload nginx
```

## 🔧 Alternative: Standalone Docker (Without Compose)

```bash
# Build image
docker build -t ai-health-fastapi .

# Run container
docker run -d \
  --name ai-health-fastapi \
  -p 8000:8000 \
  --env-file .env \
  --restart unless-stopped \
  ai-health-fastapi

# View logs
docker logs -f ai-health-fastapi
```

## 📝 Managing the Service

### View Logs
```bash
docker-compose logs -f fastapi-app
# or
docker logs -f ai-health-fastapi
```

### Restart Service
```bash
docker-compose restart
# or
docker restart ai-health-fastapi
```

### Stop Service
```bash
docker-compose down
# or
docker stop ai-health-fastapi
```

### Update Code
```bash
git pull  # or upload new files
docker-compose build
docker-compose up -d
```

## 🔐 Port Configuration

If port 8000 is already used by your Node.js app:

1. **Option 1**: Change FastAPI port in `docker-compose.yml`:
   ```yaml
   ports:
     - "8001:8000"  # External:Internal
   ```

2. **Option 2**: Use Nginx reverse proxy (recommended)

## ✅ Verification

Test your API:
```bash
curl http://localhost:8000/
curl http://localhost:8000/docs
```

Or from your domain:
```bash
curl https://yourdomain.com/api/
```

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Check what's using port 8000
netstat -tulpn | grep 8000
# Change port in docker-compose.yml
```

### Container Won't Start
```bash
# Check logs
docker-compose logs fastapi-app
# Check environment variables
docker-compose exec fastapi-app env
```

### MongoDB Connection Issues
- Verify MONGO_URI is correct
- Check MongoDB is accessible from droplet
- Whitelist droplet IP in MongoDB firewall

## 📋 Quick Reference

```bash
# Start
docker-compose up -d

# Stop
docker-compose down

# Restart
docker-compose restart

# View logs
docker-compose logs -f

# Rebuild after code changes
docker-compose build && docker-compose up -d
```

