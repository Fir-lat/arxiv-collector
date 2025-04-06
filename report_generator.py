import datetime
import os
from config import Config

class ReportGenerator:
    @staticmethod
    def generate_markdown(papers):
        content = "# Daily Paper Report\n\n"
        content += f"Data: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
        
        for paper in papers:
            content += f"## {paper['title']}\n"
            content += f"- **URL**: [arXiv:{paper['id']}]({paper['pdf_url']})\n"
            content += f"- **Category**: {paper['category']}/10\n"
            content += f"- **Publication**: {paper.get('conference_acceptance', 'None')}\n\n"
            content += paper['analysis'] + "\n\n"
            content += "------\n\n"
        
        filename = f"report_{datetime.date.today()}.md"
        with open(os.path.join(Config.BASE_PATH, filename), 'w') as f:
            f.write(content)

if __name__ == '__main__':
    
    # 假设已经有了筛选后的论文列表
    filtered_papers = [
        {
            "id": "2501.16718v1",
            "title": "HamOS: Outlier Synthesis via Hamiltonian Monte Carlo for Out-of-Distribution Detection",
            "pdf_url": "https://arxiv.org/pdf/2501.16718v1",
            "published": datetime.date.today(),
            "category": "Machine Learning",
            "conference_acceptance": "ICLR 2025",
            "analysis": "This paper presents a novel approach to out-of-distribution detection using Hamiltonian Monte Carlo.",
        }
    ]
    
    ReportGenerator.generate_markdown(filtered_papers)