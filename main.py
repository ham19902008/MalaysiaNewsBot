import streamlit as st
import requests
from bs4 import BeautifulSoup
import openai
from datetime import datetime
from dateutil import parser
import os
from serpapi import GoogleSearch
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
serpapi_key = os.getenv("SERPAPI_API_KEY")

# -------------------- STYLING --------------------
st.image("logo.webp", width=200)

st.markdown(
    "<h1 style='text-align: center; font-size: 36px;'>👋 Konnichiwa Shizenian, let's get you up to speed</h1>",
    unsafe_allow_html=True
)

# -------------------- FUNCTION TO SCRAPE ARTICLES --------------------
def search_google_news(query, serpapi_key):
    params = {
        "q": query,
        "tbm": "nws",
        "api_key": serpapi_key,
        "engine": "google",
        "num": 10
    }
    search = GoogleSearch(params)
    results = search.get_dict()
    return results.get("news_results", [])

def get_article_summary(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0"
        }
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        paragraphs = soup.find_all("p")
        text = " ".join([para.get_text() for para in paragraphs])

        # Limit to first 2000 characters for OpenAI
        prompt = f"Summarize this article in 2-3 short sentences:\n\n{text[:2000]}"
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=100
        )
        return response["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return "Summary not available."

# -------------------- SCRAPER TRIGGER --------------------
if st.button("Scrape Now"):
    with st.spinner("Scraping news..."):
        topics = [
            "renewables Malaysia",
            "Solar Malaysia",
            "Tenaga Nasional Berhad",
            "Green energy Malaysia",
            "Malaysia electricity transition",
            "sustainable energy Malaysia",
	    "Corporate renewable energy supply scheme",
	    "CRESS",
	    "Large scale solar",
	    "Data Center Malaysia",
	    "LSS",

        ]

        all_articles = []
        for topic in topics:
            results = search_google_news(topic, serpapi_key)
            for result in results:
                try:
                    article = {
                        "title": result["title"],
                        "link": result["link"],
                        "source": result.get("source"),
                        "published": parser.parse(result.get("date", "")),
                        "summary": get_article_summary(result["link"])
                    }
                    all_articles.append(article)
                except Exception:
                    continue

        # Sort by date (most recent first)
        all_articles.sort(key=lambda x: x["published"], reverse=True)

        st.success(f"Found {len(all_articles)} articles.")
        st.session_state["articles"] = all_articles

# -------------------- FILTER UI --------------------
if "articles" in st.session_state:
    keyword_filter = st.text_input("🔎 Filter by keyword")

    for article in st.session_state["articles"]:
        if keyword_filter.lower() in article["title"].lower():
            st.markdown(f"### [{article['title']}]({article['link']})")
            st.markdown(f"*Source: {article['source']} | Date: {article['published'].strftime('%Y-%m-%d %H:%M')}*")
            st.markdown(f"<span style='font-size: 14px;'>{article['summary']}</span>", unsafe_allow_html=True)
            st.markdown("---")
