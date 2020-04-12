from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask_mail import Message

from flask import current_app as app


def send_email(to, subject, template):
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Link"
    msg['From'] = app.config['MAIL_DEFAULT_SENDER']
    msg['To'] = to
    msg.attach(MIMEText(template, 'html'))
    # # Python code to illustrate Sending mail from
    # # your Gmail account
    import smtplib

    # creates SMTP session
    s = smtplib.SMTP(app.config['MAIL_SERVER'], app.config['MAIL_PORT'])

    # start TLS for security
    s.starttls()

    # Authentication
    s.login(app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])

    # sending the mail
    # s.send_message(app.config['MAIL_DEFAULT_SENDER'], to, template)
    s.sendmail(app.config['MAIL_SERVER'], to, msg.as_string())

    # terminating the session
    s.quit()
