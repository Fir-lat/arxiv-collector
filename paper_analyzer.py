import datetime
import logging
import re
import os
import requests
from openai import OpenAI

import pymupdf4llm
import pathlib

from config import Config


def remove_markdown_wrapper(text):
    """
    Removes ```markdown...``` wrapping if present.
    Returns the original string otherwise.
    """
    pattern = r"^```markdown(.*?)```$"
    match = re.match(pattern, text, re.DOTALL)
    return match.group(1) if match else text


class PDFParser:
    @staticmethod
    def extract_text(pdf_path):
        """extract text from PDF file"""
        text = pymupdf4llm.to_markdown(pdf_path)

        return text[:60000]

class PaperAnalyzer:
    @staticmethod
    def analyze_paper(paper):
        """analyze paper using DeepSeek API"""

        client = OpenAI(api_key=Config.API_KEY, base_url=Config.BASE_URL)

        full_text = PDFParser.extract_text(paper['local_path'])

        system_prompt = f"""
            The user will provide a paper. Please analyze according to the instruction and output them in Markdown format. 

            REQUIREMENTS:
            - Output in Markdown format
            - Each part contains a fiew sentences
            - Use simple and understandable language
            - Highlight the technical highlights and core technical contributions

            EXAMPLE INPUT: 
            Analyze this paper and summarize it.
            [Title] {"Do AI Scientists Dream of Electric Sheep?"}
            [Contents] {"This paper ..."}

            EXAMPLE MARKDOWN OUTPUT:
            ### Research Task
            ### Core Motivation
            ### Method Description
            ### Experimental Results
            ### Key Innovations
        """

        analysis_prompt = f"""Please analyze the following paper and summarize it.
            [Title] {paper['title']}
            [Contents] {full_text}
        """

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": analysis_prompt}
        ]
        response = client.chat.completions.create(
            model="deepseek-reasoner",
            messages=messages,
            temperature=1.0,
        )

        
        return remove_markdown_wrapper(response.choices[0].message.content)
    
if __name__ == '__main__':

    filtered_papers = [
        {
            "id": "2501.16718v1",
            "title": "HamOS: Outlier Synthesis via Hamiltonian Monte Carlo for Out-of-Distribution Detection",
            "pdf_url": "https://arxiv.org/pdf/2501.16718v1",
            "published": datetime.date.today(),
            "category": "Machine Learning",
            "local_path": "../arxiv_collection/machine learning/2025-04-06/2501.16718v1_HamOS__Outlier_Synthesis_via_Hamiltonian_Monte_Carlo_for_Out_of_Distribution_Detection.pdf"
        }
    ]

    for paper in filtered_papers:
        
        analysis_result = PaperAnalyzer.analyze_paper(paper)
        logging.info(analysis_result)