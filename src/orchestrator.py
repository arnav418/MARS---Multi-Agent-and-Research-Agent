"""
orchestrator.py

The central controller that runs the full MARS pipeline:

1. Research Agent    → Live search + fetch + chunk
2. Embeddings        → Convert chunks into vectors
3. Vector DB         → Upsert into Chroma
4. Retrieval         → Query memory for relevant text
5. Summary Agent     → RAG summary using LLM
6. Fact-Check Agent  → Validate summary against context

This makes it easy to call:
    answer = answer_query("What is AI doing in healthcare?")
"""

from typing import Dict
from src.agents.research_live import research_pipeline
from src.utils.embeddings import embed_text
from src.db.chroma_store import upsert_chunk, query_memory
from src.agents.summary_agent import generate_summary, format_context
from src.agents.factcheck_agent import fact_check, annotate_summary


# -------------------------------------------------------------
# 1. INGEST PIPELINE
# -------------------------------------------------------------

def ingest_query(query: str, pages: int = 3):
    """
    Runs:
    - Live search
    - Fetching content
    - Chunking
    - Embedding
    - Upserting into Chroma DB
    """
    print(f"\n[🔍] Researching online for: {query}\n")

    results = research_pipeline(query, max_pages=pages)

    for item in results:
        source = item["source"]
        chunks = item["chunks"]

        for chunk in chunks:
            emb = embed_text(chunk)[0]
            upsert_chunk(chunk, emb, source)

    print("[📥] Ingestion complete!\n")


# -------------------------------------------------------------
# 2. ANSWER PIPELINE (RAG + FACT CHECK)
# -------------------------------------------------------------

def answer_query(query: str, top_k: int = 5) -> Dict:
    """
    High-level function to:
    - Ingest live data
    - Generate RAG-based summary
    - Fact-check the summary
    """

    # Step 1 → Ingest and update memory
    ingest_query(query)

    # Step 2 → Generate summary
    summary = generate_summary(query, top_k=top_k)

    # Step 3 → Retrieve context again for fact-checking
    q_emb = embed_text(query)[0]
    retrieved = query_memory(q_emb, top_k=top_k)
    context_text = format_context(retrieved)

    # Step 4 → Fact-check
    fc_results = fact_check(summary, context_text)

    # Step 5 → Annotate summary
    final_output = annotate_summary(summary, fc_results)

    return {
        "query": query,
        "summary": summary,
        "fact_check": fc_results,
        "final_output": final_output
    }


# -------------------------------------------------------------
# 3. CLI FRIENDLY ENTRY POINT
# -------------------------------------------------------------

if __name__ == "__main__":
    q = input("Ask MARS a question: ")
    result = answer_query(q)

    print("\n\n===== FINAL ANSWER =====\n")
    print(result["final_output"])
