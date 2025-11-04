#!/bin/bash
# Deployment script for DigitalOcean droplet

set -e

echo "🚀 Starting deployment..."

# Check if .env exists
if [ ! -f .env ]; then
    echo "❌ Error: .env file not found!"
    echo "Please create .env file from .env.example"
    exit 1
fi

# Build and deploy
echo "📦 Building Docker image..."
docker-compose build

echo "🔄 Stopping existing containers..."
docker-compose down

echo "✅ Starting services..."
docker-compose up -d

echo "📋 Checking service status..."
docker-compose ps

echo "📝 Recent logs:"
docker-compose logs --tail=20

echo "✅ Deployment complete!"
echo "🌐 API should be available at: http://localhost:8000"
echo "📚 Docs available at: http://localhost:8000/docs"

