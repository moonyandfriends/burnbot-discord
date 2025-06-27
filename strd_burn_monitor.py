"""
STRD Burn Monitor Discord Bot

A simple Discord bot that monitors STRD token burns from the Stride blockchain
and updates its username with the current total burned amount.

Author: STRD Burn Monitor Team
License: MIT
"""

import discord
from discord.ext import tasks
import aiohttp
import logging
from datetime import datetime
import hashlib
import re
from typing import Optional, Tuple

# Import configuration
from config import (
    burnbot_discord_token,
    burnbot_logs_webhookurl,
    burnbot_csv_url,
    CHECK_INTERVAL_HOURS,
    MICRO_STRD_DIVISOR,
    COLOR_SUCCESS,
    COLOR_STRD
)

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('strd_bot.log'),
        logging.StreamHandler()
    ]
)
logger: logging.Logger = logging.getLogger(__name__)


class STRDBurnMonitor(discord.Client):
    """
    Simple Discord bot for monitoring STRD token burns.
    
    This bot fetches burn data from a CSV file and updates its username
    with the current total burned amount. No commands, just monitoring.
    """
    
    def __init__(self) -> None:
        """
        Initialize the STRD Burn Monitor bot.
        
        Sets up Discord intents and initial state.
        """
        intents = discord.Intents.default()
        intents.guilds = True
        super().__init__(intents=intents)
        
        # Bot state
        self.last_csv_hash: Optional[str] = None
        self.last_total_burned: float = 0.0
        self.last_check_time: Optional[str] = None
        
    async def setup_hook(self) -> None:
        """
        Called when the bot is starting up.
        
        Starts the CSV monitoring task.
        """
        # Start the monitoring task
        self.csv_monitor.start()
        logger.info(f"CSV monitoring task started - checking every {CHECK_INTERVAL_HOURS} hours")

    async def on_ready(self) -> None:
        """
        Called when bot is ready and connected to Discord.
        
        Sets bot status, sends webhook notification, initializes state,
        and performs initial CSV check.
        """
        logger.info(f'Bot logged in as {self.user}')
        
        # Set bot status to online and watching STRD burns
        await self.change_presence(
            status=discord.Status.online,
            activity=discord.Activity(type=discord.ActivityType.watching, name="STRD burns 🔥")
        )
        
        # Send webhook notification that bot is online
        await self.send_webhook_notification("🟢 **STRD Burn Monitor Online**", 
                                            f"Bot `{self.user}` is now monitoring STRD burns", 
                                            color=COLOR_SUCCESS)
        
        # Get initial state from current username if possible
        await self.initialize_from_username()
        
        # Perform initial check
        await self.check_csv_update()

    async def initialize_from_username(self) -> None:
        """
        Initialize bot state from current username if available.
        
        Attempts to extract the current burn total from the bot's
        display name (e.g., "401,613 STRD Burned 🔥").
        """
        try:
            # Try to extract number from current username like "401,613 STRD Burned 🔥"
            if self.user and self.user.display_name:
                match = re.search(r'([\d,]+)\s+STRD', self.user.display_name)
                if match:
                    # Remove commas and convert to float
                    self.last_total_burned = float(match.group(1).replace(',', ''))
                    logger.info(f"Initialized from current username: {self.last_total_burned:,.0f} STRD")
        except Exception as e:
            logger.warning(f"Could not initialize from username: {e}")

    async def send_webhook_notification(self, title: str, description: str, color: int = COLOR_STRD) -> None:
        """
        Send notification to webhook if configured.
        
        Args:
            title: The title of the notification embed
            description: The description text for the notification
            color: The color of the embed (default: STRD pink)
        """
        if not burnbot_logs_webhookurl or burnbot_logs_webhookurl == "YOUR_WEBHOOK_URL_HERE":
            return
            
        try:
            async with aiohttp.ClientSession() as session:
                embed = {
                    "title": title,
                    "description": description,
                    "color": color,
                    "timestamp": datetime.now().isoformat(),
                    "footer": {
                        "text": "STRD Burn Monitor"
                    }
                }
                
                payload = {
                    "embeds": [embed]
                }
                
                async with session.post(burnbot_logs_webhookurl, json=payload) as response:
                    if response.status == 204:
                        logger.info("Webhook notification sent successfully")
                    else:
                        logger.warning(f"Webhook failed with status {response.status}")
                        
        except Exception as e:
            logger.error(f"Error sending webhook notification: {e}")

    async def fetch_csv_data(self) -> Tuple[Optional[str], Optional[float]]:
        """
        Fetch and parse the latest CSV data.
        
        Returns:
            Tuple of (csv_hash, total_burned_strd) or (None, None) if failed
        """
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(burnbot_csv_url) as response:
                    if response.status != 200:
                        logger.error(f"Failed to fetch CSV: HTTP {response.status}")
                        return None, None
                    
                    csv_content = await response.text()
                    
                    # Calculate hash of CSV content to detect changes
                    csv_hash = hashlib.md5(csv_content.encode()).hexdigest()
                    
                    # Parse the last line to get the latest total
                    lines = csv_content.strip().split('\n')
                    if not lines:
                        logger.error("CSV file is empty")
                        return csv_hash, None
                    
                    # Get the last valid line
                    latest_total_micro_strd = None
                    for line in reversed(lines):
                        line = line.strip()
                        if not line:
                            continue
                        
                        parts = line.split(',')
                        if len(parts) >= 2:
                            try:
                                latest_total_micro_strd = int(parts[1])
                                break
                            except ValueError:
                                continue
                    
                    if latest_total_micro_strd is None:
                        logger.error("Could not parse latest burn amount from CSV")
                        return csv_hash, None
                    
                    # Convert microSTRD to STRD
                    latest_total_strd = latest_total_micro_strd / MICRO_STRD_DIVISOR
                    
                    logger.info(f"Latest total burned: {latest_total_strd:,.6f} STRD")
                    return csv_hash, latest_total_strd
                    
        except Exception as e:
            logger.error(f"Error fetching CSV data: {e}")
            return None, None

    async def update_bot_username(self, total_burned: float) -> bool:
        """
        Update the bot's username with the current burn amount.
        
        Args:
            total_burned: The total amount of STRD burned
            
        Returns:
            True if update was successful, False otherwise
        """
        try:
            # Format the username with comma separators
            username = f"{total_burned:,.0f} STRD Burned 🔥"
            
            try:
                if self.user:
                    await self.user.edit(username=username)
                    logger.info(f"Updated username to: {username}")
                    
                    # Send webhook notification about the update
                    await self.send_webhook_notification(
                        "🔥 **STRD Burn Update**",
                        f"Total burned: **{total_burned:,.0f} STRD**\nBot username updated to: `{username}`",
                        color=COLOR_STRD
                    )
                    
                    return True
                else:
                    logger.error("Bot user is None")
                    return False
            except discord.Forbidden:
                logger.error("No permission to change username")
                return False
            except discord.HTTPException as e:
                if "rate limited" in str(e).lower():
                    logger.warning("Username change rate limited - Discord only allows 2 changes per hour")
                else:
                    logger.error(f"Error updating username: {e}")
                return False
            except Exception as e:
                logger.error(f"Error updating username: {e}")
                return False
                
        except Exception as e:
            logger.error(f"Error in update_bot_username: {e}")
            return False

    async def check_csv_update(self) -> None:
        """
        Check if CSV has been updated and update bot if necessary.
        
        Fetches the latest CSV data, compares it with the current state,
        and updates the bot's username if the burn total has changed.
        """
        try:
            logger.info("Checking for CSV updates...")
            
            csv_hash, total_burned = await self.fetch_csv_data()
            
            if csv_hash is None or total_burned is None:
                logger.warning("Failed to fetch CSV data, skipping update")
                return
            
            # Check if the total has actually changed (more reliable than hash)
            if abs(total_burned - self.last_total_burned) > 0.000001:  # Account for floating point precision
                logger.info(f"Burn total changed from {self.last_total_burned:,.6f} to {total_burned:,.6f} STRD")
                
                # Update bot username
                success = await self.update_bot_username(total_burned)
                
                if success:
                    # Update in-memory state
                    self.last_csv_hash = csv_hash
                    self.last_total_burned = total_burned
                    self.last_check_time = datetime.now().isoformat()
                    
                    logger.info(f"Bot updated successfully with {total_burned:,.6f} STRD burned")
                else:
                    logger.error("Failed to update bot username")
            else:
                logger.info("No changes in burn total detected")
                # Still update hash and check time
                self.last_csv_hash = csv_hash
                self.last_check_time = datetime.now().isoformat()
                
        except Exception as e:
            logger.error(f"Error checking CSV update: {e}")

    @tasks.loop(hours=CHECK_INTERVAL_HOURS)
    async def csv_monitor(self) -> None:
        """
        Check for CSV updates every configured hours.
        
        This is a background task that runs automatically.
        """
        await self.check_csv_update()

    @csv_monitor.before_loop
    async def before_csv_monitor(self) -> None:
        """
        Wait until bot is ready before starting the loop.
        """
        await self.wait_until_ready()


def main() -> None:
    """
    Main entry point for the STRD Burn Monitor bot.
    
    Validates configuration, creates bot instance, and runs the bot indefinitely.
    """
    try:
        # Validate configuration
        if burnbot_discord_token == "YOUR_DISCORD_BOT_TOKEN_HERE":
            logger.error("Please update burnbot_discord_token variable in config.py with your actual bot token")
            print("Please update the burnbot_discord_token variable in config.py with your actual bot token.")
            return
            
        logger.info("Starting STRD Burn Monitor bot...")
        
        bot = STRDBurnMonitor()
        
        # Keep bot online and run indefinitely
        bot.run(burnbot_discord_token)
        
    except Exception as e:
        logger.error(f"Failed to start bot: {e}")
        print("Bot failed to start. Check the logs for details.")


if __name__ == "__main__":
    main() 