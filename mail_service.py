import random, string

email_otp = {'key1': 'value1'}
class mail_service:

    def __init__(self, smtp_server, smtp_port, username, password):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.username = username
        self.password = password

    def send_email(self, recipient, subject, body):
        import smtplib
        from email.mime.text import MIMEText

        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = self.username
        msg['To'] = recipient

        with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
            server.starttls()
            server.login(self.username, self.password)
            server.sendmail(self.username, [recipient], msg.as_string())

    def send_otp(self, recipient):
        random_string = generate_random_alphanumeric().upper()
        body = 'OTP for email verification is ' + random_string
        print(random_string)
        email_otp[recipient] = random_string
        self.send_email(recipient, 'Email Verification', body)



def generate_random_alphanumeric(length=6):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def verify_email(recipient, otp):
    print(recipient)
    print(otp)
    if recipient in email_otp:
        generated_otp = email_otp[recipient]
        if generated_otp == otp:
            return True
    return False