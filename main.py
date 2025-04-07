import logging
import os
import datetime
from arxiv_client import ArxivClient
from paper_filter import PaperFilter
from pdf_downloader import PDFDownloader
from paper_analyzer import PaperAnalyzer
from report_generator import ReportGenerator
from pdf_cleaner import PDFCacheCleaner

log_dir = ".log"
os.makedirs(log_dir, exist_ok=True)

# Configure logging
logging.basicConfig(
    level=logging.INFO,  # Log all levels (DEBUG and above)
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(os.path.join(log_dir, f"app_{datetime.datetime.now()}.log")),
        logging.StreamHandler()  # Also print logs to the console
    ]
)

def main():
    # initialize the database
    client = ArxivClient()
    
    # get new papers
    new_papers = client.get_new_papers()

    # update the database
    # insert new papers into the database
    # all the papers should be recorded to avoid duplicate searches
    client.conn.executemany(
        "INSERT INTO processed (id, title) VALUES (?, ?)",
        [(p['id'][:-2], p['title']) for p in new_papers]
    )
    client.conn.commit()
    client.conn.close()
    
    # filter papers
    filtered_papers = PaperFilter.filter_papers(new_papers)
    logging.info(f"Filtered {len(filtered_papers)} papers out of {len(new_papers)} papers.")
    
    # download PDFs
    PDFDownloader.download(filtered_papers)
    
    # analyze papers
    for i, paper in enumerate(filtered_papers):
        paper['analysis'] = PaperAnalyzer.analyze_paper(paper)
        logging.info(f"({i + 1}/{len(filtered_papers)}) Analyzed paper: {paper['title']}")
    
    # generate report
    ReportGenerator.generate_markdown(filtered_papers)

    # clean up PDFs
    PDFCacheCleaner.cleanup_pdfs()
    
if __name__ == "__main__":
    main()