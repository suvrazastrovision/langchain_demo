from pathlib import Path

from dotenv import load_dotenv
from langchain_community.document_loaders import DirectoryLoader, PyMuPDFLoader
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter


DOCS_PATH = Path(__file__).resolve().parent / "docs"
EMBEDDING_MODEL = "text-embedding-3-small"
load_dotenv(Path(__file__).resolve().parent / ".env")


def load_notes(folder):
    """Load PDF research notes as LangChain Document objects."""
    loader = DirectoryLoader(
        str(folder),
        glob="*.pdf",
        loader_cls=PyMuPDFLoader,
    )
    return loader.load()


def split_notes(documents):
    """Split loaded notes while preserving document metadata."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=220,
        chunk_overlap=40,
        separators=["\n\n", "\n", " ", ""],
    )
    return splitter.split_documents(documents)


def build_store(chunks):
    """Build an in-memory LangChain vector store from document chunks."""
    embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL)
    return InMemoryVectorStore.from_documents(chunks, embeddings)


def hunt(query, store, top_k=3):
    """Return the strongest evidence chunks for a query."""
    if not isinstance(top_k, int) or isinstance(top_k, bool) or top_k <= 0:
        raise ValueError("top_k must be a positive integer")

    matches = store.similarity_search_with_score(query, k=top_k)
    return [
        {
            "score": score,
            "source": Path(document.metadata["source"]).name,
            # PyMuPDFLoader stores a zero-based PDF page index.
            "page": document.metadata["page"] + 1,
            "text": document.page_content,
        }
        for document, score in matches
    ]


def print_evidence(query, results):
    """Print a compact evidence report."""
    print("SHERLOCK PDF")
    print(f"Query: {query}")
    print()

    if not results:
        print("Best evidence:")
        print("No evidence found.")
        return

    print("Best evidence:")
    for item in results:
        print(
            f"{item['score']:.2f} | {item['source']}, page {item['page']} | "
            f"{item['text']}"
        )


def main():
    query = ( "How do inhibitory glutamatergic synapses between dorsal fan-shaped "
    "body neurons generate slow-wave activity and regulate sleep pressure "
    "in Drosophila?")
    documents = load_notes(DOCS_PATH)
    chunks = split_notes(documents)
    store = build_store(chunks)
    results = hunt(query, store, top_k=3)
    print_evidence(query, results)


if __name__ == "__main__":
    main()
