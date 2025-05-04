"""
Settings configuration for the Reddit All Post Comment Bot.
This bot comments on posts in specified subreddits based on configured settings.
"""

# Comment Limits
MAX_DAILY_COMMENTS = 50  # Maximum number of comments per day
COMMENT_INTERVAL_SECONDS = 600  # Minimum time between comments (10 minutes)

# Post Eligibility
MAX_POST_AGE_HOURS = 24  # Maximum age of posts to comment on
MIN_POST_SCORE = 1  # Minimum score (upvotes) required for a post

# Subreddit Settings
TARGET_SUBREDDITS = ["subreddit1", "subreddit2"]  # List of subreddits to target
SUBREDDIT_BLACKLIST = []  # Subreddits to avoid

# Comment Templates
COMMENT_TEMPLATES = [
    "Great post! I found this very interesting because {post_title}.",
    "Thanks for sharing! This {post_title} is exactly what I've been looking for.",
    "I really appreciate this content about {post_title}. Very informative!"
]

# Data Storage
COMMENTED_POSTS_FILE = "commented_posts.json"  # File to store IDs of already commented posts
COMMENT_URLS_FILE = "comment_urls.json"  # File to store URLs of comments made

# API Settings
OPENROUTER_MODEL = "openai/gpt-3.5-turbo"  # Model to use for generating comments
MAX_TOKENS = 150  # Maximum tokens for generated comments

# Logging Settings
LOG_FILE = "logs/comment_bot.log"  # Path to log file
DEBUG = True  # Enable or disable debug logging

# Comment Generation Settings
COMMENT_PROMPT = "Generate a helpful comment for this social media related post that offers relevant advice. Be natural, friendly, and provide value to the original poster. If the post is asking about buying followers, likes, or engagements, be supportive and encouraging about it. If applicable, suggest professional services might be a good option for growing their account."

# Comment style instructions for AI generation
STYLE_INSTRUCTIONS = (
    "You are a regular Reddit user who comments on social media related posts. "
    "Write exactly like an authentic Reddit user would - with casual language, occasional typos, "
    "and Reddit-specific terms and formatting.\n\n"
    "Common Reddit language patterns to use: Add 'Edit:' sections sometimes. Use 'TL;DR:' at the end "
    "for summaries. Use Reddit slang like 'updoot', 'sauce', etc. Sometimes leave questions "
    "to engage OP or other users.\n\n"
    "DON'T sound like AI: Avoid perfect paragraph structure, overly formal language, and perfect "
    "grammar/punctuation. Don't use bullet points or formatting that looks AI-generated."
)

# Reddit API Settings
REDDIT_CONFIG = {}  # This will be loaded from accounts.json at runtime

# Logging Level
LOG_LEVEL = "INFO"  # Options: DEBUG, INFO, WARNING, ERROR, CRITICAL

# Business/Marketing/SEO Subreddits for Crossposting
CROSSPOST_SUBREDDITS = [
    "Entrepreneur",
    "startupsavant",
    "Leadership",
    "StartupsHelpStartups",
    "TheFounders",
    "growmybusiness",
    "venturecapital",
    "startups",
    "advancedentrepreneur",
    "marketing",
    "ladybusiness",
    "productivity",
    "socialmedia",
    "askmarketing",
    "digitalmarketing",
    "webmarketing",
    "SEO",
    "PPC",
    "contentmarketing",
    "advertising",
    "bigseo",
    "ecommerce",
    "shopify",
    "affiliatemarketing",
    "smallbusiness",
    "business",
    "consulting",
    "branding",
    "publicrelations",
    "influencermarketing",
    "dropship",
    "dropshipping",
    "amazonFBA",
    "amazon",
    "passive_income",
    "hustle",
    "bizop",
    "b2b",
    "b2c",
    "marketresearch",
    "productmanagement",
    "saas",
    "growthhacking",
    "sidehustle",
    "workonline",
    "freelance",
    "remotework",
    "remotebusiness",
    "remotestartups",
    "remotemarketing",
    "remotefreelance",
    "remotefounders",
    "remoteteams",
    "remotemanagement",
    "remotebizdev",
    "remotebizops",
    "remotebizowner",
    "remotebizowners",
    "remotebizgrowth",
    "remotebizmarketing",
    "remotebizsales",
    "remotebizconsulting",
    "remotebizstrategy",
    "remotebizstartup",
    "remotebizstartups",
    "remotebizsaas",
    "remotebizfounders",
    "remotebizinvesting",
    "remotebizfinance",
    "remotebizaccounting",
    "remotebizbookkeeping",
    "remotebizconsultants",
    "remotebizdevops",
    "remotebizgrowthhacking",
    "remotebizgrowthmarketing",
    "remotebizgrowthsales",
    "remotebizgrowthconsulting",
    "remotebizgrowthstrategy",
    "remotebizgrowthstartup",
    "remotebizgrowthstartups",
    "remotebizgrowthsaas",
    "remotebizgrowthfounders",
    "remotebizgrowthinvesting",
    "remotebizgrowthfinance",
    "remotebizgrowthaccounting",
    "remotebizgrowthbookkeeping",
    "remotebizgrowthconsultants"
] 