from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password
# # Create your models here.


# class User(models.Model):
#     mobile = models.CharField(max_length=10, null=True, blank=True)
#     address = models.CharField(max_length=256, null=True, blank=True)
#     image = models.FileField(upload_to='profileImage', null=True, blank=True)
#     status = models.BooleanField(default=True)
#     date = models.DateTimeField(auto_now_add=True)
#     userType = models.IntegerField(default=1)
#     pswd = models.CharField(max_length=100, null=True, blank=True)

#     class meta:
#         db_table = "User"


class Gallery(models.Model):
    name = models.CharField(max_length=50, default='',null=True, blank=True)   
    gallery = models.ImageField(upload_to='gallery', null=True,
                                     blank=True)
    description = models.CharField(max_length=5000, default='',null=True, blank=True)
    subtitle = models.CharField(max_length=200, default='',null=True, blank=True)
    deleted_at = models.DateTimeField(editable=True,auto_now_add=True,null=True, blank=True)
    delete_status = models.BooleanField(default=False,null=True, blank=True)
    # created_by = models.ForeignKey('User', on_delete=models.CASCADE, null=True, blank=True,
    #                                related_name="gallery_createdby")
    def __str__(self):
        return str(self.name)
    