import os
import requests
from urllib.parse import unquote
import datetime
from config import Config
import re

def sanitize_title(title):
    # Replace non-alphanumeric/underscore characters with underscores
    return re.sub(r'[^a-zA-Z0-9_]', '_', title)

class PDFDownloader:
    @staticmethod
    def download(papers):
        for paper in papers:
            # construct the save directory
            category = "General"
            if paper.get('category', None):
                category = paper['category']

            # transform uppercase to lowercase
            category = category.lower()
            
            date_str = paper['published'].isoformat()
            os.makedirs(Config.BASE_PATH, exist_ok=True)
            save_dir = os.path.join(
                Config.BASE_PATH,
                category,
                date_str,
            )
            os.makedirs(save_dir, exist_ok=True)
            
            # download the PDF
            response = requests.get(paper['pdf_url'])
            # replace all characters of tile that are not alphanumeric or underscore with underscore
            paper_title = sanitize_title(paper['title'])
            filename = f"{paper['id']}_{paper_title[:min(len(paper_title), 100)]}.pdf"
            with open(os.path.join(save_dir, filename), 'wb') as f:
                f.write(response.content)
            
            paper['local_path'] = os.path.join(save_dir, filename)


if __name__ == '__main__':
    pdf_downloader = PDFDownloader()
    
    filtered_papers = [
        {
            "id": "2501.16718v1",
            "title": "HamOS: Outlier Synthesis via Hamiltonian Monte Carlo for Out-of-Distribution Detection",
            "pdf_url": "https://arxiv.org/pdf/2501.16718v1",
            "published": datetime.date.today(),
            "category": "Machine Learning"
        }
    ]
    
    pdf_downloader.download(filtered_papers)

    print(filtered_papers)
    