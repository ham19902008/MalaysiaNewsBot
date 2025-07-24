import streamlit as st
from scraper import scrape_news
from datetime import datetime

# Page config
st.set_page_config(page_title="Shizen Malaysia NewsBot", layout="wide")

# Add logo (your image file must be in GitHub repo, or use raw image URL)
st.image("https://raw.githubusercontent.com/ham19902008/MalaysiaNewsBot/main/logo.webp", width=120)


# Header
st.markdown("### 👋 Konnichiwa Shizenian, let's get you up to speed")

# Scrape and show news
if st.button("Scrape Now"):
    results = scrape_news()
    
    # Sort by newest (assumes proper ISO date format or sorts well lexicographically)
    results = sorted(results, key=lambda x: x["date"], reverse=True)

    if results:
        for article in results:
            st.markdown(f"#### {article['title']}")
            st.markdown(f"📅 {article['date']}")
            st.markdown(f"[🔗 Read more]({article['link']})\n---")
    else:
        st.info("No articles found.")
