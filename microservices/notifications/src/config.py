import os

from dotenv import load_dotenv

if os.environ.get("ENV") == "DEV":
    load_dotenv()

config = {
    "SENDGRID_API_KEY": os.environ.get("SENDGRID_API_KEY"),
    "SENDGRID_FROM_EMAIL": os.environ.get("SENDGRID_FROM_EMAIL"),
    "SENDGRID_TO_EMAIL": os.environ.get("SENDGRID_TO_EMAIL"),
    "PORT": int(os.environ.get("PORT", 5000)),
    "REDIS_HOST": os.environ.get("REDIS_HOST", "localhost"),
    "REDIS_PORT": int(os.environ.get("REDIS_PORT", 6379)),
    "ENV": os.environ.get("ENV"),
    "EMAIL_COOLDOWN": int(os.environ.get("EMAIL_COOLDOWN", 60)),
}
