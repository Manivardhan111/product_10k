from django.db import models

# Create your models here.


class Mentor(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=50,)
    email = models.EmailField(max_length=50,)
    password = models.CharField(max_length=15,)
    is_admin = models.BooleanField(default=False)
    approved_by = models.CharField(max_length=50, default="")
    approval_status = models.CharField(max_length=50, default="pending")
    role = models.CharField(max_length=15, default="admin")

    def __str__(self):
        return f"{self.name} is-admin: {self.is_admin}"
class Assessment_Questions(models.Model):
    id = models.AutoField(primary_key=True)
    question=models.CharField(default="null")
    option_1=models.CharField(max_length=150,null=False,default="null")
    option_2=models.CharField(max_length=150,null=False,default="null")
    option_3=models.CharField(max_length=150,null=False,default="null")
    option_4=models.CharField(max_length=150,null=False,default="null")
    correct_answer=models.CharField(max_length=150,null=False,default="null")
    def __str__(self) :
        return f'{self.question}: correct answer is {self.correct_answer}'