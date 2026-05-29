import smtplib
import os
from datetime import date
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


today = date.today().strftime("%B %d, %Y")

def render_section(title, color, articles):
    html = f'''
    <div style="margin-bottom:32px;">
        <div style="background:{color};padding:12px 20px;border-radius:6px 6px 0 0;">
            <h2 style="margin:0;color:#ffffff;font-size:16px;font-weight:700;letter-spacing:1px;text-transform:uppercase;">{title}</h2>
        </div>
        <div style="border:1px solid #e2e8f0;border-top:none;border-radius:0 0 6px 6px;overflow:hidden;">
    '''
    for i, article in enumerate(articles):
        bg = "#ffffff" if i % 2 == 0 else "#f8fafc"
        html += f'''
            <div style="padding:16px 20px;background:{bg};border-bottom:1px solid #e2e8f0;">
                <a href="{article["link"]}" style="font-size:15px;font-weight:600;color:#1a202c;text-decoration:none;line-height:1.4;">{article["title"]}</a>
                <p style="margin:6px 0 0;font-size:13px;color:#718096;line-height:1.5;">{article["description"]}</p>
            </div>
        '''
    html += '</div></div>'
    return html

body = f'''
<!DOCTYPE html>
<html>
<body style="margin:0;padding:0;background:#f1f5f9;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;">
    <div style="max-width:640px;margin:0 auto;padding:24px 16px;">

        <div style="background:#1a202c;padding:28px 32px;border-radius:8px;margin-bottom:28px;">
            <h1 style="margin:0 0 4px;color:#ffffff;font-size:22px;font-weight:700;">Morning Briefing</h1>
            <p style="margin:0;color:#a0aec0;font-size:13px;">{today}</p>
        </div>

        {render_section("World & Geopolitics", "#2b6cb0", articles_glob)}
        {render_section("Lebanon", "#c53030", articles_leb)}
        {render_section("Tech & AI", "#276749", articles_tech)}

        <p style="text-align:center;color:#a0aec0;font-size:12px;margin-top:8px;">Delivered daily at 9am</p>
    </div>
</body>
</html>
'''

send_email("Your Morning Briefing", body)