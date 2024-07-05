from django.db import models
from django.contrib.auth.models import AbstractUser,User
from .manager import UserManager
import random
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone

from .emails import send_otp_via_email

class User(AbstractUser):
    username=None
    email=models.EmailField(unique=True)
    is_verified=models.BooleanField(default=False)
    otp=models.CharField(max_length=6, null=True)
    expires_at = models.DateTimeField(default=timezone.now())
    is_admin = models.BooleanField(default=False)
    numericRoleLevel = models.IntegerField(default=0, validators=[MaxValueValidator(5),MinValueValidator(0)])
    role = models.CharField(max_length=50, null=True)
    organization = models.CharField(max_length=50, null=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    
 

    USERNAME_FIELD='email'
    REQUIRED_FIELDS=[]
    objects=UserManager()
    
    

    # def __str__(self):
    #     return self.email
    # def save(self, *args, **kwargs):
    #     self.
    

class Resource(models.Model):
    CHOICES = [
        ('Auditorium', 'Auditorium'),
        ('ENTCSeminarHall', 'ENTCSeminarHall'), 
        ('COMPSeminarHall','COMPSeminarHall'),
        ('ITSeminarHall','ITSeminarHall'),
        ('DigitalBoard','DigitalBoard'),
        ('LawnCourt','LawnCourt'),
        ('Mic','Mic'),
        ('Camera','Camera'),
        ('Podium','Podium'),
    ]
    resource_name = models.CharField(max_length=20, primary_key=True, choices=CHOICES)
    resource_type = models.IntegerField(default=0)
    max_permission = models.IntegerField(default=3, validators=[MaxValueValidator(5), MinValueValidator(3)])
    current_permission = models.IntegerField(default=0)
    resource_head = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='head_resources')
    userperms  = models.JSONField(default=list, blank=True, null=True)

    def __str__(self):
        return f'{self.resource_name} - rh -{self.resource_head}'
    

    
# class Session(models.Model):
#     resource=models.ForeignKey(Resource,on_delete=models.CASCADE)
#     date = models.DateField(default = timezone.now, null = True)
#     start_time=models.DateTimeField(default=timezone.now,null=True)
#     end_time=models.DateTimeField(default=timezone.now,null=True)

#     def __str__(self):
#         return f"{self.resource}: {self.start_time} to {self.end_time}"

class Booking(models.Model):
    booking_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, related_name='bookings')
    date = models.DateField(default=timezone.now, null=True)
    start_time = models.DateTimeField(default=timezone.now, null=True)
    end_time = models.DateTimeField(default=timezone.now, null=True)
    # list  = models.JSONField(default=list, blank=True, null=True)
    all_true = models.BooleanField(default=False)
    # accept=models.BooleanField(default=False)
    curr_index = models.IntegerField(default = 0)
    max_index = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.email} for {self.resource.resource_name} with id={self.booking_id}"
    
    def save(self, *args, **kwargs):
        # Set the date part of start_time to current date
        if self.resource.userperms:
            self.max_index = len(self.resource.userperms)

        self.date = self.start_time.date()
        super().save(*args, **kwargs)