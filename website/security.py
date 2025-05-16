import secrets
from email.mime.text import MIMEText
from flask import flash
import os
import smtplib, ssl
from email.message import EmailMessage

def ResetPasswordToken():
    secure_code = secrets.randbelow(900000) + 100000
    return secure_code


def StrongPasswordVeryfication(password): #It chceks if password is correct
    SpecialCharactersTable = ["!", "@", "#", "%", "^", "&", "*", "(", ")", "_", "-", "=", "+"]
    if len(password) < 6:
        return 1
    chcecker = False
    for x in password:
        if x in SpecialCharactersTable:
            chcecker = True
    if chcecker != True:
        return 1
    return 0       

def CheckForSpecialSigns(data): #It checks if special characters are entered
    for i in data:
        sign = ord(i)
        if (sign > 32 and sign < 45) or (sign > 45 and sign < 48) or (sign > 57 and sign < 65) or (sign > 90 and sign < 94) or (sign > 122 and sign < 126) or sign == 96:
            return 1
    return 0
 
def DivideLinks(link):
    link = link.replace("\n", " ")
    tab = link.split(" ")
    for i in tab: 
        if i == '':
            tab.remove(i) 
    return tab


def SendEmail(recipient_email, token, version, from_who):
    email_sender='nessdy.com@gmail.com'
    email_password = os.getenv('NESSDY_GMAIL_PASSWD')
    port = 465  # For SSL

    if version == 1:
        subject="Password Reset Request"
        html_body = f"""
        <html>
            <body>
                <p style="font-family: Arial, sans-serif; font-size: 14px; color: #333;">
                    Hello,
                </p>
                <p style="font-family: Arial, sans-serif; font-size: 14px; color: #333;">
                    We received a request to reset your password. Here is your password reset token:
                </p>
                <p style="font-family: Arial, sans-serif; font-size: 16px; font-weight: bold; color: #0066cc; margin: 20px 0;">
                    {token}
                </p>
                <p style="font-family: Arial, sans-serif; font-size: 14px; color: #333;">
                    If you didn't request this, please ignore this email.
                </p>
                <p style="font-family: Arial, sans-serif; font-size: 14px; color: #333;">
                    Best regards,<br>
                    The Nessdy Team
                </p>
            </body>
        </html>
        """
    elif version == 2:
        subject="Account Verification"
        html_body = f"""
        <html>
            <body>
                <p style="font-family: Arial, sans-serif; font-size: 14px; color: #333;">
                    Welcome!
                </p>
                <p style="font-family: Arial, sans-serif; font-size: 14px; color: #333;">
                    Thank you for registering with us. Here is your account verification code:
                </p>
                <p style="font-family: Arial, sans-serif; font-size: 16px; font-weight: bold; color: #0066cc; margin: 20px 0;">
                    {token}
                </p>
                <p style="font-family: Arial, sans-serif; font-size: 14px; color: #333;">
                    Please enter this code to complete your registration.
                </p>
                <p style="font-family: Arial, sans-serif; font-size: 14px; color: #333;">
                    Best regards,<br>
                    The Nessdy Team
                </p>
            </body>
        </html>
        """
    elif version == 3:
        subject="User Support Request"
        html_body = f"""
        <html>
            <body>
                <p style="font-family: Arial, sans-serif; font-size: 14px; color: #333;">
                    Support Team,
                </p>
                <p style="font-family: Arial, sans-serif; font-size: 14px; color: #333;">
                    The following user has reported an issue:
                </p>
                <p style="font-family: Arial, sans-serif; font-size: 14px; font-weight: bold; color: #333;">
                    User: {from_who}
                </p>
                <p style="font-family: Arial, sans-serif; font-size: 14px; color: #333;">
                    Problem description:
                </p>
                <p style="font-family: Arial, sans-serif; font-size: 14px; color: #333; background-color: #f5f5f5; padding: 10px; border-left: 3px solid #0066cc;">
                    {token}
                </p>
                <p style="font-family: Arial, sans-serif; font-size: 12px; color: #666; margin-top: 20px;">
                    This is an automated notification from the Nessdy system.
                </p>
            </body>
        </html>
        """
    
    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = recipient_email
    em['Subject'] = subject
    em.set_content(body)  # Keep plain text fallback
    em.add_alternative(html_body, subtype='html')  # Add HTML version

    context = ssl.create_default_context()

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', port, context=context) as smtp:
            smtp.login(email_sender, email_password)
            smtp.sendmail(email_sender, recipient_email, em.as_string())
            flash("Success", category="error")
    except Exception as e:
        print(f"Error: {e}")
        flash("Couldn't send message", category="error")

    # email_sender='nessdy.com@gmail.com'
    # email_password = os.getenv('NESSDY_GMAIL_PASSWD')
    # port = 465  # For SSL

    # if version == 1:
    #     subject="Password reset"
    #     body = f"Hey, here is your password reset token: {token}"
    # elif version == 2:
    #     subject="Account verification"
    #     body = f"Hey, here is your verification code: {token}"
    # elif version == 3:
    #     subject="User problem"
    #     body = f"Use: {from_who} has a problem: {token}" 
    
    # em = EmailMessage()
    # em['From'] = email_sender
    # em['To'] = recipient_email
    # em['Subject'] = subject
    # em.set_content(body)

    # context = ssl.create_default_context()

    # try:
    #     with smtplib.SMTP_SSL('smtp.gmail.com', port, context=context) as smtp:
    #         smtp.login(email_sender, email_password)
    #         smtp.sendmail(email_sender, recipient_email, em.as_string())
    #         flash("Succes", category="error")
    # except Exception as e:
    #     print(f"Error: {e}")
    #     flash("Couldn't send message", category="error")


def CheckIfNotTooBig(files, size): 
    file_length = 0
    for file in files:
        file.seek(0, os.SEEK_END)
        file_length += file.tell()
        file.seek(0)

    if file_length > size:
        return 1
    else:
        return 0