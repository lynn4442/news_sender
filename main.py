import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
from newsapi import NewsApiClient

load_dotenv()
# this will read the .env file so python is aware that the env file exists
email = os.getenv("EMAIL")
# looks up the env var "email" and return the value as  string
app_pass = os.getenv("APP_PASS")
news_api_key = os.getenv("NEWS_API_KEY")

newsapi = NewsApiClient(api_key=news_api_key)
response_glob = newsapi.get_everything(q="geopolitics OR world politics OR international relations", language="en", page_size=8, sort_by="publishedAt")
response_leb = newsapi.get_everything(q="Lebanon OR Hezbollah OR Israeli strikes Lebanon", language="en", page_size=8, sort_by="publishedAt")
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
articles_glob = []
for item in response_glob["articles"]:
    articles_glob.append(
        {
            "title": item["title"],
            "description": item["description"],
            "link": item["url"]
        }
    ) 
# print(articles_glob)

# lebanon_loop
articles_leb = []
for item in response_leb["articles"]:
    articles_leb.append(
        {
            "title": item["title"],
            "description": item["description"],
            "link": item["url"]
        }
    ) 
# print(articles_leb)

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
# print(articles_tech)


body = "<h2>World & Geopolitics</h2><ul>"
for article in articles_glob :
    body += f'<li><a href="{article["link"]}">{article["title"]}</a><br>{article["description"]}</li>'

body += "</ul><h2>Lebanon News</h2><ul>"
for article in articles_leb :
    body += f'<li><a href="{article["link"]}">{article["title"]}</a><br>{article["description"]}</li>'

body += "</ul><h2>Tech & AI</h2><ul>"
for article in articles_tech :
    body += f'<li><a href="{article["link"]}">{article["title"]}</a><br>{article["description"]}</li>'

body += "</ul>" 

send_email("Your Morning Briefing", body)