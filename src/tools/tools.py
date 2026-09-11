import os
import re
import requests
import trafilatura
from readability import Document
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from langchain_core.tools import tool
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper

load_dotenv()

wrapper = DuckDuckGoSearchAPIWrapper(max_results=5)


@tool
def web_search(query: str) -> str:
    """Search the web for recent and reliable information on a topic. Returns Titles, URLs, and Snippets."""
    results = wrapper.results(query, max_results=5)

    out = []
    for r in results:
        out.append(
            f"Title: {r['title']}\nURL: {r['link']}\nSnippet: {r['snippet'][:300]}\n"
        )

    return "\n----\n".join(out)


@tool
def scrape_url(url: str) -> str:
    """Scrape and extract clean, readable content from a URL. Uses multiple extraction strategies for better reliability."""
    try:
        response = requests.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
        html = response.text

        text = trafilatura.extract(html)

        if not text:
            doc = Document(html)
            summary_html = doc.summary()
            soup = BeautifulSoup(summary_html, "html.parser")
            text = soup.get_text(separator=" ", strip=True)

        if not text:
            soup = BeautifulSoup(html, "html.parser")
            for tag in soup(["script", "style"]):
                tag.decompose()
            text = soup.get_text(separator=" ", strip=True)

        text = re.sub(r"\s+", " ", text).strip()
        return text[:3000]

    except Exception as e:
        return f"Could not scrape {url}: {e}"


if __name__ == "__main__":
    print(web_search.invoke("latest AI news"))
    print(scrape_url.invoke("https://www.bbc.com/news"))