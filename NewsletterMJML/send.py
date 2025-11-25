import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate, make_msgid, formataddr
import os
from dotenv import load_dotenv

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

class email_handler:
    """This class handles the sending of emails.
    """
    def __init__(self, lang:str, path:str, recipients: str, base_url: str = "https://cyprieninperu.netlify.app/"):
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
        if lang not in ['fr', 'de', 'en']:
            raise Exception('Language undefined')
        self.lang = lang
        if not os.path.isfile(path):
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
    input()
    email = email_handler("fr", "/Users/cyprien/Coding/Snakes/StaticSiteGenerator", "example@icloud.com,example@gmail.com")
    email.send(email.html_content())