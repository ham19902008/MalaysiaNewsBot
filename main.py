import streamlit as st
from scraper import scrape_news

st.set_page_config(page_title="Malaysia NewsBot", layout="wide")
st.title("🇲🇾 Malaysia Energy News Monitor")

if st.button("Scrape Now"):
    results = scrape_news()
    if results:
        for article in results:
            st.markdown(f"**{article['title']}**  \n{article['date']}  \n[Read more]({article['link']})\n---")
    else:
        st.write("No articles found.")
