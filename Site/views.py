from django.shortcuts import render,redirect
from .models import *
from buildApp.models import *
from buildApp.forms import *
# from Site.models import *


# Create your views here.


def index(request):
    port = index_tb.objects.all()
    data = {'port':port}
    return render(request,'index.html',data)


def about(request):
    return render(request,'about.html')

def gallery(request):
	
    gall=Gallery.objects.all()
    
    data = {'gall':gall}
    # g_ids =[]
    # i=0
    # c= gall.count()
    # if c >= 3:
    #     for g in gall:
    #         print(gall.count())
    #         g_ids.append(g)
    #     print(g_ids)
    #     data['img1'] = g_ids[0]
    #     data['img2'] = g_ids[1]
    #     data['img3'] = g_ids[2]
        # data['img4'] = g_ids[3]
        # data['img5'] = g_ids[4]
        # data['img6'] = g_ids[5]
       
           
    return render (request,'gallery.html',data)

def contact(request):
    form = ContactUs_tbForm()
    if request.method=='POST':
        form = ContactUs_tbForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('contact')
    else:
        form = ContactUs_tbForm()
        context = {
        "form":form
        }
    return render(request,'contact.html',context)


def contactus(request):
    query=ContactUs_tb.objects.all().order_by('-date')  
    context={
        'query':query
    }
    return render(request,'pages/contactus.html',context)    
   




def creategallery(request):
    form = GalleryForm()
    if request.method=='POST':
        form = GalleryForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('create_gallery')
    else:
        form = GalleryForm()
        context = {
        "form":form
        }
    return render(request,'pages/create_gallery.html',context)

def createindex(request):
    form = index_tbForm()
    if request.method=='POST':
        form = index_tbForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('create_index')
    else:
        form = index_tbForm()
        context = {
        "form":form
        }
    return render(request,'pages/create_index.html',context)

