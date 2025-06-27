"""
Configuration settings for the STRD Burn Monitor Discord Bot.

This module contains all configuration variables that need to be updated
before running the bot. Supports both local configuration and Railway environment variables.
"""

import os

# Discord Bot Configuration
burnbot_discord_token = os.getenv("burnbot_discord_token", "YOUR_DISCORD_BOT_TOKEN_HERE")
burnbot_logs_webhookurl = os.getenv("burnbot_logs_webhookurl", "YOUR_WEBHOOK_URL_HERE")  # Optional: Discord webhook for notifications

# Data Source Configuration
burnbot_csv_url = os.getenv("burnbot_csv_url", 'https://storage.googleapis.com/stride-public-data/burn_data/strd_burn.csv')

# Bot Settings
CHECK_INTERVAL_HOURS = 6
MICRO_STRD_DIVISOR = 1_000_000  # Convert microSTRD to STRD

# Colors for Discord embeds
COLOR_SUCCESS = 0x28a745  # Green
COLOR_STRD = 0xe50571     # STRD Pink 