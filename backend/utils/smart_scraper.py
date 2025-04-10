import requests
from bs4 import BeautifulSoup
from duckduckgo_search import DDGS

def smart_keyword_scraper(query, max_results=3):
    results = []

    try:
        with DDGS() as ddgs:
            search_results = ddgs.text(query, max_results=max_results)

            for result in search_results:
                url = result.get("href")
                if not url:
                    continue

                try:
                    page = requests.get(url, timeout=5)
                    soup = BeautifulSoup(page.content, "html.parser")
                    text = soup.get_text(separator=" ", strip=True)

                    snippet = text[:1000] + "..." if len(text) > 1000 else text
                    results.append({
                        "url": url,
                        "content": snippet
                    })
                except Exception as inner_err:
                    print(f"Error scraping {url}: {inner_err}")
                    continue

    except Exception as outer_err:
        print(f"Smart scraper error: {outer_err}")

    return results
