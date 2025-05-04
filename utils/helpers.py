import json
import os
import logging
import random
import sys
from openai import OpenAI
import time
from typing import Dict, List, Optional

import praw
import prawcore

# Configure logging
logger = logging.getLogger(__name__)

def load_commented_posts(file_path):
    """Load previously commented posts from file"""
    if os.path.exists(file_path):
        try:
            with open(file_path, 'r') as f:
                return set(json.load(f))
        except Exception as e:
            logger.error(f"Error loading commented posts: {e}")
    return set()

def save_commented_posts(file_path, post_id):
    """Save post ID to commented posts file"""
    try:
        # Load existing posts
        commented_posts = load_commented_posts(file_path)
        
        # Add new post ID
        commented_posts.add(post_id)
        
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        # Save to file
        with open(file_path, 'w') as f:
            json.dump(list(commented_posts), f)
    except Exception as e:
        logger.error(f"Error saving commented post: {e}")

def save_comment_url(file_path, comment_url):
    """Save comment URL to file"""
    try:
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        # Load existing URLs
        urls = []
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r') as f:
                    urls = json.load(f)
            except:
                urls = []
        
        # Add new URL
        if comment_url not in urls:
            urls.append(comment_url)
        
        # Save to file
        with open(file_path, 'w') as f:
            json.dump(urls, f)
    except Exception as e:
        logger.error(f"Error saving comment URL: {e}")

def generate_comment(post_title, post_text, api_config, prompt, style_instructions):
    """Generate a comment using OpenRouter API"""
    try:
        logger.debug(f"Generating comment for post: {post_title}")
        
        # Combine title and text for context
        post_content = f"Title: {post_title}\n\nContent: {post_text if post_text else '(No post text)'}"
        
        # Format user prompt with post content
        user_prompt = f"{prompt}\n\nPost: {post_content}"
        logger.debug(f"Using prompt: {user_prompt[:100]}...")
        
        # Initialize OpenAI client with OpenRouter
        client = OpenAI(
            base_url=api_config['openrouter_base_url'],
            api_key=api_config['openrouter_api_key'],
            default_headers={
                "HTTP-Referer": "https://github.com/",
                "X-Title": "Reddit Comment Bot"
            }
        )
        
        # Make request to API
        completion = client.chat.completions.create(
            model="anthropic/claude-3-haiku",  # Using Claude as it's good for natural text
            messages=[
                {"role": "system", "content": style_instructions},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.8,  # Higher temperature for more creative responses
            max_tokens=800  # Limit token usage for comments
        )
        
        if completion and completion.choices and len(completion.choices) > 0:
            comment_text = completion.choices[0].message.content.strip()
            logger.debug(f"Generated comment: {comment_text[:100]}...")
            return comment_text
        else:
            logger.error("No completion generated")
            return None
            
    except Exception as e:
        logger.error(f"OpenRouter API error: {e}", exc_info=True)
        return None 

def load_accounts(accounts_file: str) -> List[Dict]:
    """
    Load Reddit accounts from the accounts file.
    
    Args:
        accounts_file: Path to the accounts JSON file
        
    Returns:
        List of account dictionaries
    """
    if not os.path.exists(accounts_file):
        logger.error(f"Accounts file not found: {accounts_file}")
        return []
    
    try:
        with open(accounts_file, 'r') as f:
            accounts = json.load(f)
        return accounts
    except Exception as e:
        logger.error(f"Error loading accounts: {e}")
        return []

def select_account(accounts: List[Dict]) -> Optional[Dict]:
    """
    Select a random account from the list.
    
    Args:
        accounts: List of account dictionaries
        
    Returns:
        Selected account dictionary or None if no accounts
    """
    if not accounts:
        logger.error("No accounts available")
        return None
    
    return random.choice(accounts)

def get_reddit_instance(account: Dict) -> Optional[praw.Reddit]:
    """
    Create a Reddit instance with the given account.
    
    Args:
        account: Account dictionary with credentials
        
    Returns:
        PRAW Reddit instance or None if creation failed
    """
    try:
        reddit = praw.Reddit(
            client_id=account['client_id'],
            client_secret=account['client_secret'],
            user_agent=account.get('user_agent', f"python:reddit-all-post-bot:v1.0 (by /u/{account['username']})"),
            username=account['username'],
            password=account['password']
        )
        logger.info(f"Logged in as {account['username']}")
        return reddit
    except Exception as e:
        logger.error(f"Error creating Reddit instance: {e}")
        return None

def is_post_too_old(submission, max_age_hours: int) -> bool:
    """
    Check if a submission is older than the maximum age.
    
    Args:
        submission: PRAW submission object
        max_age_hours: Maximum age in hours
        
    Returns:
        True if the post is too old, False otherwise
    """
    post_age = time.time() - submission.created_utc
    max_age_seconds = max_age_hours * 3600
    
    if post_age > max_age_seconds:
        logger.debug(f"Post is too old: {submission.title}")
        return True
    return False

def is_subreddit_blacklisted(subreddit_name: str, blacklist: List[str]) -> bool:
    """
    Check if a subreddit is in the blacklist.
    
    Args:
        subreddit_name: Name of the subreddit
        blacklist: List of blacklisted subreddit names
        
    Returns:
        True if the subreddit is blacklisted, False otherwise
    """
    return subreddit_name.lower() in [s.lower() for s in blacklist]

def generate_comment(template: str, **kwargs) -> str:
    """
    Generate a comment from a template.
    
    Args:
        template: Comment template
        **kwargs: Template variables
        
    Returns:
        Formatted comment
    """
    try:
        return template.format(**kwargs)
    except KeyError as e:
        logger.error(f"Missing template variable: {e}")
        return template

def post_comment(submission, comment_text: str) -> bool:
    """
    Post a comment on a submission.
    
    Args:
        submission: PRAW submission object
        comment_text: Text of the comment
        
    Returns:
        True if comment was posted, False otherwise
    """
    try:
        comment = submission.reply(comment_text)
        logger.info(f"Posted comment on: {submission.title}")
        return True
    except prawcore.exceptions.Forbidden:
        logger.error(f"Forbidden to comment in r/{submission.subreddit.display_name}")
        return False
    except prawcore.exceptions.ServerError:
        logger.error("Reddit server error. Waiting before retry.")
        time.sleep(60)  # Wait a minute before retrying
        return False
    except Exception as e:
        logger.error(f"Error posting comment: {e}")
        return False

def has_already_commented(reddit, submission) -> bool:
    """
    Check if the bot has already commented on a submission.
    
    Args:
        reddit: PRAW Reddit instance
        submission: PRAW submission object
        
    Returns:
        True if already commented, False otherwise
    """
    try:
        for comment in submission.comments.list():
            if hasattr(comment, 'author') and comment.author and comment.author == reddit.user.me():
                logger.debug(f"Already commented on: {submission.title}")
                return True
        return False
    except Exception as e:
        logger.error(f"Error checking if already commented: {e}")
        return True  # Assume already commented to be safe 