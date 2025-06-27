"""
Test script for STRD Burn Monitor Discord Bot.

This script tests the core functionality without requiring Discord connection.
"""

import asyncio
import aiohttp
import hashlib
import logging
from typing import Optional, Tuple

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration
CSV_URL = 'https://storage.googleapis.com/stride-public-data/burn_data/strd_burn.csv'
MICRO_STRD_DIVISOR = 1_000_000


async def fetch_csv_data() -> Tuple[Optional[str], Optional[float]]:
    """
    Fetch and parse the latest CSV data.
    
    Returns:
        Tuple of (csv_hash, total_burned_strd) or (None, None) if failed
    """
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(CSV_URL) as response:
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


async def test_csv_fetching():
    """Test CSV fetching functionality."""
    print("🧪 Testing CSV fetching...")
    
    csv_hash, total_burned = await fetch_csv_data()
    
    if csv_hash and total_burned:
        print(f"✅ Successfully fetched CSV data")
        print(f"   CSV Hash: {csv_hash}")
        print(f"   Total Burned: {total_burned:,.6f} STRD")
        
        # Test username formatting
        username = f"{total_burned:,.0f} STRD Burned 🔥"
        print(f"   Username format: {username}")
        
        return True
    else:
        print("❌ Failed to fetch CSV data")
        return False


async def test_multiple_fetches():
    """Test multiple CSV fetches to ensure consistency."""
    print("\n🔄 Testing multiple CSV fetches...")
    
    results = []
    for i in range(3):
        print(f"   Fetch {i+1}/3...")
        csv_hash, total_burned = await fetch_csv_data()
        if csv_hash and total_burned:
            results.append((csv_hash, total_burned))
        await asyncio.sleep(1)  # Small delay between requests
    
    if len(results) == 3:
        # Check if all results are the same
        hashes = [r[0] for r in results]
        totals = [r[1] for r in results]
        
        if len(set(hashes)) == 1 and len(set(totals)) == 1:
            print("✅ All fetches returned consistent data")
            return True
        else:
            print("⚠️  Inconsistent data across fetches")
            return False
    else:
        print("❌ Some fetches failed")
        return False


def main():
    """Main test function."""
    print("🚀 STRD Burn Monitor Bot - Test Suite")
    print("=" * 50)
    
    # Run tests
    success1 = asyncio.run(test_csv_fetching())
    success2 = asyncio.run(test_multiple_fetches())
    
    print("\n" + "=" * 50)
    if success1 and success2:
        print("✅ All tests passed!")
        print("\n📋 The bot should work correctly when configured with:")
        print("   - Valid Discord bot token")
        print("   - Proper bot permissions")
        print("   - Network connectivity")
    else:
        print("❌ Some tests failed")
        print("\n🔧 Troubleshooting:")
        print("   - Check internet connectivity")
        print("   - Verify CSV URL is accessible")
        print("   - Check firewall settings")


if __name__ == "__main__":
    main() 