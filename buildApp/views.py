from django.shortcuts import render, redirect , HttpResponseRedirect
from .forms import *
from .models import *
from django.contrib.messages.views import SuccessMessageMixin
from django.views import generic
from django.urls import reverse_lazy,reverse
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
# Create your views here.
from django.core.exceptions import PermissionDenied
import datetime
from .resources import *
def user_is_entry_author(function):
    def wrap(request, *args, **kwargs):
        if request.session.get('myid') is None:
            return redirect('login')

        return function(request, *args, **kwargs)
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap
@user_is_entry_author
def Home(request):
    print(request.session['myid'])
    return render(request,'pages/homepage.html')
def UserList(request):
    form=createUserForm()
    query=User.objects.all().order_by('-id')
    if request.method == "POST":
        form=createUserForm(request.POST,request.FILES)
        if request.method == "POST":
            form = createUserForm(request.POST, request.FILES)
            if form.is_valid():
                user_form = form.save(commit=False)
                user_form.userType=2
                user_form.save()
                messages.add_message(request, messages.SUCCESS, 'User Successfully Created!')
                return redirect('users')
            print(form.errors)
    context={
        'form':form,
        'query':query
    }
    return render(request,'pages/user.html',context)
class SignUp(SuccessMessageMixin, generic.CreateView):
    model = User
    form_class = registerForm
    template_name = 'auth/signup.html'
    success_url = reverse_lazy('login')
    success_message = "successfully registered"
def Login(request):
    if request.method=="POST":
        print("44444")
        username=request.POST["username"]
        password=request.POST["password"]
        chk=User.objects.filter(username=username,pswd=password,userType='2').exists()
        if chk:
            print("4....5")
            chk_obj=User.objects.get(username=username,pswd=password,userType='2')
            request.session['myid']=chk_obj.id
            return redirect('home')

        else:
            print("4....5nooooooooo")
            messages.add_message(request, messages.WARNING, 'Login Failed!   Not  user......')

            return render(request, 'auth/login.html')
    else:
        return render(request, 'auth/login.html')
def Logout(request):
    if request.session.has_key('myid'):
        del request.session['myid']
        logout(request)
    return HttpResponseRedirect('/myadmin/')
##################Brands#############################
def Brands(request):
    if request.session.has_key('myid'):
        if request.method=="POST":
            brand_name = request.POST['brandname']
            var = User.objects.get(id=request.session.get('myid'))
            current_date = datetime.datetime.now().date()
            check = Brands_tb.objects.all().filter(brand_name=brand_name, created_by=var,deleted_status=False)  # ,brand_id=brand_id
            if check:
                messages.add_message(request, messages.ERROR, 'Failed! Brand Name Already Created!!')

                return redirect('brands')
            else:
                add = Brands_tb(brand_name=brand_name, created_by=var, created_date=current_date)  # ,brand_id=brand_id
                add.save()
                messages.add_message(request, messages.SUCCESS, 'Brand Successfully Created!')

                return redirect('brands')
        else:
            query = Brands_tb.objects.all().filter(deleted_status="False")
            deleted = Brands_tb.objects.all().filter(deleted_status="True")
            return render(request, 'pages/brands.html', {'query': query, 'deleted': deleted})
    else:
        return redirect('login')


def admin_update_brand(request):
    if request.session.has_key('myid'):
        if request.method == 'GET':
            id2 = request.GET['id']
            fromReg = Brands_tb.objects.get(id=id2)
            query=Brands_tb.objects.filter(deleted_status=False)
            # if fromReg.exists():
            return render(request, 'pages/admin_update_brand.html', {'form': fromReg,'query':query})
            # else:
            #     return render(request, 'pages/admin_update_brand.html', {'query': fromReg})
    else:
        return redirect('login')


