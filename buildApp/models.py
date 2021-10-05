from django.db import models
import uuid
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password
from django.utils.timezone import now
from PIL import Image

# Create your models here.
class User(AbstractUser):
    # userRole
    #
    #     1 :Superuser,
    #     2 :Admin,
    #     3 :Manager

    mobile = models.CharField(max_length=10, null=True, blank=True)
    address = models.CharField(max_length=256, null=True, blank=True)
    image = models.FileField(upload_to='profileImage', null=True, blank=True)
    status = models.BooleanField(default=True)
    date = models.DateTimeField(auto_now_add=True)
    userType = models.IntegerField(default=1)
    pswd = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return str(self.username)

    def save(self, *args, **kwargs):
        if self.is_superuser == False:
            pass_wd = self.password
            self.pswd = self.password
            self.password = make_password(pass_wd)

        super(User, self).save(*args, **kwargs)

    class meta:
        db_table = "User"
class Brands_tb (models.Model):
    brand_name = models.CharField(max_length=64, default='')
    brand_id = models.CharField(max_length=32, default='')
    created_date = models.CharField(max_length=32, default='')
    created_by = models.ForeignKey('User', on_delete=models.CASCADE, null=True, blank=True,
                                   related_name="brand_createdby")
    updated_date = models.CharField(max_length=32, default='')
    updated_by = models.ForeignKey('User', on_delete=models.CASCADE, null=True, blank=True,
                                   related_name="brand_updatedby")
    deleted_status = models.CharField(max_length=32, default='False')
    deleted_by = models.ForeignKey('User', on_delete=models.CASCADE, null=True, blank=True,
                                   related_name="brand_deletedby")
    deleted_at = models.DateTimeField(null=True, blank=True)
    def __str__(self):
        return str(self.brand_name)
    def save(self, *args, **kwargs):
        brand_id=self.brand_name[:3] +  uuid.uuid4().hex[:6]
        self.brand_id=brand_id
        super(Brands_tb, self).save(*args, **kwargs)
    class meta:
        db_table = "Brands_tb"
        
class Category_tb (models.Model):
    category_name=models.CharField(max_length=32, default='')
    category_id = models.CharField(max_length=32, default='')
    category_image = models.ImageField(upload_to='category', null=True, blank=True)
    created_date = models.CharField(max_length=32, default='')
    created_by = models.ForeignKey('User', on_delete=models.CASCADE, null=True, blank=True,
                                   related_name="category_createdby")
    updated_date = models.CharField(max_length=32, default='')
    updated_by = models.ForeignKey('User', on_delete=models.CASCADE, null=True, blank=True,
                                   related_name="category_updatedby")
    deleted_status = models.CharField(max_length=32, default='False')
    deleted_by = models.ForeignKey('User', on_delete=models.CASCADE, null=True, blank=True,
                                   related_name="category_deletedby")
    deleted_at = models.DateTimeField(null=True, blank=True)
    def __str__(self):
            return str(self.category_name)

    def save(self, *args, **kwargs):
        category_id=self.category_name[:3] +  uuid.uuid4().hex[:6]
        self.category_id=category_id
        super(Category_tb, self).save(*args, **kwargs)
    class meta:
        db_table = "Category_tb"
