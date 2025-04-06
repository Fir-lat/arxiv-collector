import requests
import json
from openai import OpenAI
from config import Config
from arxiv_client import ArxivClient

class PaperFilter:
    @staticmethod
    def filter_papers(papers):
        """使用DeepSeek API筛选论文"""

        system_prompt = f"""
            The user will provide a paper. Please analyze according to the instruction and output them in JSON format. 

            EXAMPLE INPUT: 
            Analyze this paper metadata and check if it meets ANY of these categories: [example category 1, example category 2]
            
            Paper Title: {"Do AI Scientists Dream of Electric Sheep?"}
            Abstract: {"This paper ..."}
            Comments: {"Accepted at ABCD"}

            EXAMPLE JSON OUTPUT:
            {{
                "meets_criteria": bool,
                "relevance_score": 0-10,
                "conference_acceptance": str|null,
                "category": str,
                "key_innovations": list[str]
            }}
        """
        client = OpenAI(api_key=Config.API_KEY, base_url=Config.BASE_URL)
        filtered = []
        for paper in papers:
            # 构建分析提示词
            prompt = f"""Analyze this paper metadata and check if it meets ANY of these criteria:
            - {Config.TARGET_TOPICS}
            
            Paper Title: {paper['title']}
            Abstract: {paper['abstract']}
            Comments: {paper['comments']}
            """
            
            # 调用DeepSeek API
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ]
            response = client.chat.completions.create(
                model="deepseek-chat",
                messages=messages,
                response_format={
                    'type': 'json_object'
                }
            )

            # 解析响应
            try:
                result = json.loads(response.choices[0].message.content)
                if result['meets_criteria'] and result['relevance_score'] >= 8:
                    paper.update(result)
                    filtered.append(paper)
            except:
                print(f"Error processing paper: {paper['title']}")
                continue
        
        # 按相关性排序
        return sorted(filtered, key=lambda x: x['relevance_score'], reverse=True)
    

if __name__ == '__main__':
    arxiv_client = ArxivClient()
    new_papers = arxiv_client.get_new_papers()

    cursor = arxiv_client.conn.cursor()
    cursor.execute("INSERT INTO processed (id, title) VALUES (?, ?)", 
            (new_papers['id'][:-2], new_papers['title']))
    arxiv_client.conn.commit()
    arxiv_client.conn.close()
    
    # 筛选论文
    filtered_papers = PaperFilter.filter_papers(new_papers)
    
    # 打印筛选结果
    for paper in filtered_papers:
        print(f"Title: {paper['title']}")
        print(f"ID: {paper['id']}")
        print(f"Published: {paper['published']}")
        print(f"Relevance Score: {paper['relevance_score']}")
        print(f"Category: {paper['category']}")
        print(f"Conference Acceptance: {paper['conference_acceptance']}")
        print(f"Key Innovations: {', '.join(paper['key_innovations'])}")
        print("-" * 80)