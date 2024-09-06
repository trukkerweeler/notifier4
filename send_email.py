import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email():
    sender_email = "quality@ci-aviation.com"
    receiver_email = "tim.kent@ci-aviation.com"
    password = "#A1rplane2023"

    # Create the email
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = "Scheduled Email"

    body = "This is a test email sent using Python."
    msg.attach(MIMEText(body, 'plain'))

    # Connect to the server and send the email
    try:
        # server = smtplib.SMTP('smtp.example.com', 587)
        server = smtplib.SMTP('sh10.nethosting.com', 465)
        server.starttls()
        server.login(sender_email, password)
        text = msg.as_string()
        server.sendmail(sender_email, receiver_email, text)
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")
    finally:
        server.quit()

if __name__ == "__main__":
    send_email()
