"""
summary_agent.py

This agent:
1. Embeds the user query
2. Retrieves relevant chunks from memory
3. Builds a RAG prompt
4. Calls an LLM (OpenAI or Gemini)
5. Produces a clean, cited summary
"""

import os
from typing import List, Dict

from src.utils.embeddings import embed_text
from src.db.chroma_store import query_memory

# If using OpenAI
from openai import OpenAI
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


# -----------------------------------------------------------
# 1. FORMAT RETRIEVED DOCUMENTS
# -----------------------------------------------------------

def format_context(results: Dict) -> str:
    """
    Convert Chroma results into readable context for the LLM.
    """

    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]

    formatted_segments = []

    for doc, meta in zip(documents, metadatas):
        src = meta.get("source", "unknown")
        formatted_segments.append(f"Source: {src}\n{doc}\n\n---")

    return "\n".join(formatted_segments)


# -----------------------------------------------------------
# 2. BUILD THE RAG PROMPT
# -----------------------------------------------------------

def build_rag_prompt(query: str, context: str) -> str:
    """
    Creates a citation-rich RAG prompt.
    """

    return f"""
You are MARS, a factual research assistant.

Use ONLY the information in the CONTEXT to answer the QUESTION.
If the answer is not found in the context, say 
"I don't have enough information in memory to answer that."

Your response MUST:
- Be accurate
- Be concise
- Include citations like [Source: URL]

QUESTION:
{query}

CONTEXT:
{context}

ANSWER:
"""
    

# -----------------------------------------------------------
# 3. GENERATE SUMMARY (CALL LLM)
# -----------------------------------------------------------

def generate_summary(query: str, top_k: int = 5) -> str:
    """
    - Embed the query
    - Retrieve chunks
    - Build prompt
    - LLM generation
    """

    # 1. Embed query
    query_embedding = embed_text(query)[0]

    # 2. Retrieve memory
    results = query_memory(query_embedding, top_k=top_k)

    # 3. Format context
    context_text = format_context(results)

    # 4. RAG prompt
    prompt = build_rag_prompt(query, context_text)

    # 5. Call LLM (OpenAI)
    completion = client.chat.completions.create(
        model="gpt-4o-mini",   # safe small model, replace if needed
        messages=[{"role": "user", "content": prompt}]
    )

    return completion.choices[0].message.content
