import os
import sys
import logging
import json
from pathlib import Path

# Add config and utils to path
sys.path.append(str(Path(__file__).parent / 'config'))
sys.path.append(str(Path(__file__).parent / 'utils'))

from config import settings

# Logging setup
log_dir = Path(__file__).parent / 'logs'
log_dir.mkdir(exist_ok=True)
logging.basicConfig(
    filename=log_dir / 'crosspost_bot.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s'
)
logger = logging.getLogger(__name__)

# Load accounts/credentials
accounts_path = Path(__file__).parent / 'config' / 'accounts.json'
if not accounts_path.exists():
    logger.error(f"accounts.json not found at {accounts_path}")
    sys.exit(1)

with open(accounts_path, 'r') as f:
    accounts = json.load(f)

logger.info(f"Loaded {len(accounts)} accounts.")

# Hardcoded Reddit post URL to crosspost
POST_URL = "https://www.reddit.com/r/Entrepreneur/comments/xxxxxx/example_post_title/"

# List of subreddits to crosspost to
SUBREDDITS = getattr(settings, 'CROSSPOST_SUBREDDITS', [])

logger.info(f"Ready to crosspost {POST_URL} to {len(SUBREDDITS)} subreddits.")

# Placeholder for crossposting logic
def main():
    logger.info("Bot initialized. Crossposting logic not yet implemented.")

if __name__ == "__main__":
    main() 