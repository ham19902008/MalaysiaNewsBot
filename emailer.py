import yagmail
import os
from dotenv import load_dotenv

load_dotenv()
EMAIL = os.getenv("EMAIL_USER")
PASSWORD = os.getenv("EMAIL_PASSWORD")

yag = yagmail.SMTP(EMAIL, PASSWORD)

def send_email(articles):
    if not articles:
        return

    contents = ["Here are the new articles:\n"]
    for art in articles:
        contents.append(f"{art['date']} - {art['title']}\n{art['link']}\n")

    yag.send(to=EMAIL, subject="Malaysia News Alert", contents=contents)
