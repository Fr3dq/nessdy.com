import secrets
import smtplib
from email.mime.text import MIMEText
from flask import flash
import os

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

def SendEmail(recipient_email, token):
    try:
        msg = MIMEText("Here is your token: {token}")
        msg['From'] = "nessdy.com@gmail.com"
        msg['To'] = recipient_email
        msg['Subject'] = "Password reset"

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls() #TLS hashing
        server.login("nessdy.com@gmail.com", "fokus468A@")
        server.send_message(msg)
        server.quit()
        flash("Email sent", category="error")
    except Exception as e:
        print(f"Error: {e}")
        flash("Couldn't send message", category="error")


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