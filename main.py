import streamlit as st
import pandas as pd
import openai
from serpapi import GoogleSearch  # Correct import — requires google-search-results
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

# Set OpenAI key
openai.api_key = OPENAI_API_KEY

# Suggested keywords
suggested_keywords = [
    "renewables Malaysia",
    "solar",
    "energy transition",
    "green hydrogen",
    "Tenaga Nasional Berhad",
    "solar farm",
    "Net Energy Metering Malaysia"
]

# Header
st.markdown("<h1 style='text-align: center; font-size: 42px;'>Konnichiwa Shizenian ☀️</h1>", unsafe_allow_html=True)

# Sidebar
st.sidebar.title("Search Controls")
keyword = st.sidebar.text_input("Enter keyword to search", "")
filter_keyword = st.sidebar.text_input("Filter results by topic/keyword", "")
scrape_now = st.sidebar.button("🔍 Scrape Now")

# Display suggestions
if keyword == "":
    st.subheader("Suggested Keywords:")
    for k in suggested_keywords:
        st.write(f"- {k}")

# Search function
def google_search(query):
    params = {
        "q": query,
        "engine": "google",
        "api_key": SERPAPI_API_KEY,
        "num": 5,
        "hl": "en",
        "gl": "my"
    }
    search = GoogleSearch(params)
    results = search.get_dict()
    return results.get("organic_results", [])

# Scrape and summarize
def scrape_and_summarize(url):
    try:
        res = requests.get(url, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")
        paragraphs = soup.find_all("p")
        text = " ".join([p.get_text() for p in paragraphs])
        prompt = f"Summarize this news article in 3 bullet points:\n\n{text}"
        summary = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return summary['choices'][0]['message']['content'].strip()
    except Exception as e:
        return f"Could not summarize: {e}"

# Main logic
if scrape_now and keyword:
    st.info(f"Searching for: **{keyword}**")
    results = google_search(keyword)

    if not results:
        st.warning("No results found.")
    else:
        articles = []
        for result in results:
            title = result.get("title")
            link = result.get("link")
            date_str = result.get("date") or result.get("snippet", "")[:50]
            try:
                parsed_date = parser.parse(date_str, fuzzy=True)
            except:
                parsed_date = datetime.now()
            summary = scrape_and_summarize(link)
            articles.append({
                "datetime": parsed_date,
                "title": title,
                "link": link,
                "summary": summary
            })

        # Sort by datetime descending
        sorted_articles = sorted(articles, key=lambda x: x["datetime"], reverse=True)

        # Filter
        if filter_keyword:
            sorted_articles = [a for a in sorted_articles if filter_keyword.lower() in a["title"].lower() or filter_keyword.lower() in a["summary"].lower()]

        # Display
        for a in sorted_articles:
            st.markdown(f"### [{a['title']}]({a['link']})")
            st.markdown(f"<small>{a['datetime'].strftime('%Y-%m-%d %H:%M')}</small>", unsafe_allow_html=True)
            st.markdown(f"<div style='font-size: 14px; color: gray;'>{a['summary']}</div>", unsafe_allow_html=True)
            st.markdown("---")
