import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from decouple import config
from jinja2 import Template
# import jwt

smtp_server = config("MAIL_SERVER")
port = config("MAIL_PORT")
sender_email = config("Sender_email")
password = config("Server_pass")
frontend = config("frontend")
booking_path = 'Server/booking_template.html'
reschedule_path = 'Server/reschedule_template.html'
cancel_path ='Server/cancel_template.html'


# def generate_token(id):
#     secret_key = config("SECRET_KEY")
#     return jwt.encode({"id": id}, secret_key, algorithm="HS256")

 
def send_mail(fullname, email, date, time_12, id):
    receiver_email = email
    
    token = id
    Reschedule = f"{frontend}/Reschedule?id={token}"
    print(Reschedule)
    Cancel = frontend + "/Cancel?id=" + str(token)

    with open(booking_path, "r") as file:
        email_template = Template(file.read())

    
        
    html_content = email_template.render(fullname=fullname, date=date, time=time_12, id=id, Reschedule=Reschedule, Cancel=Cancel)
    
    
    subject = "Your Appointment is Scheduled"
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message.attach(MIMEText(html_content, "html"))
  

    try:
        with smtplib.SMTP_SSL(smtp_server, port) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")

    


 
def reschedule_mail(fullname, email, date, time_12, id):
    
    receiver_email = email
    token = id
    Reschedule = f"{frontend}/Reschedule?id={token}"
    Cancel = f"{frontend}/Cancel?id={token}"

    with open(reschedule_path, "r") as file:
        email_template = Template(file.read())

    
        
    html_content = email_template.render(fullname=fullname, date=date, time=time_12, id=id, Reschedule=Reschedule, Cancel=Cancel)
    
    
    subject = "Your Appointment is recheduled"
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message.attach(MIMEText(html_content, "html"))
  

    try:
        with smtplib.SMTP_SSL(smtp_server, port) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")

    

 
def cancel_mail(email, date, time_12):
    
    receiver_email = email

    with open(cancel_path, "r") as file:
        email_template = Template(file.read())

    
        
    html_content = email_template.render(frontend=frontend, date=date, time=time_12)
    
    
    subject = "Your Appointment is cancelled"
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message.attach(MIMEText(html_content, "html"))
  

    try:
        with smtplib.SMTP_SSL(smtp_server, port) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")

    