def admin_view_update_brand(request):
    if request.method == "POST":
        up = request.GET['id']
        brand_name = request.POST['brandname']
        update_user = User.objects.get(id=request.session.get('myid'))
        current_date = datetime.datetime.now().date()

        Brands_tb.objects.filter(id=up).update(brand_name=brand_name, updated_date=current_date,
                                               updated_by=update_user)  # brand_id=brand_id,
        messages.add_message(request, messages.SUCCESS, 'Brand Successfully Updated!')

        return redirect('brands')
    elif request.method == "GET":
        up = request.GET['id']
        query = Brands_tb.objects.all().filter(id=up)
        return render(request, 'pages/brands.html', {'query': query})

def admin_delete_brand(request):
    if request.session.has_key('myid'):
        id1 = request.GET['id']
        var = User.objects.get(id=request.session.get('myid'))
        Brands_tb.objects.all().filter(id=id1).update(deleted_by=var, deleted_status="True",deleted_at=datetime.datetime.now().date())
        up = Brands_tb.objects.all().filter(deleted_status="False")
        return redirect('brands')
    else:
        return redirect('login')
from tablib import Dataset

def simple_upload(request,name):
    print(name)
    result=""
    if request.method == 'POST':
        if name == 'brand':
            person_resource = PersonResource()
            page='brands'
        elif name == 'category':
            print("----------------")
            person_resource = categoryResource()
            page = 'category'
        else:
            print("ppppppppppppppppppp")
            person_resource = productResource()
            page='products'
        dataset = Dataset()
        new_persons = request.FILES.get('myfile', None)
        # --------------
        file_format = new_persons.content_type
        if file_format == "text/csv":
            imported_data = dataset.load(new_persons.read().decode('utf-8'), format='csv')
            print("sv",imported_data)
            result = person_resource.import_data(dataset, dry_run=True,
                                                 current_user=request.user)  # Test the data import
        elif file_format == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
            imported_data = dataset.load(new_persons.read(), format='xlsx')
            print("xlsx",imported_data)
            result = person_resource.import_data(dataset, dry_run=True, current_user=request.user)
        if not result.has_errors():
            print("ok")
            person_resource.import_data(dataset, dry_run=False, current_user=request.user)  # Actually import now
            return redirect(page)
        else:
            print(result.totals)
            messages.add_message(request, messages.WARNING, 'Import csv/xlsx files!')
            return redirect(page)
        # ------------
        # # imported_data = dataset.load(new_persons.read())
        # imported_data = dataset.load(new_persons.read().decode('utf-8'), format='csv')
        # print(imported_data)
        # result = person_resource.import_data(dataset, dry_run=True,current_user=request.user)  # Test the data import
        # # for r in imported_data:
        # #     print(r)
        # #     Brands_tb.objects.get_or_create(
        # #         id=r[1][1],brand_name=r[1][2])
        # if not result.has_errors():
        #     print("ok")
        #     person_resource.import_data(dataset, dry_run=False,current_user=request.user)  # Actually import now
        # else:
        #     print(result.has_errors())
        # return redirect(page)
