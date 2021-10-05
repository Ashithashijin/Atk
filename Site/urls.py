
from django.urls import path
# from Site import views
from . import views
from .views import *

urlpatterns = [
    # path('', views.index),
    # path('about/', views.about),
    # path('gallery/', views.gallery),
    # path('contact/', views.contact),

    path('', index, name='index'),
    path('gallery/', gallery, name='gallery'),
    path('contact/', contact, name='contact'),
    path('contactus/', contactus, name='contactus'),
    path('about/', about, name='about'),
    path('create_gallery/',views.creategallery, name='create_gallery'),
    path('create_index/',views.createindex, name='create_index'),

]
