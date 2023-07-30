from django.db import models
from django.contrib.auth.models import User
# Create your models here.
    
class Contact(models.Model):
    user      = models.OneToOneField(User if User else 'self' , on_delete=models.CASCADE if User else models.SET_NULL,related_name='profile')
    mobile_no = models.CharField(max_length=17)
    username  = models.CharField(max_length=30)
    email_id  = models.EmailField()
    spam = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username},{self.mobile_no},{self.email_id}"
