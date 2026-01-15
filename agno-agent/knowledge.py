from pathlib import Path

DOCS_PATH = Path(__file__).parent / "data" / "docs.txt"
STOP_WORDS = {"what", "is", "the", "a", "an", "how", "why", "explain", "tell", "me", "about", "can", "you"}


def load_documents() -> list[str]:
    """Load and chunk documents from docs.txt."""
    raw_text = DOCS_PATH.read_text()
    chunks = [line.strip() for line in raw_text.split("\n") if line.strip()]
    return chunks


def retrieve_relevant_chunks(query: str, chunks: list[str]) -> list[str]:
    """Retrieve chunks that match keywords in the query."""
    # Extract keywords
    words = query.lower().replace(",", "").replace("?", "").replace(".", "").split()
    keywords = [w for w in words if len(w) > 2 and w not in STOP_WORDS]

    # Find matching chunks
    matches = []
    for chunk in chunks:
        chunk_lower = chunk.lower()
        if any(kw in chunk_lower for kw in keywords):
            matches.append(chunk)

    return matches
