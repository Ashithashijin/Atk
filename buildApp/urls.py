"""buildmart URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from .views import *
from .Views.site_views import *
from . import views
urlpatterns = [
    path('upload/<str:name>',simple_upload,name='upload'),
    path('signup/', SignUp.as_view(), name='signup'),
    path('', Login, name='login'),
    path('home/page', Home, name='home'),
    path('logout/', Logout, name='logout'),

    path('user/', UserList, name='users'),

    path('brand/', Brands, name='brands'),
    path('brand/update/',admin_update_brand,name='brandupdate'),
	path('brand/view_update_brand/',admin_view_update_brand,name='brandviewupdate'),
	path('brand/delete/',admin_delete_brand,name='branddelete'),

    path('category/', Category, name='category'),
    path('category/update/',admin_update_category,name='categoryupdate'),
    path('category/update/', admin_update_category, name='categoryupdate'),
	# path('category/view_update_category/',admin_view_update_category,name='categoryviewupdate'),
	path('category/delete/',admin_delete_category,name='categorydelete'),

    path('products/', Products, name='products'),
    path('products/update/', admin_update_products, name='productsupdate'),
    path('products/delete/', admin_delete_product, name='productsdelete'),

    # path('gallerytypes/', GalleryTypes, name='gallerytypes'),
    # path('gallerytypes/delete/', admin_delete_gallerytypes, name='gallerytypesdelete'),

    path('gallerys/', Gallerys, name='gallerys'),
    path('gallery/delete/', admin_delete_gallery, name='gallerydelete'),

    path('contactus/', contactus, name='contactus'),
    
    path('getprice/', getprice, name='getprice'),

    path('newsletter/', newsletter, name='newsletter'),
    # path('create_gallery/',views.creategallery, name='create_gallery'),
    # path('gallery/', gallery, name='gallery'),
    









]
