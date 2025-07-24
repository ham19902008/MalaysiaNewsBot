import streamlit as st
from scraper import scrape_news
from summarizer import summarize
from datetime import datetime

st.set_page_config(page_title="Shizenian NewsBot", layout="wide")

# HEADER with logo and greeting
st.markdown("""
<div style='text-align: center;'>
    <img src='https://raw.githubusercontent.com/ham19902008/MalaysiaNewsBot/main/logo.webp' width='120'/>
    <h1 style='font-size: 38px; margin-top: 10px;'>👋 Konnichiwa Shizenian, let's get you up to speed</h1>
</div>
""", unsafe_allow_html=True)

# SEARCH BAR
search_query = st.text_input("🔍 Search articles by keyword:", "")

# CUSTOM STYLED SCRAPE BUTTON
scrape_col = st.columns([4, 1, 4])[1]
with scrape_col:
    scrape_now = st.button("Scrape Now", use_container_width=True)

if scrape_now:
    articles = scrape_news()

    # Parse dates correctly
    def parse_date(date_str):
        try:
            return datetime.strptime(date_str, "%m/%d/%Y, %I:%M %p, %z")
        except:
            return datetime.min

    # Sort by newest first
    articles.sort(key=lambda x: parse_date(x["date"]), reverse=True)

    # Filter articles based on search
    if search_query:
        articles = [a for a in articles if search_query.lower() in a["title"].lower()]

    if articles:
        for article in articles:
            st.markdown(f"<h3 style='margin-bottom: 0;'>{article['title']}</h3>", unsafe_allow_html=True)
            st.markdown(f"<span style='color: grey;'>🗓️ {article['date']}</span>", unsafe_allow_html=True)

            # Show summary (OpenAI)
            summary = summarize(article["title"])
            st.markdown(f"<p style='font-size: 14px; color: #444;'>{summary}</p>", unsafe_allow_html=True)

            st.markdown(f"<a href='{article['link']}' target='_blank' style='font-size: 13px;'>🔗 Read more</a>", unsafe_allow_html=True)
            st.markdown("<hr>", unsafe_allow_html=True)
    else:
        st.warning("No articles found.")
