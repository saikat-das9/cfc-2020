import os
import smtplib
from email.message import EmailMessage
from email.mime.image import MIMEImage

EMAIL_ADDRESS = os.environ.get('EMAIL_USER')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASS')
msg = EmailMessage()

def send_registration_mail(recipient, fname, lname):
    msg['Subject'] = 'Welcome to Aaksathe!'
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = recipient
    msg.set_content('Welcome to Aaksathe!')

    msg.add_alternative("""\
    <!DOCTYPE html>
    <html>
        <body>
            <img src="cid:image1" width="150" height="150">
            <h1 style="color:Green;">Welcome to Aaksathe!!</h1>
            <h2 style="color:Green;">Together we can</h2>
            <h3>Hi """+fname.capitalize()+""" """+lname.capitalize()+""",
            Together we can do a lot of things, be it helping people or getting help.
            As you have joined Aaksathe, you will get to know like minded people eager to help people in need.
            Join a Group to start helping or you can do your part by donating to causes set up across the world.d</h3>
            </br></br></br></br>
            <h3>Let's start helping! Together we can.</h3>
            <h2>Team Aaksathe</h2>
        </body>
    </html>
    """, subtype='html')
    fp = open('logo.png', 'rb')
    msgImage = MIMEImage(fp.read())
    fp.close()
    msgImage.add_header('Content-ID', '<image1>')
    msg.attach(msgImage)
    send_mail(msg)

def forgot_password_mail(recipient, fname, lname, new_pwd):
    msg['Subject'] = 'Aaksathe - Password Changed'
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = recipient
    msg.set_content('Aaksathe - Password Changed')

    msg.add_alternative("""\
    <!DOCTYPE html>
    <html>
        <body>
            <img src="cid:image1" width="150" height="150">
            <h3>Hi """+fname.capitalize()+""" """+lname.capitalize()+""",
            Your password to your aaksathe account has been changed. 
            Use the new password to login, and we recommend changing your password from settings.
            
            This is your new password: """+new_pwd+"""</h3>
            </br></br></br></br>
            <h3>Let's continue helping! Together we can.</h3>
            <h2>Team Aaksathe</h2>
        </body>
    </html>
    """, subtype='html')
    fp = open('logo.png', 'rb')
    msgImage = MIMEImage(fp.read())
    fp.close()
    msgImage.add_header('Content-ID', '<image1>')
    msg.attach(msgImage)
    send_mail(msg)

def send_mail(msg):
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)