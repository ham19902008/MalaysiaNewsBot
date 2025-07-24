import streamlit as st
import pandas as pd
from serpapi import GoogleSearch
from dotenv import load_dotenv
from datetime import datetime
from dateutil import parser
import os
import requests
from bs4 import BeautifulSoup

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

# Set page config
st.set_page_config(page_title="Malaysia Energy NewsBot", layout="wide")

# Display logo (make sure logo.webp is in the same directory)
st.markdown(
    """
    <div style="text-align: center;">
        <img src="logo.webp" width="200"/>
    </div>
    """,
    unsafe_allow_html=True
)

# Page header
st.markdown("<h1 style='text-align: center;'>👋 Konnichiwa Shizenian, let's get you up to speed</h1>", unsafe_allow_html=True)
st.markdown("")

# Filter input
filter_keyword = st.text_input("🔎 Optional: Filter results by topic/keyword", "")

# Scrape function
def google_search(query):
    params = {
        "q": query,
        "engine": "google",
        "api_key": SERPAPI_API_KEY,
        "num": 3,
        "hl": "en",
        "gl": "my"
    }
    search = GoogleSearch(params)
    results = search.get_dict()
    return results.get("organic_results", [])

# Scrape on button click
if st.button("📰 Scrape Now", type="primary"):
    all_articles = []

    with st.spinner("Scraping news..."):
        for kw in keywords:
            results = google_search(kw)
            for r in results:
                title = r.get("title")
                link = r.get("link")
                snippet = r.get("snippet", "")
                date_str = r.get("date") or snippet[:50]
                try:
                    parsed_date = parser.parse(date_str, fuzzy=True)
                except:
                    parsed_date = datetime.now()

                all_articles.append({
                    "datetime": parsed_date,
                    "title": title,
                    "link": link,
                })

    # Sort results by datetime descending
    sorted_articles = sorted(all_articles, key=lambda x: x["datetime"], reverse=True)

    # Optional filter
    if filter_keyword:
        sorted_articles = [
            a for a in sorted_articles
            if filter_keyword.lower() in a["title"].lower()
        ]

    # Display articles
    for article in sorted_articles:
        st.markdown(f"### [{article['title']}]({article['link']})")
        st.markdown(f"<small>{article['datetime'].strftime('%Y-%m-%d %H:%M')}</small>", unsafe_allow_html=True)
        st.markdown("---")
