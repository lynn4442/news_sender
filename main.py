import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
from newsapi import NewsApiClient

load_dotenv() # this will read the .env file so python is aware that the env file exists
email = os.getenv("email") # looks up the env var "email" and return the value as  string
app_pass = os.getenv("app_pass")
news_api_key = os.getenv("news_api_key")

newsapi = NewsApiClient(api_key=news_api_key)
response_pol = newsapi.get_everything(q="Lebanon Middle East", language="en", page_size=8, sort_by="publishedAt")
response_tech = newsapi.get_everything(q="technology OR artificial intelligence OR cybersecurity OR software OR startup", language="en", page_size=8, sort_by="publishedAt")


def send_email(subject, body) : 
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = email
    msg["To"] = email
    msg.attach(MIMEText(body, "html"))

    with smtplib.SMTP("smtp.gmail.com", 587) as server :
        server.starttls()
        server.login(email, app_pass)
        server.sendmail(email, email, msg.as_string())

# political_loop
articles_pol = []
for item in response_pol["articles"]:
    articles_pol.append(
        {
            "title": item["title"],
            "description": item["description"],
            "link": item["url"]
        }
    ) 
print(articles_pol)

# tech_loop
articles_tech = []
for item in response_tech["articles"]:
    articles_tech.append(
        {
            "title": item["title"],
            "description": item["description"],
            "link": item["url"]
        }
    ) 
print(articles_tech)

body = "<h2>Lebanon & Geopolitics</h2><ul>"
for article in articles_pol :
    body += f'<li><a href="{article["link"]}">{article["title"]}</a><br>{article["description"]}</li>'

body += "</ul><h2>Tech & AI</h2><ul>"
for article in articles_tech :
    body += f'<li><a href="{article["link"]}">{article["title"]}</a><br>{article["description"]}</li>'

send_email("Your Morning Briefing", body)