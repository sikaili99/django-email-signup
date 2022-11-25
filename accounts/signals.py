import os
from smtplib import SMTPException
from rest_framework.response import Response
from django.dispatch import receiver
from rest_framework import status
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from templated_email import send_templated_mail
from django.db.models.signals import post_save
from .models import CustomUser,Profile

@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):

    token_link = "http://localhost:3000{}?token={}".format(reverse('password_reset:reset-password-request'), reset_password_token.key)
     
    try:
        send_templated_mail(
            template_name='password_reset',
            from_email=os.environ.get('DEFAULT_FROM_EMAIL'),
            recipient_list= [reset_password_token.user.email],
            context={
                'full_name':reset_password_token.user.get_full_name(),
                'token_link': token_link,
            }
        )
    except SMTPException as e:
        Response({"error": "There was an error sending an email,contact admin."}, status=status.HTTP_200_OK)

    return Response({'message':"password reset link sent to your email."}, status=status.HTTP_201_CREATED)


@receiver(post_save, sender=CustomUser)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=CustomUser)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()
