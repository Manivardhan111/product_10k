from django.db import models

# Create your models here.


class intrestedStudent(models.Model):
    id = models.AutoField(primary_key=True,null=False)
    name = models.CharField(max_length=50, null=False)
    email = models.EmailField(max_length=50, null=False)
    mobile = models.CharField(max_length=10, null=False)
    is_registered = models.CharField(default='pending', max_length=15)
    status = models.CharField(max_length=25, default="interested", null=False)
    visited_on = models.DateField(default="0000-00-00", null=True)

    def __str__(self):
        return f"{self.name} with {self.email} is {self.status}. His registration status is {self.is_registered}"


class registeredStudents(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    name = models.CharField(max_length=50, null=False)
    email = models.EmailField(max_length=50, null=False, unique=True)
    mobile = models.CharField(max_length=10, null=False)
    city = models.CharField(max_length=50, null=False)
    qualification = models.CharField(max_length=50, null=False)
    is_registered = models.CharField(default='pending', max_length=15)
    payment_status = models.CharField(default='pending', max_length=15)
    password = models.CharField(max_length=15, default='null', null=False)
    auth_token = models.CharField(max_length=150, null=False, default="null")

    def __str__(self):
        return f"{self.id} {self.name} {self.city} {self.qualification} {self.email} {self.mobile}"
