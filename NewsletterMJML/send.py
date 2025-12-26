import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate, make_msgid, formataddr
from email.header import Header

from bs4 import BeautifulSoup as BS

from rich.console import Console
from rich.prompt import Prompt

import os
import sys
from dotenv import load_dotenv
import json
import time

import argparse

from createStaticPage import prepare_web_html

console = Console()
load_dotenv()

EMAIL = os.getenv('EMAIL')
EMAIL_PWD = os.getenv('EMAIL_PWD')

if not EMAIL:
    raise ValueError("EMAIL not found. Please set EMAIL in your .env file.")

if not EMAIL_PWD:
    raise ValueError("EMAIL_PWD not found. Please set EMAIL_PWD in your .env file.")

Translations = {
    'fr':{
        'plain_text':'Bonjour,\n\nCe message contient du contenu HTML. Veuillez l\'ouvrir dans une application de messagerie plus moderne ou ouvrez le lien suivant dans un navigateur internet: {{ARTICLE_URL}}'
    },
    'de':{
        'plain_text':'Hallo,\n\nDiese Nachricht enthält HTML Inhalte. Bitte öffnen Sie diese E-Mail in einer modernen E-Mail Anwendung oder öffnen Sie folgenden Link mit einem Browser: {{ARTICLE_URL}}'
    },
    'en':{
        'plain_text':'Hello,\n\nThis message contains HTML content. Please view it in a modern email client or open the following URL with a browser: {{ARTICLE_URL}}'
    }
}

languages = ['fr', 'de', 'en']

def load_recipients(json_path):
    """Load recipients from JSON file."""
    if not os.path.isfile(json_path):
        console.print(f"[bold red]JSON file not found: {json_path}[/bold red]")
        sys.exit(1)
    with open(json_path, 'r') as file:
        email_data = json.load(file)
    return email_data


class email_handler:
    """This class handles the sending of emails.
    """
    def __init__(self, lang:str, path:str, article_name:str, domain: str = "https://cyprieninperu.netlify.app/", newsletter_url: str = "https://cyprieninperu.netlify.app/newsletters/", check_mail: bool = False):
        """Intializes the email_handler class.

        Args:
            lang (str): The language abbreviation of this e-mail for correct rendering of the e-mail.
            path (str): The path of the html template for this e-mail.
            domain (str): The base url to be used to access the website at. Should be the root! Defaults to: "https://cyprieninperu.netlify.app/"
        """
        self.smtp_server = '127.0.0.1'
        self.smtp_port = 1026  # Use Bridge SMTP port and local server
        self.smtp_user = EMAIL
        self.smtp_password = EMAIL_PWD
        self.display_name = ""
        self.sender_email = "Cyprieninperu@pm.me"
        if lang not in languages:
            raise Exception('Language undefined')
        self.lang = lang
        if not os.path.isfile(path) and path.split('.')[:-1] != 'html':
            raise Exception(f'Unknown file: {path}')
        self.path = path
        self.check_mail = check_mail
        self.newsletter_url = newsletter_url
        self.domain = domain
        self.article_name = article_name

    def html_content(self, name, mail) -> str:
        with open(self.path, "r", encoding="utf-8") as f:
            html = f.read()
        html = html.replace('{{NAME}}', name) # Name of the reciever
        html = html.replace('{{BASE_URL}}', self.domain) # The domain of the website, default: "https://cyprieninperu.netlify.app/"
        html = html.replace('{{FILENAME}}', self.path.split("/")[-1]) #Name of the Newsletters HTML file in content
        html = html.replace('{{ARTICLE_SLUG}}', self.article_name) # The articles Slug for utm_campaign and the url
        return html.replace('{{MAIL}}', mail) # The recievers e-mail

    def send(self, content: str, recipient_email: str = "cyprieninperu@pm.me"):
        msg = MIMEMultipart("alternative")
        msg["From"] = formataddr((self.display_name, self.sender_email))
        msg["To"] = recipient_email
        soup = BS(content, 'html.parser')
        title_elem = soup.find('title')
        title_text = title_elem.string.strip() if title_elem and title_elem.string else "Newsletter"
        msg["Subject"] = Header(title_text, 'utf-8')
        msg["Date"] = formatdate(localtime=True)
        msg["Message-ID"] = make_msgid(domain="pm.me")

        if self.check_mail:
            if Prompt.ask(f"[bold {"yellow"}]GLOBAL[/bold {"yellow"}] › You are sending {msg}. \nContinue?", default="y").lower() != "y":
                console.print("[bold red]Cancelled by user[/bold red]")
                exit()

        plain_text = self.plain_text()
        msg.attach(MIMEText(plain_text, "plain", "utf-8"))
        msg.attach(MIMEText(content, "html", "utf-8"))
        try:
            with smtplib.SMTP_SSL(self.smtp_server, self.smtp_port) as server:
                server.login(self.smtp_user, self.smtp_password)
                server.send_message(msg) # ATTENTION --- DELETE # TO ACTUALLY SEND
                console.log(f'E-Mail sent successfully to {msg["To"]}')
        except Exception as e:
            print(f"Error: {e}")
    
    def plain_text(self):
        return Translations[self.lang]['plain_text'].replace('{{ARTICLE_URL}}', f'{self.newsletter_url}{self.path.split('/')[-1]}')

def main():
    parser = argparse.ArgumentParser(description="Send HTML newsletter emails")
    parser.add_argument("language", choices=languages, help="Language (fr, de, en)")
    parser.add_argument("html_path", help="Path to HTML template")
    parser.add_argument("article_slug", help="The articles slug.")
    parser.add_argument("-j", "--json", default="newslettermjml/.emails.json", help="Path to email JSON (default: newslettermjml/.emails.json)")
    parser.add_argument("-g", "--generate", action='store_true', help="After having sent the emails, it will generate a website friendly html.")
    
    args = parser.parse_args()
    console.log(args.generate)
    # Validate HTML path
    if not os.path.isfile(args.html_path):
        console.print(f"[bold red]HTML file not found: {args.html_path}[/bold red]")
        sys.exit(1)
    
    #Validate article slug
    if not os.path.isdir(f'output/{args.article_slug}'):
        console.print(f"[bold red]Article file not found: {args.article_slug}[/bold red]")
        sys.exit(1)
    
    # Load recipients
    email_data = load_recipients(args.json)
    mails = email_data.get(args.language, {})
    
    if not mails:
        console.print(f"[bold red]No emails found for language: {args.language}[/bold red]")
        sys.exit(1)
    
    # Initialize email handler
    handler = email_handler(args.language, args.html_path, args.article_slug)

    for count, i in enumerate(mails.items()):
        handler.check_mail=True if count == 0 else False
        name, address = i
        handler.send(handler.html_content(name, address), address)
        time.sleep(2) # Prevent blocking because of too many requests
    
    if args.generate:
        prepare_web_html(args.html_path, args.html_path.split("/")[-1], args.article_slug)
        console.log(f"Newsletter has been generated for website: {args.html_path.split("/")[-1]}")

if __name__ == '__main__':
    main()