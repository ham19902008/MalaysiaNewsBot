import requests
from bs4 import BeautifulSoup
import openai
from datetime import datetime

# --- Your OpenAI API Key ---
openai.api_key = "YOUR_OPENAI_API_KEY"  # Replace with your actual key

# --- NEWS SOURCES (can expand) ---
NEWS_SOURCES = [
    "https://www.theedgemarkets.com/taxonomy/term/6800",  # Energy articles on The Edge
]

# --- CLEAN DATE FORMAT ---
def format_date(raw_datetime):
    try:
        dt = datetime.strptime(raw_datetime, "%Y-%m-%dT%H:%M:%S%z")
        return dt.strftime("%d/%m/%Y, %I:%M %p, %z UTC")
    except Exception:
        return raw_datetime  # fallback

# --- GENERATE SUMMARY ---
def generate_summary(text):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Summarize the news article in 2–3 short sentences."},
                {"role": "user", "content": text},
            ],
            temperature=0.7,
            max_tokens=100,
        )
        return response.choices[0].message["content"].strip()
    except Exception as e:
        return "Summary not available."

# --- SCRAPER FUNCTION ---
def scrape_news():
    articles = []

    for source_url in NEWS_SOURCES:
        try:
            response = requests.get(source_url, timeout=10)
            soup = BeautifulSoup(response.text, "html.parser")

            for article in soup.select(".article"):
                title_tag = article.select_one("h2 a")
                date_tag = article.select_one("time")
                link = title_tag["href"] if title_tag else None
                title = title_tag.text.strip() if title_tag else "No title"
                date_raw = date_tag["datetime"] if date_tag and "datetime" in date_tag.attrs else ""
                formatted_date = format_date(date_raw)
                url = link if link and link.startswith("http") else "https://www.theedgemarkets.com" + link

                # Attempt to fetch and summarize the article content
                summary = ""
                try:
                    article_resp = requests.get(url, timeout=10)
                    article_soup = BeautifulSoup(article_resp.text, "html.parser")
                    paragraphs = article_soup.select("div.field--name-body p")
                    full_text = " ".join(p.get_text() for p in paragraphs[:5])  # Grab only first few paragraphs
                    summary = generate_summary(full_text)
                except:
                    summary = "Summary not available."

                articles.append({
                    "title": title,
                    "date": formatted_date,
                    "url": url,
                    "summary": summary
                })

        except Exception as e:
            print(f"Error scraping {source_url}: {e}")

    return articles
