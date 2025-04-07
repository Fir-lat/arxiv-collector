# arxiv-collector

This repo is the python implementation of [arxiv-collector] which utilizes LLMs to retrieve and analyze the updated papers on arxiv


## Architecture

```bash
arxiv_collection/
├── config.py            # configuration
├── arxiv_client.py      # arXiv retriever
├── paper_filter.py      # paper filter
├── pdf_downloader.py    # paper downloader
├── paper_analyzer.py    # paper analyzer
├── report_generator.py  # report generator
├── pdf_cleaner.py       # paper cache cleaner
└── main.py              # main process
```


## DeepSeek API

Please create the '''.env''' file :
```bash
touch .env
```

And place your deepseek api key as:

```bash
API_KEY=sk-XXX
```