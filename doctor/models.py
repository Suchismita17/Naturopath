from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Doctor(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    Is_patient = models.BooleanField(default=False)
    Is_doctor = models.BooleanField(default=True)

    name = models.CharField(max_length=50)
    dob = models.DateField()
    pin = models.IntegerField(null=True)
    address = models.CharField(max_length=100)
    specialist = models.CharField(max_length=30, null=True)
    mobile_no = models.CharField(max_length=13)
    gender = models.CharField(max_length=10,null=True)
    qualification = models.CharField(max_length=40, null=True)
    experience = models.IntegerField(null=True)
    fees = models.IntegerField(null=True, default=100)
    language = models.CharField( max_length=30 ,null=True, default='English')
    image = models.ImageField(upload_to='profile_img', blank=True,null=True)

    def __str__(self):
        return self.name

class ConsultDetails(models.Model):
    user=models.OneToOneField(Doctor, on_delete=models.CASCADE, primary_key=True)
    fees = models.IntegerField(null=True)
    time = models.CharField(max_length=50, null=True)



class Consultation(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    fees = models.IntegerField(null=True)
    time = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.user.username
    
