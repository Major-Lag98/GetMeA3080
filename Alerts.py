import smtplib
from email.message import EmailMessage


def text_alert(body, to):
    msg = EmailMessage()
    msg.set_content(body)
    msg['to'] = to

    user = "email@email.com"  # Email for alerts to come from
    msg['from'] = user
    password = "appPassword"   # App password provided by google
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(user, password)
    server.send_message(msg)
    print(f"Sent message: {body}")
    server.quit()