class Products_tb (models.Model):
    product_name=models.CharField(max_length=64, default='')
    product_id = models.CharField(max_length=32, null=True,blank=True)
    category = models.ForeignKey(Category_tb, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brands_tb, on_delete=models.CASCADE)
    product_image = models.ImageField(upload_to='product', null=True,blank=True)
    product_image1 = models.ImageField(upload_to='product', null=True,blank=True)
    product_image2 = models.ImageField(upload_to='product', null=True,blank=True)
    product_image3 = models.ImageField(upload_to='product', null=True,blank=True)
    product_image_main = models.ImageField(upload_to='product', null=True,blank=True)
    price = models.FloatField(default=0.00)
    product_description = models.CharField(max_length=200, null=True,blank=True)
    product_details = models.CharField(max_length=200, null=True,blank=True)
    product_priority = models.CharField(max_length=32, null=True,blank=True)
    created_date = models.DateTimeField(editable=True,auto_now_add=True)
    created_by = models.ForeignKey('User', on_delete=models.CASCADE, null=True, blank=True,
                                   related_name="product_createdby")
    updated_date = models.DateTimeField(null=True,blank=True)
    updated_by = models.ForeignKey('User', on_delete=models.CASCADE, null=True, blank=True,
                                   related_name="product_updatedby")
    deleted_status = models.BooleanField(default=False)
    deleted_by = models.ForeignKey('User', on_delete=models.CASCADE, null=True, blank=True,
                                   related_name="product_deletedby")
    deleted_at = models.DateTimeField(null=True, blank=True)
    def __str__(self):
        return str(self.product_name)
    def save(self, *args, **kwargs):
        product_id=self.product_name[:3] + uuid.uuid4().hex[:6]
        self.product_id=product_id
        super(Products_tb, self).save(*args, **kwargs)
    class meta:
        db_table = "Products_tb"
    # def save(self, *args, **kwargs):
    #     if self.product_image is not None:
    #         super().save(*args, **kwargs)
    #         product_image = Image.open(self.product_image.path)
    #         # if product_image.height > 100 or product_image.weight > 100:
    #         output_size = (370, 270)
    #         product_image.thumbnail(output_size)
    #         product_image.save(self.product_image.path)
    # def save(self, *args, **kwargs):
    #     if self.product_image1:
    #         super().save(*args, **kwargs)
    #         product_image1 = Image.open(self.product_image1.path)
    #         # if product_image.height > 100 or product_image.weight > 100:
    #         output_size = (170, 180)
    #         product_image1.thumbnail(output_size)
    #         product_image1.save(self.product_image1.path)
    # def save(self, *args, **kwargs):
    #     if self.product_image2:
    #         super().save(*args, **kwargs)
    #         product_image2 = Image.open(self.product_image2.path)
    #         # if product_image.height > 100 or product_image.weight > 100:
    #         output_size = (170, 180)
    #         product_image2.thumbnail(output_size)
    #         product_image2.save(self.product_image2.path)
    # def save(self, *args, **kwargs):
    #     if self.product_image3:
    #         super().save(*args, **kwargs)
    #         product_image3 = Image.open(self.product_image3.path)
    #         # if product_image.height > 100 or product_image.weight > 100:
    #         output_size = (170, 180)
    #         product_image3.thumbnail(output_size)
    #         product_image3.save(self.product_image3.path)
    # def save(self, *args, **kwargs):
    #     if self.product_image_main:
    #         super().save(*args, **kwargs)
    #         product_image_main = Image.open(self.product_image_main.path)
    #         # if product_image.height > 100 or product_image.weight > 100:
    #         output_size = (505, 584)
    #         product_image_main.thumbnail(output_size)
    #         product_image_main.save(self.product_image_main.path)

class ContactUs_tb (models.Model):    
    name = models.CharField(max_length=32, default='',null=True, blank=True)
    last_name = models.CharField(max_length=32, default='', null=True, blank=True)
    email = models.CharField(max_length=32, default='',null=True, blank=True)
    phone = models.CharField(max_length=32, default='',null=True, blank=True)
    subject = models.CharField(max_length=100, default='',null=True, blank=True)    
    details = models.CharField(max_length=500, default='',null=True, blank=True)
    date = models.DateTimeField(editable=True,auto_now_add=True,null=True, blank=True)
    response_status = models.CharField(max_length=32, default='',null=True, blank=True)
    def __str__(self):
        return str(self.name)
    class meta:
        db_table = "ContactUs_tb"
class AboutUs_tb (models.Model):
    name = models.CharField(max_length=32, default='')
    date = models.CharField(max_length=32, default='')
    details = models.CharField(max_length=200, default='')

    def __str__(self):
        return str(self.name)
    class meta:
        db_table = "AboutUs_tb"
