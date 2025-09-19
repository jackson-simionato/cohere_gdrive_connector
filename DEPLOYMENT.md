# Google Drive Connector - Render Deployment Guide

This guide will help you deploy your Google Drive connector to Render.

## 🚀 Deployment Options

### Option 1: Using Render Dashboard (Recommended)

1. **Push your code to GitHub**
   ```bash
   git add .
   git commit -m "Add Google Drive connector with Render deployment config"
   git push origin main
   ```

2. **Connect to Render**
   - Go to [Render Dashboard](https://dashboard.render.com)
   - Click "New" → "Web Service"
   - Connect your GitHub repository
   - Select the `gdrive` folder as the root directory

3. **Configure the service**
   - **Name**: `gdrive-connector` (or your preferred name)
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn --bind 0.0.0.0:$PORT wsgi:app`

4. **Set Environment Variables**
   In the Render dashboard, go to "Environment" and add:
   ```
   GDRIVE_SERVICE_ACCOUNT_INFO = {"type":"service_account","project_id":"your-project",...}
   GDRIVE_CONNECTOR_API_KEY = your-secure-api-key
   GDRIVE_SEARCH_LIMIT = 10
   ```

### Option 2: Using render.yaml (Blueprints)

1. **Push your code to GitHub** (same as above)

2. **Deploy with Blueprint**
   - Go to [Render Dashboard](https://dashboard.render.com)
   - Click "New" → "Blueprint"
   - Connect your GitHub repository
   - Select the `render.yaml` file

## 🔧 Environment Variables Setup

### Required Variables

1. **GDRIVE_SERVICE_ACCOUNT_INFO**
   - Copy the JSON from your local `.env` file
   - Paste it as a single line in Render dashboard
   - Make sure to escape quotes properly

2. **GDRIVE_CONNECTOR_API_KEY**
   - Use the same API key from your local `.env` file
   - Or generate a new secure key

### Optional Variables

- **GDRIVE_SEARCH_LIMIT**: Number of results (default: 10)
- **GDRIVE_FOLDER_ID**: Specific folder to search (optional)

## 🧪 Testing Your Deployment

Once deployed, test your connector:

```bash
curl -X POST "https://your-app-name.onrender.com/search" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "test"}'
```

## 📋 Pre-deployment Checklist

- [ ] Code pushed to GitHub
- [ ] Environment variables ready
- [ ] Google Drive files shared with service account
- [ ] Service account has proper permissions
- [ ] Test files (Google Docs/Sheets/Slides) created

## 🔍 Troubleshooting

### Common Issues

1. **Build fails**: Check Python version compatibility
2. **Runtime errors**: Verify environment variables are set correctly
3. **No results**: Ensure Google Drive files are shared with service account
4. **Authentication errors**: Double-check service account JSON format

### Debug Commands

```bash
# Check if service is running
curl https://your-app-name.onrender.com/health

# Test search endpoint
curl -X POST "https://your-app-name.onrender.com/search" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "test"}'
```

## 🔗 Integration with Cohere

Once deployed, register your connector with Cohere:

```bash
curl -X POST 'https://api.cohere.ai/v1/connectors' \
  --header 'Accept: */*' \
  --header 'Authorization: Bearer YOUR_COHERE_API_KEY' \
  --header 'Content-Type: application/json' \
  --data-raw '{
    "name": "Google Drive Connector",
    "url": "https://your-app-name.onrender.com",
    "api_key": "YOUR_CONNECTOR_API_KEY"
  }'
```

## 📊 Monitoring

- Check Render dashboard for logs and metrics
- Monitor response times and error rates
- Set up alerts for service downtime

## 🔄 Updates

To update your deployment:
1. Make changes locally
2. Test locally
3. Push to GitHub
4. Render will automatically redeploy
