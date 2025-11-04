# Railway Deployment Guide

## 📦 Files Created for Railway

1. **`railway.json`** - Railway configuration
2. **`runtime.txt`** - Python version specification
3. **`Procfile`** - Process file for Railway
4. **`nixpacks.toml`** - Nixpacks build configuration

## 🚀 Deployment Steps

### 1. Install Railway CLI (Optional)
```bash
npm install -g @railway/cli
```

### 2. Deploy via Railway Dashboard

1. Go to [railway.app](https://railway.app)
2. Click "New Project"
3. Select "Deploy from GitHub repo" (or "Empty Project")
4. Connect your GitHub repository
5. Railway will automatically detect the project and deploy

### 3. Set Environment Variables

In Railway dashboard, go to your project → Variables → Add:

```env
MONGO_URI=mongodb://your-mongo-connection-string
DB_NAME=dagg_api
GOOGLE_API_KEY=your_google_api_key
CEREBRAS_API_KEY=your_cerebras_api_key (optional)
PORT=8000 (Railway sets this automatically)
```

### 4. Important Notes

- **Port**: Railway sets `$PORT` automatically - don't hardcode it
- **MongoDB**: Use Railway's MongoDB service or external MongoDB (MongoDB Atlas)
- **Start Command**: Railway uses `Procfile` or `railway.json` startCommand

## 🔧 Configuration Files

### railway.json
- Defines build and deploy commands
- Uses Nixpacks builder
- Sets restart policy

### Procfile
- Defines the web process
- Uses `$PORT` environment variable

### runtime.txt
- Specifies Python version (3.12.7)

### nixpacks.toml
- Alternative build configuration
- Specifies Python and build steps

## 🌐 After Deployment

Your API will be available at:
- Railway provides a URL like: `https://your-app.railway.app`
- Update your Laravel `.env` to use this URL:
  ```env
  FASTAPI_URL=https://your-app.railway.app
  ```

## 📝 Checklist

- [ ] Push code to GitHub
- [ ] Connect repo to Railway
- [ ] Set environment variables in Railway
- [ ] Deploy
- [ ] Test endpoint: `https://your-app.railway.app/docs`
- [ ] Update Laravel API URL

## 🐛 Troubleshooting

### Build Fails
- Check `requirements.txt` is correct
- Verify Python version in `runtime.txt`
- Check Railway build logs

### App Crashes
- Check environment variables are set
- Verify MongoDB connection string
- Check logs in Railway dashboard

### Port Issues
- Ensure using `$PORT` not hardcoded port
- Railway automatically sets PORT