##################Brands end############################
##################Category ############################
# def Category(request):
#     if request.session.has_key('myid'):
#         if request.method == "POST":
#             category_name = request.POST['categoryname']
#
#             var = User.objects.get(id=request.session.get('myid'))
#             current_date = datetime.datetime.now().date()
#             query = Category_tb.objects.all().filter(deleted_status="False")
#             deleted = Category_tb.objects.all().filter(deleted_status="True")
#
#             check = Category_tb.objects.all().filter(category_name=category_name,
#                                                      created_by=var,deleted_status=False)  # ,category_id=category_id
#             if check:
#                 messages.add_message(request, messages.ERROR, 'Failed! Category Name Already Created!!')
#                 return redirect('category')
#             else:
#                 add = Category_tb(category_name=category_name, created_by=var,
#                                   created_date=current_date)  # ,category_id=category_id
#                 add.save()
#                 messages.add_message(request, messages.SUCCESS, 'Category Successfully Created!')
#
#                 return redirect('category')
#         else:
#             query = Category_tb.objects.all().filter(deleted_status="False")
#             deleted = Category_tb.objects.all().filter(deleted_status="True")
#             return render(request, 'pages/category.html', {'query': query, 'deleted': deleted})
#     else:
#         return redirect('login')
#
#
# def admin_update_category(request):
#     if request.session.has_key('myid'):
#         if request.method == 'GET':
#             id2 = request.GET['id']
#             fromReg = Category_tb.objects.get(id=id2)
#             query = Category_tb.objects.filter(deleted_status=False)
#             # if fromReg.exists():
#             return render(request, 'pages/admin_update_category.html', {'form': fromReg, 'query': query})
#     else:
#         return redirect('login')
#
#
# def admin_view_update_category(request):
#     if request.method == "POST":
#         up = request.GET['id']
#         category_name = request.POST['categoryname']
#         # category_id=request.POST['categoryid']
#         current_date = datetime.datetime.now().date()
#         ii = request.session['myid']
#         var = User.objects.get(id=request.session.get('myid'))
#
#
#         Category_tb.objects.filter(id=up).update(category_name=category_name, updated_date=current_date,
#                                                  updated_by=var)  # brand_id=brand_id,
#         messages.add_message(request, messages.SUCCESS, 'Category Successfully Updated!')
#
#         return redirect('category')
#     elif request.method == "GET":
#         up = request.GET['id']
#         query = Category_tb.objects.all().filter(id=up)
#         return render(request, 'pages/category.html', {'query': query})
#
#
# def admin_delete_category(request):
#     if request.session.has_key('myid'):
#         id1 = request.GET['id']
#
#         var = User.objects.get(id=request.session.get('myid'))
#         Category_tb.objects.all().filter(id=id1).update(deleted_by=var, deleted_status="True",deleted_at=datetime.datetime.now().date())
#         up = Category_tb.objects.all().filter(deleted_status="False")
#         return redirect('category')
#     else:
#         return redirect('login')
def Category(request):
    if request.session.has_key('myid'):
        form = categoryForm(request.POST or None, request.FILES or None)
        if request.method == "POST":
            if form.is_valid():
                cat_form = form.save(commit=False)
                cat_form.created_date = datetime.datetime.now().date()
                created_user=User.objects.get(id=request.session.get('myid'))
                cat_form.created_by=created_user
                cat_form.save()
                print("success")
                messages.add_message(request, messages.SUCCESS, 'Category Successfully Created!')


                return redirect('category')
            else:
                print(form.errors)

        else:

            form=categoryForm(request.POST or None, request.FILES or None)
        query = Category_tb.objects.all().filter(deleted_status="False")
        deleted = Category_tb.objects.all().filter(deleted_status="True")
        print("here")
        return render(request, 'pages/category.html',{'query': query, 'deleted': deleted,'form':form})
    else:
        return render(request, 'auth/login.html')

def admin_update_category(request):
    if request.session.has_key('myid'):
        id2 = request.GET['id']
        print(id2)
        fromReg = Category_tb.objects.get(id=id2)
        if request.method == 'POST':
            print("hi")
            id2 = request.GET['id']
            form=categoryForm(request.POST,request.FILES, instance=fromReg)
            if form.is_valid():
                print("kkk");
                cat_form = form.save(commit=False)
                cat_form.updated_date = datetime.datetime.now().date()
                cat_form.created_date = fromReg.created_date

                updated_user=User.objects.get(id=request.session.get('myid'))
                cat_form.updated_by=updated_user
                cat_form.save()
                messages.add_message(request, messages.SUCCESS, 'Category Successfully Updated!')
            else:
                print(form.errors)
                messages.add_message(request, messages.SUCCESS, form.errors)

            return redirect('category')
        else:
            id2 = request.GET['id']
            fromReg = Category_tb.objects.get(id=id2)
            form = categoryForm(instance=fromReg)
            query = Category_tb.objects.all().filter(deleted_status="False")
            deleted = Category_tb.objects.all().filter(deleted_status="True")
            return render(request, 'pages/admin_update_category.html', {'cat':fromReg,'query': query, 'deleted': deleted, 'form': form})
    else:
        return render(request, 'auth/login.html')
