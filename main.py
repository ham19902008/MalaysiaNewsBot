import streamlit as st
import requests
from bs4 import BeautifulSoup
import openai
import os
from dotenv import load_dotenv
from serpapi import GoogleSearch
from datetime import datetime
from dateutil import parser

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")

# Streamlit page settings
st.set_page_config(page_title="Malaysia Energy News", layout="centered")

# Branding and header
st.image("logo.webp", use_container_width=True)
st.markdown(
    "<h1 style='text-align: center; font-size: 36px;'>👋 Konnichiwa Shizenian, let's get you up to speed</h1>",
    unsafe_allow_html=True,
)

# Function to call OpenAI for summary
def summarize_text(text):
    prompt = f"Summarize this news article in 1-2 sentences:\n\n{text}"
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You summarize news articles briefly."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=100,
            temperature=0.5
        )
        summary = response['choices'][0]['message']['content'].strip()
        return summary
    except Exception as e:
        return f"Summary not available. Error: {str(e)}"

# Scraper function
def scrape_news():
    params = {
        "engine": "google",
        "q": "Malaysia energy news site:thestar.com.my OR site:nst.com.my OR site:bernama.com",
        "api_key": SERPAPI_API_KEY,
        "num": 10,
        "hl": "en"
    }

    search = GoogleSearch(params)
    results = search.get_dict()
    articles = results.get("organic_results", [])

    scraped = []
    for article in articles:
        title = article.get("title")
        link = article.get("link")
        date_str = article.get("date")
        snippet = article.get("snippet")

        try:
            published = parser.parse(date_str)
        except:
            published = datetime.now()

        summary = summarize_text(snippet)

        scraped.append({
            "title": title,
            "link": link,
            "published": published,
            "summary": summary
        })

    return sorted(scraped, key=lambda x: x["published"], reverse=True)

# Button logic
if st.button("Scrape Now", type="primary"):
    st.info("Scraping in progress...")
    try:
        scraped_articles = scrape_news()
        st.success(f"Scraped {len(scraped_articles)} articles.")
    except Exception as e:
        st.error(f"Error during scraping: {e}")
        scraped_articles = []
else:
    scraped_articles = []

# Display section
if scraped_articles:
    st.write("## 📰 Latest News")

    for article in scraped_articles:
        st.markdown(f"### {article['title']}")
        st.markdown(f"📅 {article['published'].strftime('%m/%d/%Y, %I:%M %p, %Z')}")
        st.markdown(f"<p style='font-size: 14px;'><a href='{article['link']}' target='_blank'>🔗 Read more</a></p>", unsafe_allow_html=True)
        st.markdown(f"<p style='font-size: 13px; color: gray;'>{article['summary']}</p>", unsafe_allow_html=True)
        st.markdown("---")
