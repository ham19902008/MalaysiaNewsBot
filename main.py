import streamlit as st
import pandas as pd
from serpapi import GoogleSearch
from dotenv import load_dotenv
from datetime import datetime, timedelta
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

# Streamlit config
st.set_page_config(page_title="Malaysia Energy NewsBot", layout="wide")

# Centered logo using HTML
st.markdown(
    """
    <div style='text-align: center;'>
        <img src='logo.webp' width='200'/>
    </div>
    """,
    unsafe_allow_html=True
)

# Title header
st.markdown("<h1 style='text-align: center;'>👋 Konnichiwa Shizenian, let's get you up to speed</h1>", unsafe_allow_html=True)
st.markdown("")

# Optional keyword filter
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

# Scrape Now button
if st.button("📰 Scrape Now", type="primary"):
    all_articles = []
    now = datetime.now()
    five_days_ago = now - timedelta(days=5)

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
                    continue  # Skip articles with bad date

                # Filter: Only include articles from the past 5 days
                if published < five_days_ago:
                    continue

                all_articles.append({
                    "datetime": published,
                    "title": title,
                    "link": link,
                    "source": source
                })

    # Sort articles by datetime descending
    sorted_articles = sorted(all_articles, key=lambda x: x["datetime"], reverse=True)

    # Optional filtering
    if filter_keyword:
        sorted_articles = [a for a in sorted_articles if filter_keyword.lower() in a["title"].lower()]

    # Display articles
    for article in sorted_articles:
        st.markdown(f"### [{article['title']}]({article['link']})")
        st.markdown(f"<small>{article['datetime'].strftime('%Y-%m-%d')} | {article['source']}</small>", unsafe_allow_html=True)
        st.markdown("---")
