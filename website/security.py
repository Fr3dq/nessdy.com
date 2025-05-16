import secrets
from email.mime.text import MIMEText
from flask import flash
import os
import smtplib, ssl
from email.message import EmailMessage
import dkim

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


def SendEmail(recipient_email, token, version, from_who=None):
    email_sender = 'nessdy.com@gmail.com'
    email_password = os.getenv('NESSDY_GMAIL_PASSWD')
    port = 465  # For SSL

    # HTML templates for each email type
    if version == 1:
        subject = "Password Reset Request"
        body = f"""
        <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6;">
                <p>Dear User,</p>
                <p>We received a request to reset your password. Please use the following token to proceed:</p>
                <p style="font-size: 18px; font-weight: bold; margin: 20px 0;">{token}</p>
                <p>If you didn't request this, please ignore this email.</p>
                <p>Best regards,<br>The Nessdy Team</p>
            </body>
        </html>
        """
    elif version == 2:
        subject = "Account Verification"
        body = f"""
        <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6;">
                <p>Dear User,</p>
                <p>Thank you for registering with us. Here is your verification code:</p>
                <p style="font-size: 18px; font-weight: bold; margin: 20px 0;">{token}</p>
                <p>Please enter this code to complete your account verification.</p>
                <p>Best regards,<br>The Nessdy Team</p>
            </body>
        </html>
        """
    elif version == 3:
        subject = "User Support Request"
        body = f"""
        <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6;">
                <p>Support Team,</p>
                <p>A user has reported the following issue:</p>
                <p style="background-color: #f5f5f5; padding: 10px; border-left: 3px solid #ccc;">{token}</p>
                <p>Reported by: {from_who}</p>
                <p>Please address this issue at your earliest convenience.</p>
                <p>System Notification</p>
            </body>
        </html>
        """
    
    # Plain text fallback
    text_body = f"Here is your information: {token}" if version in [1, 2] else f"User {from_who} reported: {token}"

    em = EmailMessage()
    em['From'] = f"Nessdy Support <{email_sender}>"
    em['To'] = recipient_email
    em['Subject'] = subject
    
    # Set both HTML and plain text versions
    em.set_content(text_body)
    em.add_alternative(body, subtype='html')

    context = ssl.create_default_context()

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', port, context=context) as smtp:
            smtp.login(email_sender, email_password)
            smtp.sendmail(email_sender, recipient_email, em.as_string())
            flash("Email sent successfully", category="success")
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