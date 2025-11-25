import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate, make_msgid, formataddr

from rich.console import Console
from rich.prompt import Prompt
from rich.text import Text

import os
from dotenv import load_dotenv
import json

import time

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
        'plain_text':'Hallo,\n\nDiese Nachricht enthält HTML Inhalte. Bitte öffnen Sie diese E-Mail in einer modernen E-Mail Anwendung oder öffnen Sie folgenden Link in einem Browser: {{ARTICLE_URL}}'
    },
    'en':{
        'plain_text':'Hello,\n\nThis message contains HTML content. Please view it in a modern email client or open the following URL with a browser: {{ARTICLE_URL}}'
    }
}

languages = ['fr', 'de', 'en']

def __input(prompt_text, default="", style="cyan"):
    """Enhanced global input with consistent styling."""
    return Prompt.ask(f"[bold {style}]GLOBAL[/bold {style}] › {prompt_text}", default=default)

def main():
    lang = __input(
            "Please select a language (fr, de, en)\nEnter your choice:",
            style="yellow"
        ).lower()
    while lang not in languages:
        console.print("[bold red]Invalid option! Please try again.[/bold red]")
        lang = __input(
            "Please select a language (fr, de, en)\nEnter your choice:",
            style="yellow"
        ).lower()
    
    path = __input(
            "Please enter a path for your html (MJML) template.\nEnter your choice:",
            style="yellow"
        )
    while path.split('.')[:-1] != 'html' and not os.path.isfile(path):
        console.print("[bold red]Invalid option! Check the path and file type (HTML). Please try again.[/bold red]")
        path = __input(
            "Please enter a path for your html (MJML) template.\nEnter your choice:",
            style="yellow"
        )
    
    addresses = __input("Please enter a path your e-mail address json.\nEnter your choice:", style="yellow", default="newslettermjml/.emails.json")
    while addresses.split('.')[:-1] != 'json' and not os.path.isfile(addresses):
        console.print("[bold red]Invalid option! Check the path and file type (json). Please try again.[/bold red]")
        addresses = __input("Please enter a path your e-mail address json.\nEnter your choice:", style="yellow", default="newslettermjml/.emails.json")

    with open(addresses, 'r') as file:
        email_data = json.load(file)

    mails = email_data.get(lang, [])

    for i in mails:
        mail = email_handler(lang, path)
        mail.send(mail.html_content(), i)
        time.sleep(2) # Prevent blocking because of too many requests


class email_handler:
    """This class handles the sending of emails.
    """
    def __init__(self, lang:str, path:str, base_url: str = "https://cyprieninperu.netlify.app/", recipients: str = None):
        """Intializes the email_handler class.

        Args:
            lang (str): The language abbreviation of this e-mail for correct rendering of the e-mail.
            path (str): The path of the html template for this e-mail.
            recipients (str): A str containing e-mails separated by commas, that will be added as bcc to the sent email.
            base_url (str): The base url to be used to access the website at. Should be the root!
        """
        self.smtp_server = '127.0.0.1'
        self.smtp_port = 1026  # Use Bridge SMTP port and local server
        self.smtp_user = EMAIL
        self.smtp_password = EMAIL_PWD
        self.display_name = ""
        self.sender_email = "Cyprieninperu@pm.me"
        self.bcc = recipients
        if lang not in languages:
            raise Exception('Language undefined')
        self.lang = lang
        if not os.path.isfile(path) and path.split('.')[:-1] != 'html':
            raise Exception(f'Unknown file: {path}')
        self.path = path

    def html_content(self) -> str:
        with open(self.path, "r", encoding="utf-8") as f:
            html = f.read()
        return html #Add Jinja2 Syntax Support

    def send(self, content: str, recipient_email: str = "cyprieninperu@pm.me"):
        msg = MIMEMultipart("alternative")
        msg["From"] = formataddr((self.display_name, self.sender_email))
        msg["To"] = recipient_email
        if self.bcc:
            msg["Bcc"] = self.bcc
        msg["Subject"] = "Cyprien au Pérou - Newsletter du Lundi, 24 Novembre 2025"
        msg["Date"] = formatdate(localtime=True)
        msg["Message-ID"] = make_msgid(domain="pm.me")

        plain_text = "Hello,\n\nThis message contains HTML content. Please view it in a modern email client or open the following URL with a browser: " # URL should represent Netlify with the e-mail html.
        msg.attach(MIMEText(plain_text, "plain", "utf-8"))
        msg.attach(MIMEText(content, "html", "utf-8"))
        try:
            with smtplib.SMTP_SSL(self.smtp_server, self.smtp_port) as server:
                server.login(self.smtp_user, self.smtp_password)
                #server.send_message(msg)
        except Exception as e:
            print(f"Error: {e}")

if __name__ == '__main__':
    main()