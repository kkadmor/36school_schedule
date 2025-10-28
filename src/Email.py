import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_simple_email(smtp_server, port, login, password, 
                     from_addr, to_addr, subject, body):
    
    msg = MIMEMultipart()
    msg['From'] = from_addr
    msg['To'] = to_addr
    msg['Subject'] = subject
    
    msg.attach(MIMEText(body, 'html'))
    
    try:
        server = smtplib.SMTP(smtp_server, port)
        server.starttls()
        server.login(login, password)
        
        server.send_message(msg)
    except Exception as e:
        print(f"Ошибка при отправке письма: {e}")
    finally:
        server.quit()