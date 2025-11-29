"""
research_live.py

This agent performs:
<<<<<<< HEAD
1. Live web search (via SerpAPI)
=======
1. Live web search (via Google Custom Search API)
>>>>>>> ec1bd1a (Upload full local project)
2. Fetching webpage content
3. Extracting readable text
4. Chunking the text for embeddings
"""

import os
import requests
from bs4 import BeautifulSoup
<<<<<<< HEAD
from serpapi import GoogleSearch
=======
from googleapiclient.discovery import build
>>>>>>> ec1bd1a (Upload full local project)
from typing import List, Dict


# -----------------------------------------------------------
<<<<<<< HEAD
# 1. LIVE SEARCH USING SERPAPI
# -----------------------------------------------------------
def search_web(query: str, num_results: int = 5) -> List[str]:
    """
    Performs a live Google search using SerpAPI and returns a list of URLs.
=======
# 1. LIVE SEARCH USING GOOGLE CUSTOM SEARCH API
# -----------------------------------------------------------
def search_web(query: str, num_results: int = 5) -> List[str]:
    """
    Performs a live Google search using the Google Custom Search API and returns a list of URLs.
>>>>>>> ec1bd1a (Upload full local project)

    Args:
        query (str): search query
        num_results (int): number of results to fetch

    Returns:
        List[str]: list of URLs
    """

<<<<<<< HEAD
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
=======
    api_key = os.environ.get("GOOGLE_API_KEY")
    cse_id = os.environ.get("CUSTOM_SEARCH_ENGINE_ID")

    if not api_key:
        raise Exception("Missing GOOGLE_API_KEY in environment variables.")
    if not cse_id:
        raise Exception("Missing CUSTOM_SEARCH_ENGINE_ID in environment variables.")

    try:
        service = build("customsearch", "v1", developerKey=api_key)
        res = service.cse().list(q=query, cx=cse_id, num=num_results).execute()
        
        urls = [item['link'] for item in res.get('items', [])]
        return urls

    except Exception as e:
        print(f"Error during Google search: {e}")
        return []
>>>>>>> ec1bd1a (Upload full local project)


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
