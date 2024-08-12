from evalinst import settings
import os
import json
from email.message import EmailMessage
import ssl
import smtplib
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.core import serializers

def sendEmail(request, context, emailSubject, sendTo):
    sendFrom = settings.EMAIL_HOST_USER
    html_content = render_to_string('loadlist/mailAprendiz.html', context, request=request)

    try:
        #I used EmailMultiAlternatives because I wanted to send both text and html
        emailMessage = EmailMultiAlternatives(subject=emailSubject, body=html_content, from_email=sendFrom, to=[sendTo,], reply_to=[sendFrom,])
        emailMessage.attach_alternative(html_content, "text/html")
        emailMessage.send(fail_silently=False)

    except Exception as e:
        print('There was an error sending an email: ', e) 
        error = {'message': ",".join(e.args) if len(e.args) > 0 else 'Unknown Error'}
        raise serializers.ValidationError(error)


def sendEmailInst(request, context, emailSubject, sendTo):
    sendFrom = settings.EMAIL_HOST_USER
    html_content = render_to_string('loadlist/mailInstructor.html', context, request=request)

    try:
        #I used EmailMultiAlternatives because I wanted to send both text and html
        emailMessage = EmailMultiAlternatives(subject=emailSubject, body=html_content, from_email=sendFrom, to=[sendTo,], reply_to=[sendFrom,])
        emailMessage.attach_alternative(html_content, "text/html")
        emailMessage.send(fail_silently=False)

    except Exception as e:
        print('There was an error sending an email: ', e) 
        error = {'message': ",".join(e.args) if len(e.args) > 0 else 'Unknown Error'}
        raise serializers.ValidationError(error)


def sendEmailCoord(request, context, emailSubject, sendTo):
    sendFrom = settings.EMAIL_HOST_USER
    html_content = render_to_string('loadlist/mailCoordinador.html', context, request=request)

    try:
        #I used EmailMultiAlternatives because I wanted to send both text and html
        emailMessage = EmailMultiAlternatives(subject=emailSubject, body=html_content, from_email=sendFrom, to=[sendTo,], reply_to=[sendFrom,])
        emailMessage.attach_alternative(html_content, "text/html")
        emailMessage.send(fail_silently=False)

    except Exception as e:
        print('There was an error sending an email: ', e) 
        error = {'message': ",".join(e.args) if len(e.args) > 0 else 'Unknown Error'}
        raise serializers.ValidationError(error)

'''with open('C:/Users/USUARIO/Desktop/json_config/evalinstructorV1.json') as config_file:
    config = json.load(config_file)

EMAIL_HOST_USER = config['EMAIL_USER']
EMAIL_HOST_PASSWORD = config['EMAIL_PASSWORD']
EMAIL_RECEIVER = 'oboi2995@gmail.com'

subject = 'Texto de ejemplo'

body = 'Texto de ejemplo 2'

em = EmailMessage()
em['From'] = EMAIL_HOST_USER
em['To'] = EMAIL_RECEIVER
em['Subject'] = subject
em.set_content(body)

context = ssl.create_default_context()

with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
    smtp.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
    smtp.sendmail(EMAIL_HOST_USER, EMAIL_RECEIVER, em.as_string())'''