import os
from dotenv import load_dotenv

load_dotenv()  # load environment variables from .env file

class Config:
    API_KEY = os.getenv("API_KEY")
    BASE_URL = "https://api.deepseek.com"
    BASE_PATH = os.path.expanduser("../arxiv_collection") # Where your arxiv-collection is going to be
    CATEGORIES = ["cs.AI", "cs.CV", "cs.LG"]
    TARGET_TOPICS = [
        "multi-modal understanding and generation",
        "unified model",
        "any-to-any generation",
        "embodied AI"
    ]
    PAPER_LIMIT = 200  # Number of papers to fetch from arXiv
    
    MAX_STORAGE_GB = 10         # max storage size in GB
    AUTO_CLEAN_DAYS = 60         # automatic clean up days
    CLEANUP_THRESHOLD = 0.9
    
    # database
    DB_PATH = os.path.join(BASE_PATH, "processed_papers.db")

if __name__ == '__main__':
    os.makedirs(Config.BASE_PATH, exist_ok=True)
    print(Config.API_KEY)