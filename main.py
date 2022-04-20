import pandas as pd


def send_notification(domain, day_left):
    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart

    sender_address = 'sender@gmail.com'
    receiver_address = 'receiver@gmail.com'
    subject = 'SSL Cert for {} is about to expire'.format(domain)
    mail_content = '''Hey, 

            Your SSL certificate for {} is about to expire in {} days.

            Please recheck and renew the certificate with the below Link.

            https://www.sslshopper.com/ssl-checker.html#hostname={}

        With regards,
        SSL Checker Bot
            '''.format(domain, day_left, domain)

    if day_left == "Expired":
        subject = 'SSL Cert for {} has Expired or an Error Found'.format(domain)
        mail_content = '''Hey, 
        
        Your SSL certificate for {} has Expired or an Error Found.
    
        Please recheck and renew the certificate with the below Link.
    
        https://www.sslshopper.com/ssl-checker.html#hostname={}
        
    With regards,
    SSL Checker Bot
        '''.format(domain, domain)

    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login("email@gmail.com", "passward")
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = subject
    message.attach(MIMEText(mail_content, 'plain'))
    text = message.as_string()
    server.sendmail(sender_address, receiver_address, text)


def check_expiration_date(domain):
    import ssl
    import socket
    import dateutil.parser
    import dateutil.utils

    context = ssl.create_default_context()
    conn = context.wrap_socket(socket.socket(socket.AF_INET), server_hostname=domain)
    conn.connect((domain, 443))
    ssl_info = conn.getpeercert()
    expiry_date = ssl_info['notAfter']
    current_date = dateutil.utils.today()
    expiry_date = dateutil.parser.parse(expiry_date)
    days_left = (expiry_date.date() - current_date.date()).days
    return days_left


domain_list = pd.read_excel('Domain.xlsx', sheet_name='Sheet1')
site = domain_list['URL']
s_no = domain_list['S.No']
print("S_No", "Domain", "Day_left")
for id in range(0, len(site)):
    try:
        day_left = check_expiration_date(site[id])
    except:
        day_left = 'Expired'

    if day_left == "Expired" or day_left == 30 or day_left == 14 or day_left <= 7:
        send_notification(site[id], day_left)

    print(s_no[id], site[id], day_left)



