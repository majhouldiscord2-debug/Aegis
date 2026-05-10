import requests
from bs4 import BeautifulSoup

def search_web(query):
    """
    Performs a basic web search using a search engine (simulated with DuckDuckGo).
    """
    try:
        url = f"https://html.duckduckgo.com/html/?q={query}"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        results = []
        for result in soup.find_all('a', class_='result__a', limit=3):
            results.append(f"{result.text}: {result['href']}")
            
        return "\n".join(results) if results else "No results found."
    except Exception as e:
        return f"Search Error: {str(e)}"

def fetch_url(url):
    """
    Fetches the content of a specific URL and returns a text summary.
    """
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.extract()
            
        text = soup.get_text()
        # Clean up whitespace
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = '\n'.join(chunk for chunk in chunks if chunk)
        
        return text[:1000] + "..." if len(text) > 1000 else text
    except Exception as e:
        return f"Fetch Error: {str(e)}"
