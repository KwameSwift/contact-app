import sendgrid
import os
from config.keys import SENDGRID_API_KEY, SENDER_EMAIL
from sendgrid.helpers.mail import Mail, Email, To, Content

def send_email(recipient, sub, message):
    sg = sendgrid.SendGridAPIClient(api_key=SENDGRID_API_KEY)
    from_email = Email(SENDER_EMAIL)  # Change to your verified sender
    to_email = To(recipient)  # Change to your recipient
    subject = sub
    content = Content("text/plain", message)
    mail = Mail(from_email, to_email, subject, content)

    # Get a JSON-ready representation of the Mail object
    mail_json = mail.get()

    # Send an HTTP POST request to /mail/send
    response = sg.client.mail.send.post(request_body=mail_json)
    print(response.status_code)
    print(response.headers)