import streamlit as st
import pandas as pd
import openai
from serpapi import GoogleSearch
from dotenv import load_dotenv
from datetime import datetime
from dateutil import parser
import os
import requests
from bs4 import BeautifulSoup

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")
openai.api_key = OPENAI_API_KEY

# Static keywords list
keywords = [
    "renewable energy Malaysia", "solar Malaysia", "corporate renewable energy supply scheme Malaysia",
    "CRESS Malaysia", "PPA Malaysia", "RP4 Malaysia", "Review Period 4 Malaysia",
    "Energy Commission Malaysia", "Suruhanjaya Tenaga", "electricity Malaysia",
    "electricity tariff Malaysia", "energy Malaysia", "voltage Malaysia"
]

# Set page config
st.set_page_config(page_title="Malaysia Energy NewsBot", layout="wide")

# Header Logo (replace with your own logo URL or local file)
st.markdown(
    """
    <div style="text-align: center;">
        <img src="https://shizenenergy.net/wp-content/uploads/2022/11/logo_shizen_black.png" alt="Shizen Energy" width="200"/>
    </div>
    """,
    unsafe_allow_html=True
)

# Greeting
st.markdown("<h1 style='text-align: center;'>👋 Konnichiwa Shizenian, let's get you up to speed</h1>", unsafe_allow_html=True)
st.markdown("")

# Filter input
filter_keyword = st.text_input("🔎 Optional: Filter results by topic/keyword", "")

# Search button
if st.button("📰 Scrape Now"):
    all_articles = []

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

    def scrape_and_summarize(url):
        try:
            res = requests.get(url, timeout=10)
            soup = BeautifulSoup(res.text, "html.parser")
            text = " ".join(p.get_text() for p in soup.find_all("p"))
            prompt = f"Summarize this Malaysian news article in 3 bullet points:\n\n{text}"
            summary = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}]
            )
            return summary['choices'][0]['message']['content'].strip()
        except Exception as e:
            return f"Could not summarize: {e}"

    with st.spinner("Scraping news and generating summaries..."):
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

                summary = scrape_and_summarize(link)
                all_articles.append({
                    "datetime": parsed_date,
                    "title": title,
                    "link": link,
                    "summary": summary
                })

    # Sort results by datetime
    sorted_articles = sorted(all_articles, key=lambda x: x["datetime"], reverse=True)

    # Optional filter
    if filter_keyword:
        sorted_articles = [
            a for a in sorted_articles
            if filter_keyword.lower() in a["title"].lower() or filter_keyword.lower() in a["summary"].lower()
        ]

    # Display results
    for article in sorted_articles:
        st.markdown(f"### [{article['title']}]({article['link']})")
        st.markdown(f"<small>{article['datetime'].strftime('%Y-%m-%d %H:%M')}</small>", unsafe_allow_html=True)
        st.markdown(f"<div style='font-size: 14px; color: gray;'>{article['summary']}</div>", unsafe_allow_html=True)
        st.markdown("---")
