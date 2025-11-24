"""
research_live.py

This agent performs:
1. Live web search (via SerpAPI)
2. Fetching webpage content
3. Extracting readable text
4. Chunking the text for embeddings
"""

import os
import requests
from bs4 import BeautifulSoup
from serpapi import GoogleSearch
from typing import List, Dict


# -----------------------------------------------------------
# 1. LIVE SEARCH USING SERPAPI
# -----------------------------------------------------------
def search_web(query: str, num_results: int = 5) -> List[str]:
    """
    Performs a live Google search using SerpAPI and returns a list of URLs.

    Args:
        query (str): search query
        num_results (int): number of results to fetch

    Returns:
        List[str]: list of URLs
    """

    api_key = os.environ.get("SERPAPI_KEY")

    if not api_key:
        raise Exception("Missing SERPAPI_KEY in environment variables.")

    search = GoogleSearch({
        "q": query,
        "num": num_results,
        "api_key": api_key,
        "engine": "google"
    })

    results = search.get_dict()
    urls = []

    for result in results.get("organic_results", []):
        link = result.get("link")
        if link:
            urls.append(link)

    return urls


# -----------------------------------------------------------
# 2. FETCH WEBPAGE CONTENT
# -----------------------------------------------------------
def fetch_page_text(url: str) -> str:
    """
    Downloads webpage HTML and extracts readable text.
    """

    try:
        response = requests.get(url, timeout=10, headers={
            "User-Agent": "Mozilla/5.0 (MARS-Agent)"
        })

        soup = BeautifulSoup(response.text, "html.parser")
        paragraphs = soup.find_all("p")

        text_blocks = [p.get_text().strip() for p in paragraphs if p.get_text().strip()]
        clean_text = "\n".join(text_blocks)

        return clean_text

    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return ""


# -----------------------------------------------------------
# 3. CHUNK TEXT FOR EMBEDDINGS
# -----------------------------------------------------------
def chunk_text(text: str, chunk_size: int = 800) -> List[str]:
    """
    Splits long text into smaller chunks. Useful for embeddings.
    """
    words = text.split()
    chunks = []

    for i in range(0, len(words), chunk_size):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)

    return chunks


# -----------------------------------------------------------
# 4. FULL PIPELINE
# -----------------------------------------------------------
def research_pipeline(query: str, max_pages: int = 3, chunk_size: int = 800) -> List[Dict]:
    """
    Performs:
    - Search
    - Fetch
    - Chunk

    Returns a list of dictionaries:
    {
      "source": URL,
      "chunks": [chunk1, chunk2, ...]
    }
    """

    urls = search_web(query, num_results=max_pages)
    results = []

    for url in urls:
        raw_text = fetch_page_text(url)
        if not raw_text:
            continue

        chunks = chunk_text(raw_text, chunk_size=chunk_size)

        results.append({
            "source": url,
            "chunks": chunks
        })

    return results
