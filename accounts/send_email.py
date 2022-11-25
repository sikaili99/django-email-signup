import os
from smtplib import SMTPException
from rest_framework.response import Response
from rest_framework import status
from templated_email import send_templated_mail

def send_email_verify(first_name,email,token, *args, **kwargs):

    token_link = "http://localhost:3000/{}".format(token)
     
    try:
        send_templated_mail(
            template_name='email_verify',
            from_email=os.environ.get('DEFAULT_FROM_EMAIL'),
            recipient_list= [email],
            context={
                'name':first_name,
                'token_link': token_link,
            }
        )
    except SMTPException as e:
        Response({"error": "There was an error sending an email,contact admin."}, status=status.HTTP_200_OK)
