import streamlit as st
import pandas as pd
from serpapi import GoogleSearch
from dotenv import load_dotenv
from datetime import datetime, timedelta
from dateutil import parser
import os
import base64

# Load environment variables
load_dotenv()
SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")

# Streamlit config
st.set_page_config(page_title="Malaysia Energy NewsBot", layout="wide")

# Load and center logo properly
logo_path = "logo.webp"
if os.path.exists(logo_path):
    with open(logo_path, "rb") as img_file:
        b64_encoded = base64.b64encode(img_file.read()).decode()
    st.markdown(
        f"""
        <div style='text-align: center;'>
            <img src='data:image/webp;base64,{b64_encoded}' width='200'/>
        </div>
        """,
        unsafe_allow_html=True
    )
else:
    st.warning("⚠️ Logo not found. Ensure 'logo.webp' is in the same folder as this file.")

# Title
st.markdown("<h1 style='text-align: center;'>👋 Konnichiwa Shizenian, let's get you up to speed</h1>", unsafe_allow_html=True)
st.markdown("")

# Optional filter
filter_keyword = st.text_input("🔎 Optional: Filter results by topic/keyword", "")

# Keywords to search
keywords = [
    "renewable energy Malaysia", "solar Malaysia", "corporate renewable energy supply scheme Malaysia",
    "CRESS Malaysia", "PPA Malaysia", "RP4 Malaysia", "Review Period 4 Malaysia",
    "Energy Commission Malaysia", "Suruhanjaya Tenaga", "electricity Malaysia",
    "electricity tariff Malaysia", "energy Malaysia", "voltage Malaysia"
]

# Google News search function
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

# Button to trigger scraping
if st.button("📰 Scrape Now", type="primary"):
    all_articles = []
    now = datetime.now()
    cutoff = now - timedelta(days=30)

    with st.spinner("Scraping news from the past 30 days..."):
        for kw in keywords:
            results = google_news_search(kw)
            for r in results:
                title = r.get("title", "No Title")
                link = r.get("link")
                source = r.get("source")
                date_str = r.get("date")

                try:
                    published = parser.parse(date_str, fuzzy=True)
                    published = published.replace(tzinfo=None)  # Remove timezone to avoid comparison error
                except:
                    continue

                if published < cutoff:
                    continue

                all_articles.append({
                    "datetime": published,
                    "title": title,
                    "link": link,
                    "source": source
                })

    # Sort by datetime descending
    sorted_articles = sorted(all_articles, key=lambda x: x["datetime"], reverse=True)

    # Keyword filter
    if filter_keyword:
        sorted_articles = [a for a in sorted_articles if filter_keyword.lower() in a["title"].lower()]

    # Display results
    for article in sorted_articles:
        st.markdown(f"### [{article['title']}]({article['link']})")
        st.markdown(f"<small>{article['datetime'].strftime('%Y-%m-%d')} | {article['source']}</small>", unsafe_allow_html=True)
        st.markdown("---")
