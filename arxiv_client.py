import arxiv
from datetime import datetime, timedelta
import sqlite3
from config import Config

class ArxivClient:
    def __init__(self):
        self.client = arxiv.Client()
        self.conn = sqlite3.connect(Config.DB_PATH)
        self._init_db()
        self.paper_limit = Config.PAPER_LIMIT

    def _init_db(self):
        """Initialize the SQLite database."""

        self.conn.execute('''CREATE TABLE IF NOT EXISTS processed 
                          (id TEXT PRIMARY KEY, title TEXT)''')

    def get_new_papers(self):
        """get new papers from arXiv."""
        # construct the search query
        query = " OR ".join([f"cat:{cat}" for cat in Config.CATEGORIES])
        
        # get the newest papers
        search = arxiv.Search(
            query=query,
            max_results=self.paper_limit,
            sort_by=arxiv.SortCriterion.SubmittedDate
        )
        
        # filter out already processed papers
        cursor = self.conn.cursor()
        new_papers = []
        for result in self.client.results(search):
            if not cursor.execute("SELECT 1 FROM processed WHERE id=?", 
                                (result.get_short_id()[:-2],)).fetchone():
                new_papers.append({
                    "id": result.get_short_id(),
                    "title": result.title,
                    "abstract": result.summary,
                    "comments": result.comment,
                    "pdf_url": result.pdf_url,
                    "published": result.published.date()
                })
        print(f"Found {len(new_papers)} new papers.")
        
        return new_papers
    

if __name__ == '__main__':
    client = ArxivClient()
    new_papers = client.get_new_papers()
    for paper in new_papers:
        print(f"Title: {paper['title']}")
        print(f"ID: {paper['id']}")
        print(f"Published: {paper['published']}")
        print(f"Comments: {paper['comments']}")
        # print(f"Abstract: {paper['abstract']}")
        print(f"PDF URL: {paper['pdf_url']}")
        print("-" * 80)
        cursor = client.conn.cursor()
        cursor.execute("INSERT INTO processed (id, title) VALUES (?, ?)", 
                       (paper['id'], paper['title']))
        client.conn.commit()
    # print the items in the database
    cursor = client.conn.cursor()
    cursor.execute("SELECT * FROM processed")
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    # delete all items in the database
    cursor.execute("DELETE FROM processed")
    client.conn.commit()
    # close the connection
    client.conn.close()
    
    
        
        