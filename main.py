import streamlit as st
from scraper import scrape_news
from datetime import datetime
from dateutil import parser
from PIL import Image

# --- PAGE CONFIG ---
st.set_page_config(page_title="Malaysia Energy News", layout="centered")

# --- CUSTOM STYLING ---
shizen_blue = "#0072BC"
st.markdown(
    f"""
    <style>
    .headline {{
        font-size: 28px;
        font-weight: bold;
        margin-top: 30px;
        margin-bottom: 10px;
    }}
    .summary {{
        font-size: 16px;
        color: #555;
        margin-bottom: 20px;
    }}
    .scrape-button > button {{
        background-color: {shizen_blue} !important;
        color: white !important;
        border-radius: 8px;
        padding: 0.5em 1em;
        font-size: 16px;
    }}
    .header-container {{
        text-align: center;
    }}
    .header-container h1 {{
        font-size: 36px;
        margin-top: 20px;
    }}
    .logo {{
        width: 120px;
        margin: 0 auto;
    }}
    .search-bar input {{
        width: 100%;
        padding: 0.5em;
        font-size: 16px;
        border-radius: 8px;
        border: 1px solid #ccc;
        margin-bottom: 20px;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# --- HEADER ---
with st.container():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        logo = Image.open("logo.webp")
        st.image(logo, use_column_width=False)
        st.markdown('<div class="header-container"><h1>👋 Konnichiwa Shizenian, let\'s get you up to speed</h1></div>', unsafe_allow_html=True)

# --- SCRAPE BUTTON ---
if st.button("Scrape Now", key="scrape", help="Fetch latest news"):
    st.session_state["articles"] = scrape_news()

# --- FETCH DATA ---
if "articles" not in st.session_state:
    st.session_state["articles"] = scrape_news()

articles = st.session_state["articles"]

# --- FILTER / SEARCH BAR ---
search_term = st.text_input("Search articles by keyword", "").strip().lower()
if search_term:
    articles = [a for a in articles if search_term in a["title"].lower() or search_term in a.get("summary", "").lower()]

# --- DATE PARSING FIX ---
def parse_date(date_str):
    try:
        clean_str = date_str.replace("UTC", "").strip()
        return parser.parse(clean_str)
    except Exception:
        return datetime.min  # fallback if parsing fails

# --- SORT BY DATE DESCENDING ---
articles.sort(key=lambda x: parse_date(x["date"]), reverse=True)

# --- DISPLAY ARTICLES ---
for article in articles:
    st.markdown(f"<div class='headline'>{article['title']}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='summary'>{article['summary']}</div>", unsafe_allow_html=True)
    st.write(f"📅 {article['date']}")
    st.markdown(f"🔗 [Read more]({article['url']})")
