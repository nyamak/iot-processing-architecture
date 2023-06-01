import os

from dotenv import load_dotenv

if os.environ.get("ENV") == "DEV":
    load_dotenv()

config = {
    "PORT": int(os.environ.get("PORT", 5000)),
    "SENDGRID_API_KEY": os.environ.get("SENDGRID_API_KEY"),
    "SENDGRID_FROM_EMAIL": os.environ.get("SENDGRID_FROM_EMAIL"),
    "SENDGRID_TO_EMAIL": os.environ.get("SENDGRID_TO_EMAIL"),
    "REDIS_HOST": os.environ.get("REDIS_HOST"),
    "REDIS_PORT": os.environ.get("REDIS_PORT"),
}
