import streamlit as st
from scraper import scrape_news
from datetime import datetime

# Page config
st.set_page_config(page_title="Shizenian NewsBot", layout="wide")

# Centered logo and header
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image("https://raw.githubusercontent.com/ham19902008/MalaysiaNewsBot/main/logo.webp", width=120)
    st.markdown("### 👋 Konnichiwa Shizenian, let's get you up to speed")

# Scrape button
if st.button("Scrape Now"):
    results = scrape_news()

    def parse_date(date_str):
        try:
            return datetime.strptime(date_str, "%m/%d/%Y, %I:%M %p, %z")
        except:
            return datetime.min  # fallback if date format fails

    # Sort articles by date (most recent first)
    results = sorted(results, key=lambda x: parse_date(x["date"]), reverse=True)

    if results:
        for article in results:
            st.markdown(f"### {article['title']}")
            st.markdown(f"🗓️ {article['date']}")
            st.markdown(f"<span style='font-size:14px'><a href='{article['link']}' target='_blank'>🔗 Read more</a></span>", unsafe_allow_html=True)
            st.markdown("---")
    else:
        st.info("No articles found.")
