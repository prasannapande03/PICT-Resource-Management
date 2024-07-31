from django.core.mail import send_mail
import random
from django.conf import settings
from .models import User
from datetime import datetime, timedelta
from django.utils import timezone

from django.contrib.auth import get_user_model

# User = get_user_model()




def send_otp_via_email(email):

    subject = 'Your account verification email'

    otp = random.randint(1000, 9999)

    message = f'Your otp is {otp}'

    email_from = settings.EMAIL_HOST

    send_mail(subject, message, email_from, [email])
    user_obj=get_user_model().objects.get(email=email)
    # user_obj.expire

    user_obj.expires_at=timezone.now()+timedelta(minutes=2)
    user_obj.otp=otp
    user_obj.save()

def send_random_password(email, password):
    subject = 'Your random password'

    message = f'Your pass is {password}'

    email_from = settings.EMAIL_HOST

    send_mail(subject, message, email_from, [email])

def RequestAcceptedMail(email,resource, date, booking_id):
    message=f'Your request for {resource} on {date} has been booked'
    subject=f'{resource} Booked Resource - {booking_id}'
    email_from = settings.EMAIL_HOST
    send_mail(subject, message, email_from, [email])

def RequestDeniededMail(email,resource,date, booking_id):
    message=f'Your request for {resource} on {date} has been denied. Booking id {booking_id}'
    subject='Request Denied'
    email_from = settings.EMAIL_HOST
    send_mail(subject, message, email_from, [email])