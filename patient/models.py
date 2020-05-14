from django.db import models
from django.contrib.auth.models import User
from doctor.models import Doctor

# Create your models here.

class Patient(models.Model):
    user=models.OneToOneField(
        'auth.user',
        on_delete=models.CASCADE,
    )
    Is_patient = models.BooleanField(default=True)
    Is_doctor = models.BooleanField(default=False)

    name = models.CharField(max_length=50)
    dob = models.DateField(null=True)
    pin = models.IntegerField(null=True)
    address = models.CharField(max_length=100, null=True)
    mobile_no = models.CharField(max_length=13,null=True)
    gender = models.CharField(max_length=10,null=True)
    image = models.ImageField(upload_to='profile_img', blank=True, null=True)

    def __str__(self):
        return self.name


class Appointment(models.Model):
    appointment_id = models.AutoField(primary_key=True)
    pat_id = models.IntegerField(null=False)
    doc_id = models.IntegerField(null=False)
    appointment_status = models.BooleanField(default=False)
    payment_status = models.BooleanField(default=False)
    reject_status = models.BooleanField(default=False)
    appdate = models.CharField(max_length=30 ,null=True)
    time = models.CharField(max_length=30 ,null=True)
    reason = models.CharField(max_length=200, null=True)
    fees = models.IntegerField(null=True)
    txnid = models.CharField(max_length=40, null=True)





class Chat(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    message = models.TextField()

    def __unicode__(self):
        return self.message

    