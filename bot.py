import os
import sys
import logging
import json
from pathlib import Path
import praw
from utils import helpers

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
POST_URL = "https://www.reddit.com/r/China_Dealradar/comments/1mmzgyy/best_emulation_handheld_again_on_sale_for_22/"

# List of subreddits to crosspost to
SUBREDDITS = getattr(settings, 'CROSSPOST_SUBREDDITS', [])

# Number of upvotes to buy for each crosspost
UPVOTES_TO_BUY = getattr(settings, 'CROSSPOST_UPVOTES_TO_BUY', 5)

logger.info(f"Ready to crosspost {POST_URL} to {len(SUBREDDITS)} subreddits.")
logger.info(f"Will buy {UPVOTES_TO_BUY} upvotes for each crosspost.")

# File to track already crossposted subreddits
CROSSPOSTED_FILE = Path(__file__).parent / 'crossposted_subreddits.json'
if CROSSPOSTED_FILE.exists():
    with open(CROSSPOSTED_FILE, 'r') as f:
        crossposted_subreddits = set(json.load(f))
else:
    crossposted_subreddits = set()

def save_crossposted_subreddits(subreddit_name):
    crossposted_subreddits.add(subreddit_name)
    with open(CROSSPOSTED_FILE, 'w') as f:
        json.dump(list(crossposted_subreddits), f)

def crosspost_with_flair(submission, subreddit, subreddit_name):
    # Try to crosspost with flair if required
    try:
        flairs = list(subreddit.flair.link_templates)
        if not flairs:
            logger.error(f"No flairs available for r/{subreddit_name}, cannot crosspost.")
            return None
        flair_id = flairs[0]['id']
        logger.info(f"Using flair id {flair_id} for r/{subreddit_name}")
        cross = submission.crosspost(subreddit=subreddit_name, send_replies=False, flair_id=flair_id)
        return cross
    except Exception as e:
        logger.error(f"Failed to crosspost with flair to r/{subreddit_name}: {e}")
        return None

# Placeholder for crossposting logic
def main():
    logger.info("Starting crossposting bot...")
    if not accounts or not accounts.get('accounts'):
        logger.error("No accounts found in accounts.json.")
        return
    account = accounts['accounts'][0]  # Use the first account for now
    reddit = praw.Reddit(
        client_id=account['client_id'],
        client_secret=account['client_secret'],
        username=account['username'],
        password=account['password'],
        user_agent=account['user_agent']
    )
    logger.info(f"Logged in as {account['username']}")
    # Get the original submission
    try:
        submission = reddit.submission(url=POST_URL)
        logger.info(f"Loaded original post: {submission.title}")
    except Exception as e:
        logger.error(f"Failed to load original post: {e}")
        return
    for subreddit_name in SUBREDDITS:
        if subreddit_name in crossposted_subreddits:
            logger.info(f"Already crossposted to r/{subreddit_name}, skipping.")
            continue
        try:
            # Check if subreddit exists and is public
            try:
                subreddit = reddit.subreddit(subreddit_name)
                if subreddit.subreddit_type == 'private' or subreddit.over18:
                    logger.warning(f"Skipping r/{subreddit_name}: private or NSFW.")
                    continue
                # Try to fetch subreddit display name to confirm existence
                _ = subreddit.display_name
            except Exception as sub_err:
                logger.warning(f"Skipping r/{subreddit_name}: does not exist or inaccessible. Error: {sub_err}")
                continue
            logger.info(f"Crossposting to r/{subreddit_name}")
            try:
                cross = submission.crosspost(subreddit=subreddit_name, send_replies=False)
            except praw.exceptions.APIException as api_exc:
                if api_exc.error_type == 'SUBMIT_VALIDATION_FLAIR_REQUIRED':
                    logger.info(f"Flair required for r/{subreddit_name}, attempting with flair.")
                    cross = crosspost_with_flair(submission, subreddit, subreddit_name)
                    if not cross:
                        continue
                else:
                    logger.error(f"APIException for r/{subreddit_name}: {api_exc}")
                    continue
            cross_url = f"https://www.reddit.com{cross.permalink}"
            logger.info(f"Crossposted to r/{subreddit_name}: {cross_url}")
            save_crossposted_subreddits(subreddit_name)
            # Buy upvotes for the crosspost
            logger.debug(f"Ordering {UPVOTES_TO_BUY} upvotes for {cross_url}")
            upvote_result = helpers.order_post_upvotes(cross_url, UPVOTES_TO_BUY, account)
            logger.info(f"Upvote order result for {cross_url}: {upvote_result}")
        except Exception as e:
            logger.error(f"Error crossposting to r/{subreddit_name}: {e}")
            continue

if __name__ == "__main__":
    main() 