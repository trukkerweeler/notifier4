from email.message import EmailMessage

content = "<p>This is a paragraph!</p>"
msg = EmailMessage()
msg.set_content(content, subtype='html')
msg['Subject'] = "Subject"
msg['From'] = "SENDER"
msg['To'] = "RECEIVER"


