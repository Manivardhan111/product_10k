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