class GalleryTypes_tb (models.Model):
    name = models.CharField(max_length=32, default='')
    gallerytype_id = models.CharField(max_length=32, default='')
    date = models.BooleanField(default=False)
    status = models.BooleanField(default=False)
    def __str__(self):
        return str(self.name)
    def save(self, *args, **kwargs):
        gallerytype_id=self.name[:3] +  uuid.uuid4().hex[:6]
        self.gallerytype_id=gallerytype_id
        super(GalleryTypes_tb, self).save(*args, **kwargs)
    class meta:
        db_table = "GalleryTypes_tb"
class Gallery_tb (models.Model):
    name = models.CharField(max_length=50, default='')
    brand_name = models.CharField(max_length=100, default='')    
    gallery = models.ImageField(upload_to='gallery')
    latest_product = models.ImageField(upload_to='gallery')
    description = models.CharField(max_length=200, default='')
    gallery_type = models.CharField(max_length=100, default='')
    deleted_at = models.DateTimeField(editable=True,auto_now_add=True)
    delete_status = models.BooleanField(default=False)
    created_date = models.DateTimeField(editable=True,auto_now_add=True)
    created_by = models.ForeignKey('User', on_delete=models.CASCADE, null=True, blank=True,
                                   related_name="gallery_createdby")
    def __str__(self):
        return str(self.id)
    class meta:
        db_table = "Gallery_tb"
    # def save(self, *args, **kwargs):
    #     if self.gallery:
    #         super().save(*args, **kwargs)
    #         gallery = Image.open(self.gallery.path)
    #         # if product_image.height > 100 or product_image.weight > 100:
    #         output_size = (370, 390)
    #         gallery.thumbnail(output_size)
    #         gallery.save(self.gallery.path)
    # def save(self, *args, **kwargs):
    #     if self.latest_product:
    #         super().save(*args, **kwargs)
    #         latest_product = Image.open(self.latest_product.path)
    #         # if product_image.height > 100 or product_image.weight > 100:
    #         output_size = (370, 270)
    #         latest_product.thumbnail(output_size)
    #         latest_product.save(self.latest_product.path)

class GetPrice_tb (models.Model):    
    name = models.CharField(max_length=32, default='')
    phone = models.CharField(max_length=32, default='')
    city = models.CharField(max_length=100, default='')    
    details = models.CharField(max_length=300, default='')
    date = models.DateTimeField(editable=True,auto_now_add=True)
    product_id = models.ForeignKey(Products_tb, on_delete=models.CASCADE, null=True, blank=True)
    def __str__(self):
        return str(self.name)
    class meta:
        db_table = "GetPrice_tb"

class NewsLetter_tb (models.Model):    
    email = models.CharField(max_length=32, default='')   
    date = models.DateTimeField(editable=True,auto_now_add=True)    
    def __str__(self):
        return str(self.email)
    class meta:
        db_table = "NewsLetter_tb"




       # 

class Gallery(models.Model):
    name = models.CharField(max_length=50, default='',null=True, blank=True)   
    gallery = models.ImageField(upload_to='gallery', null=True,
                                     blank=True)
    gallery_side = models.ImageField(upload_to='gallery', null=True,
                                     blank=True)
    gallery_side1 = models.ImageField(upload_to='gallery', null=True,
                                     blank=True)
    gallery_row = models.ImageField(upload_to='gallery', null=True,
                                     blank=True)
    description = models.CharField(max_length=5000, default='',null=True, blank=True)
    subtitle = models.CharField(max_length=200, default='',null=True, blank=True)
    deleted_at = models.DateTimeField(editable=True,auto_now_add=True,null=True, blank=True)
    delete_status = models.BooleanField(default=False,null=True, blank=True)
    # created_by = models.ForeignKey('User', on_delete=models.CASCADE, null=True, blank=True,
    #                                related_name="gallery_createdby")
    def __str__(self):
        return str(self.name)
    class meta:
        db_table = "gallery"    

class index_tb(models.Model):
    title = models.CharField(max_length=500, default='',null=True, blank=True) 
    subtitle = models.CharField(max_length=500, default='',null=True, blank=True)
    description = models.CharField(max_length=5000, default='',null=True, blank=True)  
    index_image = models.ImageField(upload_to='index', null=True,
                                     blank=True)   

    def __str__(self):
        return str(self.title)
    class meta:
        db_table = "index"                                       