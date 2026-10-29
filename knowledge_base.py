"""
L7 — Personal Knowledge Base  (STARTER)
========================================
Run with:
    python starter.py

Your goal: build a persistent ChromaDB knowledge base from course content and
demonstrate metadata-filtered semantic search.

Required features:
    1. A persistent ChromaDB client (data survives restarts)
    2. A collection called "my_knowledge" created with get_or_create_collection
    3. At least 15 documents from at least 3 different modules, each with:
       - A unique ID (e.g. "doc_01")
       - Text content (a sentence or short paragraph)
       - Metadata with at least `module` (e.g. "5") and `topic`
         (e.g. "api", "database", "frontend", "ai")
    4. A search() function that accepts a query and optional module filter
       and returns the top 5 results with distances and metadata
    5. At least 3 test queries:
       - One broad (no filter)
       - One filtered to a specific module
       - One where the query words differ from the stored documents

Key concepts:
    Persistent client:
        client = chromadb.PersistentClient(path="./chroma_db")

    Upsert avoids errors on re-runs:
        collection.upsert(ids=[...], documents=[...], metadatas=[...])

    Metadata filtering:
        collection.query(
            query_texts=["your query"],
            n_results=5,
            where={"module": "5"}   # only return docs from module 5
        )

    Result structure:
        results["ids"][0]        # list of IDs
        results["documents"][0]  # list of document strings
        results["metadatas"][0]  # list of metadata dicts
        results["distances"][0]  # list of distances (lower = more similar)
"""

import chromadb

# ── Client & collection ──────────────────────────────────────────────────────
# TODO: Create a PersistentClient with path="./chroma_db"
# TODO: Get or create a collection called "my_knowledge"

client = chromadb.PersistentClient(path="./chroma_db")

collection = client.get_or_create_collection(
    name="my_knowledge",
    configuration={"hsnw": {"space": "cosine"}}
)

# ── Documents ────────────────────────────────────────────────────────────────
# TODO: Define three lists that match in length:
#   ids       — unique strings like "doc_01", "doc_02", ...
#   documents — text summaries from at least 3 different modules
#   metadatas — dicts with at least {"module": "X", "topic": "Y"}
#
# Aim for at least 15 documents.

ids = [f"doc_{i:02d}" for i in range(1, 16)]

documents = [
    # Module 3 — Databases
    "SQLAlchemy maps Python classes to relational database tables.",
    "SQLite stores structured data in a lightweight relational database.",
    "CRUD operations allow applications to create, read, update, and delete database records.",
    "Database relationships connect records using primary and foreign keys.",
    "SQL queries retrieve and filter information stored in database tables.",

    # Module 5 — FastAPI
    "FastAPI creates REST API endpoints using Python decorators.",
    "Pydantic models validate incoming API request data.",
    "JWT tokens authenticate users and protect API endpoints.",
    "FastAPI background tasks execute operations after returning a response.",
    "Pytest and TestClient automate testing of FastAPI endpoints.",

    # Module 6 — Streamlit
    "Streamlit creates interactive Python web applications and dashboards.",
    "Streamlit session state preserves values between application reruns.",
    "Streamlit widgets collect user input through buttons, sliders, and text fields.",
    "Pandas processes and organizes datasets for visualization.",
    "Streamlit displays charts and tables to help users explore data."
]

metadatas = [
    {"module": "3", "topic": "orm"},
    {"module": "3", "topic": "database"},
    {"module": "3", "topic": "crud"},
    {"module": "3", "topic": "relationships"},
    {"module": "3", "topic": "sql"},

    {"module": "5", "topic": "api"},
    {"module": "5", "topic": "validation"},
    {"module": "5", "topic": "authentication"},
    {"module": "5", "topic": "background_tasks"},
    {"module": "5", "topic": "testing"},

    {"module": "6", "topic": "frontend"},
    {"module": "6", "topic": "session_state"},
    {"module": "6", "topic": "widgets"},
    {"module": "6", "topic": "data"},
    {"module": "6", "topic": "visualization"}
]

# TODO: Upsert all documents into the collection

collection.upsert(
    documents=documents,
    metadatas=metadatas,
    ids=ids
)

print(f"Upserted {len(documents)} documents.")
print(f"Collection now has {collection.count()} documents.")


# ── Search function ──────────────────────────────────────────────────────────
def search(query: str, module_filter: str = None, n_results: int = 5):
    """Return top results for query, optionally filtered to a specific module."""
    # TODO: Build the where dict only when module_filter is provided
    # TODO: Call collection.query() with query_texts, n_results, and where
    # TODO: Print each result's rank, distance, metadata, and document text
    
    where_filter = {"module": module_filter} if module_filter else None

    results = collection.query(
        query_texts=[query],
        n_results=n_results,
        where=where_filter
    )

    for i, doc in enumerate(results["documents"][0], start=1):
        distance = results["distances"][0][i - 1]
        metadata = results["metadatas"][0][i - 1]

        print(f"\n{i}. Distance: {distance:.4f}")
        print(f"   Module: {metadata['module']}")
        print(f"   Topic: {metadata['topic']}")
        print(f"   Document: {doc}")

# ── Test queries ─────────────────────────────────────────────────────────────
print("=== Broad search (no filter) ===")
# TODO: Call search() with a broad query

search("How do Python applications manage and store data?")

print("\n=== Filtered to a specific module ===")
# TODO: Call search() with a query and a module_filter

search("How do I secure API endpoints?", module_filter="5")

print("\n=== Different words than stored documents ===")
# TODO: Call search() with a query that paraphrases rather than copies
#       the stored text — e.g. "how to handle bad user input" instead of
#       "Pydantic validates request data"

search("How can I build a website where people interact with charts?")