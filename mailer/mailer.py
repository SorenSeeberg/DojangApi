from typing import List
import smtplib
import config


def _build_email(sent_from: str, to: List[str], subject: str, body: str) -> str:
    return f'From: {sent_from}\n' \
           f'To: {"".join(to)}\n' \
           f'Subject: {subject}\n' \
           f'\n' \
           f'{body}'


def _send_email(target_email: str, email_content: str):
    try:
        server_ssl = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server_ssl.ehlo()
        server_ssl.login(config.MAIL_SENDER, config.MAIL_KEY)
        server_ssl.sendmail(config.MAIL_SENDER, target_email, email_content)
        print(f'Email sent to {target_email}')
    except:
        print('Something went wrong...')


def send_activation_mail(target_email: str, activation_token: str):

    subject = 'Velkommen til DOJANG. Aktiver din profil!'

    body = f'' \
        f'Hej {target_email},\n\n' \
        f'Velkommen til DOJANG, en Taekwondo teoriapp som virker!\n\n' \
        f'Aktiver din profil med dette link\n' \
        f'{config.SITE_URL}/users/activate/{activation_token}\n\n' \
        f'Med venlig hilsen,\n' \
        f'Grand Master Kwon'

    content = _build_email(config.MAIL_SENDER, [target_email], subject, body)

    _send_email(target_email, content)
