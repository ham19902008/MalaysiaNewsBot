import streamlit as st
import pandas as pd
from serpapi import GoogleSearch
from dotenv import load_dotenv
from datetime import datetime
from dateutil import parser
import os

# Load environment variables
load_dotenv()
SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")

# Keywords for Malaysia energy news
keywords = [
    "renewable energy Malaysia", "solar Malaysia", "corporate renewable energy supply scheme Malaysia",
    "CRESS Malaysia", "PPA Malaysia", "RP4 Malaysia", "Review Period 4 Malaysia",
    "Energy Commission Malaysia", "Suruhanjaya Tenaga", "electricity Malaysia",
    "electricity tariff Malaysia", "energy Malaysia", "voltage Malaysia"
]

# Page config
st.set_page_config(page_title="Malaysia Energy NewsBot", layout="wide")

# Show logo (ensure logo.webp is in the same directory)
st.image("logo.webp", width=200)

# Header
st.markdown("<h1 style='text-align: center;'>👋 Konnichiwa Shizenian, let's get you up to speed</h1>", unsafe_allow_html=True)
st.markdown("")

# Optional filter
filter_keyword = st.text_input("🔎 Optional: Filter results by topic/keyword", "")

# Scraper function using Google News
def google_news_search(query):
    params = {
        "q": query,
        "engine": "google_news",
        "api_key": SERPAPI_API_KEY,
        "hl": "en",
        "gl": "my",
        "num": 5
    }
    search = GoogleSearch(params)
    return search.get_dict().get("news_results", [])

# Scrape button
if st.button("📰 Scrape Now", type="primary"):
    all_articles = []

    with st.spinner("Scraping recent news..."):
        for kw in keywords:
            results = google_news_search(kw)
            for r in results:
                title = r.get("title", "No Title")
                link = r.get("link")
                source = r.get("source")
                date_str = r.get("date")

                try:
                    published = parser.parse(date_str, fuzzy=True)
                except:
                    published = datetime.now()

                all_articles.append({
                    "datetime": published,
                    "title": title,
                    "link": link,
                    "source": source
                })

    # Sort by datetime descending
    sorted_articles = sorted(all_articles, key=lambda x: x["datetime"], reverse=True)

    # Filter if needed
    if filter_keyword:
        sorted_articles = [a for a in sorted_articles if filter_keyword.lower() in a["title"].lower()]

    # Display results
    for article in sorted_articles:
        st.markdown(f"### [{article['title']}]({article['link']})")
        st.markdown(f"<small>{article['datetime'].strftime('%Y-%m-%d')} | {article['source']}</small>", unsafe_allow_html=True)
        st.markdown("---")
