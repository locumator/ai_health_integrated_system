# Quick Deployment Guide for /var/www/bot Droplet

## 🚀 Deployment Steps on Your Droplet

### Step 1: SSH into Your Droplet
```bash
ssh root@your-droplet-ip
```

### Step 2: Navigate and Create Directory
```bash
cd /var/www
mkdir -p ai-health-api
cd ai-health-api
```

### Step 3: Clone or Upload Your Code

**Option A: Using Git**
```bash
git clone your-repo-url .
# Switch to your branch if needed
git checkout your-branch-name
```

**Option B: Upload via SCP (from your local machine)**
```bash
# From your local machine, in the project directory:
scp -r . root@your-droplet-ip:/var/www/ai-health-api
```

### Step 4: Create .env File
```bash
cd /var/www/ai-health-api
nano .env
```

Add:
```env
MONGO_URI=mongodb://your-mongodb-connection-string
DB_NAME=dagg_api
GOOGLE_API_KEY=your_google_api_key
CEREBRAS_API_KEY=your_cerebras_api_key
```

Save: `Ctrl+X`, then `Y`, then `Enter`

### Step 5: Deploy with Docker Compose
```bash
# Build and start
docker-compose up -d --build

# Or use the deploy script
chmod +x deploy.sh
./deploy.sh
```

### Step 6: Check if Running
```bash
# Check container status
docker-compose ps

# Check logs
docker-compose logs -f

# Test API
curl http://localhost:8001/
```

## 📝 Directory Structure

Your droplet will have:
```
/var/www/
├── bot/              # Your existing Node.js bot
└── ai-health-api/    # This FastAPI application
    ├── Dockerfile
    ├── docker-compose.yml
    ├── .env
    ├── app/
    └── ...
```

## 🔧 Port Configuration

- **FastAPI runs on**: `http://localhost:8001` (inside droplet)
- **Node.js bot**: Likely on port 8000 or 3000
- **No conflicts**: They run on different ports

## 🌐 Nginx Configuration (If Needed)

If you want to access FastAPI via your domain, add to Nginx:

```nginx
# /etc/nginx/sites-available/default

# Your existing Node.js bot config
server {
    # ... existing bot config ...
}

# FastAPI app
location /api/ {
    proxy_pass http://localhost:8001/;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
}
```

Then reload Nginx:
```bash
nginx -t
systemctl reload nginx
```

## 🔄 Managing the Service

```bash
# Start
docker-compose up -d

# Stop
docker-compose down

# Restart
docker-compose restart

# View logs
docker-compose logs -f

# Update code
cd /var/www/ai-health-api
git pull  # or upload new files
docker-compose build
docker-compose up -d
```

## ✅ Verification

```bash
# Check container is running
docker ps | grep ai-health-fastapi

# Test endpoint
curl http://localhost:8001/
curl http://localhost:8001/docs

# Check logs for errors
docker-compose logs fastapi-app
```

