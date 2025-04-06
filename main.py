from arxiv_client import ArxivClient
from paper_filter import PaperFilter
from pdf_downloader import PDFDownloader
from paper_analyzer import PaperAnalyzer
from report_generator import ReportGenerator

def main():
    # initialize the database
    client = ArxivClient()
    
    # get new papers
    new_papers = client.get_new_papers()

    # update the database
    client.conn.executemany(
        "INSERT INTO processed (id, title) VALUES (?, ?)",
        [(p['id'], p['title']) for p in new_papers]
    )
    client.conn.commit()
    client.conn.close()
    
    # filter papers
    filtered_papers = PaperFilter.filter_papers(new_papers)
    
    # download PDFs
    PDFDownloader.download(filtered_papers)
    
    # analyze papers
    for paper in filtered_papers:
        paper['analysis'] = PaperAnalyzer.analyze_paper(paper)
    
    # generate report
    ReportGenerator.generate_markdown(filtered_papers)
    
if __name__ == "__main__":
    main()