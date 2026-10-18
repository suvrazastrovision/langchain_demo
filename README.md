# Sherlock PDF

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![LangChain](https://img.shields.io/badge/Built%20with-LangChain-1C3C3C)](https://docs.langchain.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**Sherlock PDF** is a small semantic-search tool for scientific literature. Ask a question in natural language and it retrieves relevant passages from local PDFs with the source filename, page number, similarity score, and original text.

> Because *"I remember reading that somewhere"* is not a reproducible research method.

📖 [Read the complete hands-on tutorial](https://medium.com/@suvranath047/a-hands-on-langchain-tutorial-building-sherlock-pdf-for-smarter-scientific-literature-search-be56f5cde245?sharedUserId=suvranath047)

## Why LangChain?

[LangChain](https://docs.langchain.com/) provides reusable components for loading documents, splitting text, creating embeddings, and searching vector stores. Sherlock PDF connects these components in a simple pipeline:

```text
PDFs → page-aware chunks → OpenAI embeddings → similarity search → evidence
```

Embeddings make it possible to find passages with similar meanings even when they use different terminology from the question.

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Create a `.env` file containing your OpenAI API key:

```env
OPENAI_API_KEY=your_api_key
```

## Usage

1. Add text-based PDFs to `docs/`.
2. Set the `query` in `main()` inside `sherlock_pdf.py`.
3. Run:

```powershell
python sherlock_pdf.py
```

Example:

```text
0.91 | article.pdf, page 5 | Relevant excerpt from the article...
```

Always open the cited page and verify the result in context. Semantic similarity finds related text; it does not validate a scientific claim.

The current in-memory index is rebuilt each time the script runs. PDF text is sent to the OpenAI API for embedding, so only use documents allowed by your data policy.
