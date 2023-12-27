from django.db import models

# Create your models here.


class intrestedStudent(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=50, null=False)
    email = models.EmailField(max_length=50, null=False)
    mobile = models.CharField(max_length=10, null=False)
    city = models.CharField(max_length=50, null=False)
    qualification = models.CharField(max_length=50, null=False)
    is_registered=models.CharField(default='pending',max_length=15)
    payment_status=models.CharField(default='pending',max_length=15)
    password=models.CharField(max_length=15,default='null',null=False)

    def __str__(self):
        return f"{self.id} {self.name} {self.city} {self.qualification} {self.email} {self.mobile}"