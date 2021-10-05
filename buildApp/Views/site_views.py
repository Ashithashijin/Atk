from django.shortcuts import render,redirect,HttpResponseRedirect
#######################Site###############################
def index(request):
    return render(request,'site/index.html')

def gallery(request):
    return render(request,'site/gallery.html')

def contact(request):
    return render(request,'site/contact.html')

def about(request):
    return render(request,'site/about.html')

def blog(request):
    return render(request,'site/blog-details.html')

def catalogue(request):
    return render(request,'site/catalogue.html')

def product(request):
    return render(request,'site/product.html')

def productDetails(request):
    return render(request,'site/productDetails.html')

def productTile(request):
    return render(request,'site/productTile.html')