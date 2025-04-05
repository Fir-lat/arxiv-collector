import os

class Config:
    DEEPSEEK_API_KEY = "<Place Your API Key Here>"
    BASE_PATH = os.path.expanduser("../arxiv_collection") # Where your arxiv-collection is going to be
    CATEGORIES = ["cs.AI", "cs.CV", "cs.LG"]
    TARGET_TOPICS = [
        "multi-modal understanding/generation",
        "unified model",
        "any-to-any generation",
        "embodied AI"
    ]
    
    # 数据库路径（用于记录已处理论文）
    DB_PATH = os.path.join(BASE_PATH, "processed_papers.db")

if __name__ == '__main__':
    config = Config()
    os.makedirs(config.BASE_PATH, exist_ok=True)
    print(config.BASE_PATH)