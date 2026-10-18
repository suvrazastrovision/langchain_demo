# Sherlock PDF

A small semantic-search demo that finds relevant excerpts in local PDF articles. Results include the PDF filename, page number, relevance score, and excerpt text.

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Create a `.env` file containing your OpenAI API key:

```env
OPENAI_API_KEY=your_api_key
```

## Usage

1. Add PDF files to `docs/`.
2. Set the search question in `main()` inside `sherlock_pdf.py`.
3. Run:

```powershell
python sherlock_pdf.py
```

Example result:

```text
0.91 | article.pdf, page 5 | Relevant excerpt from the article...
```

The vector store is in memory and is rebuilt each time the script runs.
