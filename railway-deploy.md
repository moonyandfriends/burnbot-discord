# Railway Deployment Guide

This guide will help you deploy the STRD Burn Monitor Discord Bot to Railway.

## Prerequisites

1. **Railway Account**: Sign up at [railway.app](https://railway.app)
2. **Discord Bot Token**: Get your bot token from [Discord Developer Portal](https://discord.com/developers/applications)
3. **Optional Webhook URL**: Create a Discord webhook for notifications

## Step 1: Prepare Your Repository

Make sure your repository contains all the necessary files:
- `strd_burn_monitor.py` - Main bot script
- `config.py` - Configuration file
- `requirements.txt` - Python dependencies
- `Procfile` - Railway process file
- `runtime.txt` - Python version specification
- `railway.json` - Railway configuration

## Step 2: Deploy to Railway

### Option A: Deploy from GitHub

1. **Connect GitHub**:
   - Go to [Railway Dashboard](https://railway.app/dashboard)
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your `burnbot-discord` repository

2. **Configure Environment Variables**:
   - In your Railway project, go to the "Variables" tab
   - Add the following environment variables:

```
burnbot_discord_token=your_discord_bot_token_here
burnbot_logs_webhookurl=your_discord_webhook_url_here
burnbot_csv_url=https://storage.googleapis.com/stride-public-data/burn_data/strd_burn.csv
```

3. **Deploy**:
   - Railway will automatically detect the Python project
   - It will install dependencies from `requirements.txt`
   - The bot will start using the `Procfile`

### Option B: Deploy from Local Files

1. **Install Railway CLI**:
   ```bash
   npm install -g @railway/cli
   ```

2. **Login to Railway**:
   ```bash
   railway login
   ```

3. **Initialize Project**:
   ```bash
   railway init
   ```

4. **Set Environment Variables**:
   ```bash
   railway variables set burnbot_discord_token=your_discord_bot_token_here
   railway variables set burnbot_logs_webhookurl=your_discord_webhook_url_here
   railway variables set burnbot_csv_url=https://storage.googleapis.com/stride-public-data/burn_data/strd_burn.csv
   ```

5. **Deploy**:
   ```bash
   railway up
   ```

## Step 3: Update Configuration for Railway

The bot will automatically use environment variables. Update your `config.py` to support Railway:

```python
import os

# Discord Bot Configuration
burnbot_discord_token = os.getenv("burnbot_discord_token", "YOUR_DISCORD_BOT_TOKEN_HERE")
burnbot_logs_webhookurl = os.getenv("burnbot_logs_webhookurl", "YOUR_WEBHOOK_URL_HERE")

# Data Source Configuration
burnbot_csv_url = os.getenv("burnbot_csv_url", 'https://storage.googleapis.com/stride-public-data/burn_data/strd_burn.csv')

# Bot Settings
CHECK_INTERVAL_HOURS = 6
MICRO_STRD_DIVISOR = 1_000_000

# Colors for Discord embeds
COLOR_SUCCESS = 0x28a745  # Green
COLOR_STRD = 0xe50571     # STRD Pink
```

## Step 4: Monitor Your Deployment

1. **Check Logs**:
   - In Railway dashboard, go to your project
   - Click on the deployment
   - View logs to ensure the bot is running correctly

2. **Verify Bot Status**:
   - Check that your Discord bot appears online
   - Verify it shows "Watching STRD burns 🔥" status
   - Look for webhook notifications

## Railway-Specific Features

### Automatic Restarts
Railway will automatically restart your bot if it crashes or fails.

### Environment Variables
Railway provides a secure way to store sensitive data like bot tokens.

### Logging
All bot logs are available in the Railway dashboard.

### Scaling
Railway can automatically scale your bot based on usage.

## Troubleshooting

### Bot Won't Start
1. Check Railway logs for error messages
2. Verify environment variables are set correctly
3. Ensure Discord bot token is valid

### Bot Not Appearing Online
1. Check if the bot has proper permissions
2. Verify the bot token is correct
3. Look for authentication errors in logs

### Webhook Not Working
1. Verify webhook URL is correct
2. Check if webhook has proper permissions
3. Look for webhook errors in logs

### CSV Fetch Errors
1. Verify the CSV URL is accessible
2. Check if the URL format is correct
3. Look for network connectivity issues

## Cost Optimization

Railway offers a free tier with:
- 500 hours per month
- 512MB RAM
- Shared CPU

For 24/7 operation, you'll need a paid plan:
- $5/month for 24/7 uptime
- 1GB RAM
- Dedicated CPU

## Alternative: Railway with Docker

If you prefer Docker deployment, create a `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "strd_burn_monitor.py"]
```

Then use `railway up` to deploy the Docker container.

## Support

- **Railway Docs**: [docs.railway.app](https://docs.railway.app)
- **Discord Bot Issues**: Check the logs in Railway dashboard
- **GitHub Issues**: Open an issue in your repository

---

Your STRD Burn Monitor Bot will now run 24/7 on Railway, automatically monitoring burns and updating its username! 