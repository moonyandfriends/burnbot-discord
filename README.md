# STRD Burn Monitor Discord Bot

A simple Discord bot that monitors STRD token burns from the Stride blockchain and automatically updates its username with the current total burned amount.

## Features

- 🔥 **Real-time Monitoring**: Fetches burn data from Stride's public CSV every 6 hours
- 🤖 **Dynamic Username**: Updates bot username with current burn total (e.g., "401,613 STRD Burned 🔥")
- 🔔 **Webhook Notifications**: Optional Discord webhook notifications for updates
- ⚡ **Automatic Updates**: Background task runs every 6 hours to check for new burns
- 🛡️ **Error Handling**: Robust error handling and logging
- 📱 **Always Online**: Bot appears online 24/7 with "Watching STRD burns 🔥" status
- ☁️ **Railway Ready**: Pre-configured for easy deployment on Railway

## Prerequisites

- Python 3.8 or higher
- Discord Bot Token
- Optional: Discord Webhook URL for notifications

## Quick Deploy to Railway

The easiest way to run this bot 24/7 is using Railway:

1. **Fork this repository** to your GitHub account
2. **Sign up** at [railway.app](https://railway.app)
3. **Create new project** → "Deploy from GitHub repo"
4. **Set environment variables**:
   - `burnbot_discord_token` = your Discord bot token
   - `burnbot_logs_webhookurl` = your Discord webhook URL (optional)
   - `burnbot_csv_url` = CSV data source URL (optional, has default)
5. **Deploy** - Railway will automatically build and run your bot!

For detailed Railway deployment instructions, see [railway-deploy.md](railway-deploy.md).

## Local Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/burnbot-discord.git
   cd burnbot-discord
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure the bot:**
   - Edit `config.py` and update the following variables:
     - `burnbot_discord_token`: Your Discord bot token
     - `burnbot_logs_webhookurl`: Optional webhook URL for notifications
     - `burnbot_csv_url`: Optional CSV data source URL

4. **Run the bot:**
   ```bash
   python strd_burn_monitor.py
   ```

## Configuration

### Required Configuration

Update the following variables in `config.py`:

```python
burnbot_discord_token = "your_discord_bot_token_here"
```

### Optional Configuration

```python
burnbot_logs_webhookurl = "your_discord_webhook_url_here"  # For notifications
burnbot_csv_url = "your_csv_data_source_url"  # Default: Stride's public CSV
```

### Bot Settings

You can customize these settings in `config.py`:

- `CHECK_INTERVAL_HOURS`: How often to check for updates (default: 6 hours)
- `burnbot_csv_url`: Data source URL (default: Stride's public CSV)

## How It Works

The bot operates silently in the background:

1. **Startup**: Bot connects to Discord, sets status to "Watching STRD burns 🔥", and sends webhook notification
2. **Monitoring**: Every 6 hours, the bot fetches the latest CSV data from Stride
3. **Updates**: If the burn total has changed, the bot updates its username and sends a webhook notification
4. **Logging**: All activities are logged to `strd_bot.log`

## Data Source

The bot fetches burn data from Stride's public CSV file:
- **URL**: `https://storage.googleapis.com/stride-public-data/burn_data/strd_burn.csv`
- **Format**: CSV with timestamp and microSTRD amounts
- **Update Frequency**: Every 6 hours automatically

## Features in Detail

### Automatic Username Updates

The bot automatically updates its username to reflect the current total STRD burned:
- Format: `{total_burned:,.0f} STRD Burned 🔥`
- Example: `401,613 STRD Burned 🔥`
- Rate limiting: Discord allows only 2 username changes per hour

### Webhook Notifications

If configured, the bot sends Discord webhook notifications for:
- Bot startup (green notification)
- Username updates (pink notification with burn details)

### Always Online Status

The bot maintains an "Online" status with the activity "Watching STRD burns 🔥" to show it's actively monitoring.

## Logging

The bot creates detailed logs in `strd_bot.log` including:
- Bot startup/shutdown events
- CSV fetch attempts and results
- Username update attempts
- Error conditions and stack traces

## Development

### Project Structure

```
burnbot-discord/
├── strd_burn_monitor.py  # Main bot script
├── config.py             # Configuration settings
├── requirements.txt      # Python dependencies
├── README.md            # This file
├── test_bot.py          # Test script
├── railway-deploy.md    # Railway deployment guide
├── Procfile             # Railway process file
├── runtime.txt          # Python version for Railway
├── railway.json         # Railway configuration
├── Dockerfile           # Docker deployment
├── .dockerignore        # Docker ignore rules
└── .gitignore           # Git ignore rules
```

### Testing

Run the test script to verify functionality:

```bash
python test_bot.py
```

This will test CSV fetching without requiring Discord connection.

## Deployment Options

### Railway (Recommended)
- **Easy setup**: One-click deployment from GitHub
- **24/7 uptime**: $5/month for continuous operation
- **Automatic restarts**: Self-healing if bot crashes
- **Environment variables**: Secure token storage

### Docker
- **Portable**: Run anywhere Docker is supported
- **Consistent**: Same environment across deployments
- **Scalable**: Easy to scale horizontally

### Local Server
- **Full control**: Complete control over the environment
- **Cost effective**: No cloud hosting fees
- **Requires maintenance**: Manual updates and monitoring

## Troubleshooting

### Common Issues

1. **Bot won't start**: Check that `burnbot_discord_token` is set correctly
2. **Username not updating**: Verify bot has permission to change username
3. **Rate limiting**: Discord limits username changes to 2 per hour
4. **CSV fetch errors**: Check network connectivity and CSV URL accessibility

### Logs

Check `strd_bot.log` for detailed error information and debugging.

## Bot Permissions

Your Discord bot needs these permissions:
- **Send Messages** (for webhook notifications)
- **Change Nickname** (for username updates)
- **Use Slash Commands** (not used but recommended)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, please open an issue on GitHub or contact the development team.

---

**Note**: This bot is designed to run continuously and will automatically restart if it encounters errors. Railway deployment is recommended for 24/7 operation.