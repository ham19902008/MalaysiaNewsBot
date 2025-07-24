import schedule
import time
from scraper import scrape_news
from emailer import send_email

last_sent = set()

def job():
    global last_sent
    new_articles = scrape_news()
    new_set = {a["title"] for a in new_articles}

    # Check if new articles arrived
    diff = new_set - last_sent
    if diff:
        send_email([a for a in new_articles if a["title"] in diff])
        last_sent = new_set

schedule.every(30).minutes.do(job)

print("NewsBot Scheduler Running...")

while True:
    schedule.run_pending()
    time.sleep(1)
