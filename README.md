# arxiv-collector

This repo is the python implementation of [arxiv-collector] which utilizes LLMs to retrieve and analyze the updated papers on arxiv


## Architecture

```bash
arxiv_collection/
├── config.py            # 配置文件
├── arxiv_client.py      # arXiv数据获取模块
├── paper_filter.py      # 论文筛选模块
├── pdf_downloader.py    # PDF下载模块
├── paper_analyzer.py    # 论文分析模块
├── report_generator.py  # 报告生成模块
└── main.py              # 主流程控制
```