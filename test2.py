import os
import smtplib
from email.message import EmailMessage
from email.mime.image import MIMEImage

EMAIL_ADDRESS = os.environ.get('EMAIL_USER')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASS')
msg = EmailMessage()

msg['Subject'] = 'Welcome to Aaksathe!'
msg['From'] = EMAIL_ADDRESS
msg['To'] = 'das.saikat23@gmail.com'
name="saikat"
msg.set_content('Welcome to Aaksathe!')

msg.add_alternative("""\
<!DOCTYPE html>
<html>
    <body>
        <img src="cid:image1" width="200" height="200">
        <h1 style="color:Green;">Welcome to Aaksathe!!</h1>
            <h2 style="color:LightGreen;">Together we can</h2>
            </br>
            <h4>Hi """+name.capitalize()+""",
            Together we can do a lot of things, be it helping people or getting help.
            As you have joined Aaksathe, you will get to know like minded people eager to help people in need.
            Join a Group to start helping or you can do your part by donating to causes set up across the world.</h4>
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

with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
    smtp.ehlo()
    smtp.starttls()
    smtp.ehlo()
    smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
    smtp.send_message(msg)