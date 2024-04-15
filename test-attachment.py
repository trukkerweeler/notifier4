import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# Create the email message
msg = MIMEMultipart()
msg['From'] = 'your_email@example.com'
msg['To'] = 'recipient@example.com'
msg['Subject'] = 'Your Subject'

# Add the body of the email
body = 'Your email body text here.'
msg.attach(MIMEText(body, "plain"))

# Attach the files
attachment_paths = ["path_to_file/data.csv", "path_to_file/data.xlsx"]
for attachment_path in attachment_paths:
    attachment = open(attachment_path, "rb")
    part = MIMEBase("application", "octet-stream")
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', f'attachment; filename="{attachment_path}"')
    msg.attach(part)

# Send the email
server = smtplib.SMTP('smtp.example.com', 587)
server.starttls()
server.login('your_email@example.com', 'your_email_password')
server.sendmail('your_email@example.com', 'recipient@example.com', msg.as_string())
server.quit()


# import smtplib
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText
# from email.mime.base import MIMEBase
# from email import encoders

# # Create the email message
# msg = MIMEMultipart()
# msg['From'] = 'your_email@example.com'
# msg['To'] = 'recipient@example.com'
# msg['Subject'] = 'Your Subject'

# # Add the body of the email
# body = 'Your email body text here.'
# msg.attach(MIMEText(body, "plain"))

# # Attach the files
# attachment_paths = ["path_to_file/data.csv", "path_to_file/data.xlsx"]
# for attachment_path in attachment_paths:
#     attachment = open(attachment_path, "rb")
#     part = MIMEBase("application", "octet-stream")
#     part.set_payload((attachment).read())
#     encoders.encode_base64(part)
#     part.add_header('Content-Disposition', f'attachment; filename="{attachment_path}"')
#     msg.attach(part)

# # Send the email
# server = smtplib.SMTP('smtp.example.com', 587)
# server.starttls()
# server.login('your_email@example.com', 'your_email_password')
# server.sendmail('your_email@example.com', 'recipient@example.com', msg.as_string())
# server.quit()