def admin_delete_category(request):
    if request.session.has_key('myid'):
        id1 = request.GET['id']

        var = User.objects.get(id=request.session.get('myid'))
        Category_tb.objects.all().filter(id=id1).update(deleted_by=var, deleted_status="True",deleted_at=datetime.datetime.now().date())
        up = Category_tb.objects.all().filter(deleted_status="False")
        return redirect('category')
    else:
        return redirect('login')
##################Category end############################
##################Products############################
def Products(request):
    if request.session.has_key('myid'):
        form = productForm(request.POST or None, request.FILES or None)
        if request.method == "POST":
            if form.is_valid():
                pro_form = form.save(commit=False)
                pro_form.created_date = datetime.datetime.now().date()
                created_user=User.objects.get(id=request.session.get('myid'))
                pro_form.created_by=created_user
                pro_form.save()
                print("success")
                messages.add_message(request, messages.SUCCESS, 'Product Successfully Created!')


                return redirect('products')
            else:
                print(form.errors)

        else:

            form=productForm(request.POST or None, request.FILES or None)
        category = Category_tb.objects.all().filter(deleted_status="False")
        brand = Brands_tb.objects.all().filter(deleted_status="False")
        query = Products_tb.objects.all().filter(deleted_status="False")
        deleted = Products_tb.objects.all().filter(deleted_status="True")
        print("here")
        return render(request, 'pages/products.html',
                          {'category': category, 'brand': brand, 'query': query, 'deleted': deleted,'form':form})
    else:
        return render(request, 'auth/login.html')
def admin_update_products(request):
    if request.session.has_key('myid'):
        id2 = request.GET['id']
        print(id2)
        fromReg = Products_tb.objects.get(id=id2)
        if request.method == 'POST':
            print("hi")
            id2 = request.GET['id']
            form=productForm(request.POST,request.FILES, instance=fromReg)
            if form.is_valid():
                print("kkk");
                pro_form = form.save(commit=False)
                pro_form.updated_date = datetime.datetime.now().date()
                pro_form.created_date = fromReg.created_date

                updated_user=User.objects.get(id=request.session.get('myid'))
                pro_form.updated_by=updated_user
                pro_form.save()
                messages.add_message(request, messages.SUCCESS, 'Product Successfully Updated!')
            else:
                print(form.errors)
                messages.add_message(request, messages.SUCCESS, form.errors)

            return redirect('products')
        else:
            id2 = request.GET['id']
            fromReg = Products_tb.objects.get(id=id2)
            form = productForm(instance=fromReg)
            query = Products_tb.objects.all().filter(deleted_status="False")
            deleted = Products_tb.objects.all().filter(deleted_status="True")
            return render(request, 'pages/admin_update_products.html', {'prodct':fromReg,'query': query, 'deleted': deleted, 'form': form})
    else:
        return render(request, 'auth/login.html')
def admin_delete_product(request):
    if request.session.has_key('myid'):
        id1 = request.GET['id']

        var = User.objects.get(id=request.session.get('myid'))
        Products_tb.objects.all().filter(id=id1).update(deleted_by=var, deleted_status="True",deleted_at=datetime.datetime.now().date())
        up = Products_tb.objects.all().filter(deleted_status="False")
        return redirect('products')
    else:
        return redirect('login')
##################Products end############################
##################Gallery Type#############################
def GalleryTypes(request):
    if request.session.has_key('myid'):
        if request.method=="POST":
            name = request.POST.get['type']
            current_date = datetime.datetime.now().date()
            check = GalleryTypes_tb.objects.all().filter(name=name,status=False) 
            if check:
                messages.add_message(request, messages.ERROR, 'Failed! Gallery Type Already Created!!')

                return redirect('gallerytype')
            else:
                add = GalleryTypes_tb(name=name, date=current_date)  
                add.save()
                messages.add_message(request, messages.SUCCESS, 'Gallery Type Successfully Created!')

                return redirect('gallerytype')
        else:
            query = GalleryTypes_tb.objects.all().filter(status="False")
            deleted = GalleryTypes_tb.objects.all().filter(status="True")
            return render(request, 'pages/gallery_type.html', {'query': query, 'deleted': deleted})
    else:
        return redirect('login')


