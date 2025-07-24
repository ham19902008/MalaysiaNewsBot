import os
import requests
from dotenv import load_dotenv

load_dotenv()
SERP_API_KEY = os.getenv("SERPAPI_API_KEY")

KEYWORDS = [
    "malaysia", "renewable energy", "solar", "national energy transition roadmap",
    "carbon tax", "electricity", "tenaga nasional berhad", "suruhanjaya tenaga",
    "energy commission", "electricity tariff", "CRESS", "PPA", "LSS"
]

def scrape_news():
    url = "https://serpapi.com/search"
    params = {
        "q": " OR ".join(KEYWORDS) + " site:news.google.com",
        "api_key": SERP_API_KEY,
        "engine": "google_news",
        "num": 10
    }

    response = requests.get(url, params=params)
    results = response.json().get("news_results", [])
    
    articles = []
    for article in results:
        articles.append({
            "title": article.get("title"),
            "link": article.get("link"),
            "date": article.get("date"),
        })
    
    return articles
