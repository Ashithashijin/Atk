from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin
# Register your models here.
admin.site.register(User)
# admin.site.register(Brands_tb)
# admin.site.register(Category_tb)
# admin.site.register(Products_tb)
@admin.register(Brands_tb)
class PersonAdmin(ImportExportModelAdmin):
    pass
@admin.register(Category_tb)
class categoryAdmin(ImportExportModelAdmin):
    pass
@admin.register(Products_tb)
class productAdmin(ImportExportModelAdmin):
    pass
admin.site.register(ContactUs_tb)
admin.site.register(Gallery_tb)
admin.site.register(NewsLetter_tb)
admin.site.register(AboutUs_tb)
admin.site.register(GalleryTypes_tb)
admin.site.register(GetPrice_tb)
admin.site.register(Gallery)
admin.site.register(index_tb)