def admin_delete_gallerytypes(request):
    if request.session.has_key('myid'):
        id1 = request.GET['id']
        GalleryTypes_tb.objects.all().filter(id=id1).update(status="True",date=datetime.datetime.now().date())
        up = GalleryTypes_tb.objects.all().filter(status="False")
        return redirect('gallerytype')
    else:
        return redirect('login')
##################Gallery Type end############################
##################Gallery #############################
def Gallerys(request):
    if request.session.has_key('myid'):
        form = productForm(request.POST or None, request.FILES or None)
        if request.method=='POST':
            name=request.POST.get('name')
            brand_name=request.POST.get('brand_name')
            gallery=request.FILES.get('product_image')
            description=request.POST.get('description')
            gallery_type=request.POST.get('gallery_type')
            print('------------------------------',gallery_type)
            latest_product=request.FILES.get('product_image1')
            var = User.objects.get(id=request.session.get('myid'))
            current_date = datetime.datetime.now().date()
            check=Gallery_tb.objects.all().filter(name=name,brand_name=brand_name,gallery=gallery,description=description,gallery_type=gallery_type,created_by=var)
            if check:
                messages.add_message(request, messages.ERROR, 'Failed! Gallery Already Created!!')
                return redirect('gallerys')
            else:
                if gallery_type == 'Gallery':
                    add=Gallery_tb(name=name,brand_name=brand_name,gallery=gallery,description=description,gallery_type=gallery_type,created_date=current_date,created_by=var)
                    add.save()
                    messages.add_message(request, messages.SUCCESS, 'Gallery Successfully Created!------')
                    return redirect('gallerys')
                else:
                    add=Gallery_tb(name=name,brand_name=brand_name,latest_product=latest_product,gallery_type=gallery_type,created_date=current_date,created_by=var)
                    add.save()
                    messages.add_message(request, messages.SUCCESS, 'Gallery Successfully Created!***')
                    return redirect('gallerys')
        else:
            query = Gallery_tb.objects.all().filter(delete_status="False")
            deleted = Gallery_tb.objects.all().filter(delete_status="True")
            brands =Brands_tb.objects.all().filter(deleted_status="False")
            return render(request, 'pages/gallery.html', {'query': query, 'deleted': deleted,'form':form,'brands':brands})
    else:
        return redirect('login')


def admin_delete_gallery(request):
    if request.session.has_key('myid'):
        id1 = request.GET['id']
        Gallery_tb.objects.all().filter(id=id1).update(delete_status="True",deleted_at=datetime.datetime.now().date())
        up = Gallery_tb.objects.all().filter(delete_status="False")
        return redirect('gallerys')
    else:
        return redirect('login')
##################Gallery end############################
def contactus(request):
    query=ContactUs_tb.objects.all().order_by('-date')  
    context={
        'query':query
    }
    return render(request,'pages/contactus.html',context)

def getprice(request):
    query=GetPrice_tb.objects.all().order_by('-date')  
    context={
        'query':query
    }
    return render(request,'pages/getprice.html',context)

def newsletter(request):
    query=NewsLetter_tb.objects.all().order_by('-date')  
    context={
        'query':query
    }
    return render(request,'pages/newsletter.html',context)

# def creategallery(request):
#     form = GalleryForm()
#     if request.method=='POST':
#         form = GalleryForm(request.POST,request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('create_gallery')
#         else:
#             print("hhhhh",form.errors)
#     context = {"form":form}
#     return render(request,'create_gallery.html',context)
    
# def gallery(request):
    
#     gall=Gallery.objects.all()
    
#     return render (request,'gallery.html',{'gall':gall})