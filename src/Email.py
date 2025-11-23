import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_simple_email(smtp_server, port, login, password, 
                     from_addr, to_addr, subject, body):
    
    msg = MIMEMultipart('alternative')
    msg['From'] = from_addr
    msg['To'] = to_addr
    msg['Subject'] = subject
    
    html_part = MIMEText(body, 'html')
    
    msg.attach(html_part)
    
    try:
        server = smtplib.SMTP(smtp_server, port)
        server.starttls()
        server.login(login, password)
        
        server.send_message(msg)
        print(f"Письмо отправлено: {to_addr}")
    except Exception as e:
        print(f"Ошибка при отправке письма: {e}")
    finally:
        server.quit()