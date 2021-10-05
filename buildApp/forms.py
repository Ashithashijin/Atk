from django import forms
from .models import *




class registerForm(forms.ModelForm):

     class Meta:
        model = User
        fields = ['username', 'password', 'address', 'email', 'userType']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'fadeIn second', 'placeholder': 'Username'}),
            'password': forms.TextInput(attrs={'class': 'fadeIn third', 'placeholder': 'Password'}),
            'email': forms.TextInput(attrs={'class': 'fadeIn second', 'placeholder': 'Email'}),
            'address': forms.TextInput(attrs={'class': 'fadeIn second', 'placeholder': 'Address'}),



        }
class createUserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username', 'password',  'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'password': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Password','type':'password'}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),




        }
class productForm(forms.ModelForm):
    category= forms.ModelChoiceField(label='Category', queryset=Category_tb.objects.filter(deleted_status=False),
                                       widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'Category'}))
    brand = forms.ModelChoiceField(label='Brand', queryset=Brands_tb.objects.filter(deleted_status=False),
                                      widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'Brand'}))


    class Meta:
        model = Products_tb
        fields = ['product_name','price','product_image','product_image1','product_image2','product_image3','product_image_main','product_description','product_details','product_priority','brand','category']
        widgets = {
            'product_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'product name'}),
            'price': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'price'}),
            'product_description': forms.Textarea(attrs={'class': 'form-control','rows':4, 'placeholder': 'Product Description'}),
            'product_details': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'product details'}),
            'product_priority': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'product priority'}),

        }
    def save(self,  *args, **kwargs):
        photo = super(productForm, self).save(*args, **kwargs)

         # save the user here



        # image = Image.open(photo.product_image)
        # cropped_image = image.crop((50,100,60,120))
        # resized_image = cropped_image.resize((20, 20), Image.ANTIALIAS)
        # resized_image.save(photo.product_image.path)
        

        # if commit:
        #     photo.save()
        return photo
    def __init__(self, *args, **kwargs):
        super(productForm, self).__init__(*args, **kwargs)
        self.fields['category'].empty_label = ' Select a Category'
        self.fields['brand'].empty_label = ' Select a Brand'
        self.fields['price'].empty_label = 'price'


class categoryForm(forms.ModelForm):
    class Meta:
        model = Category_tb
        fields = ['category_name', 'category_image']
        widgets = {
            'category_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'category name'}),

        }

class galleryForm(forms.ModelForm):
    brand_name = forms.ModelChoiceField(label='Brand', queryset=Brands_tb.objects.filter(deleted_status=False),
                                   widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'Brand'}))

    class Meta:
        model = Gallery_tb
        fields = ['name', 'brand_name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'name'}),

        }

class GalleryForm(forms.ModelForm):
    class Meta:
        model = Gallery
        fields = ('name','subtitle','gallery')
        labels = {
                'name':'Name',
                'subtitle':'Subtitle',
                'gallery':'Gallery_Image',
               

        }
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control','placeholder':'Name'}),
            'subtitle': forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'gallery':forms.FileInput(attrs={'class':'form-control','type':'file','placeholder': ''}),
            
            
        }   

class index_tbForm(forms.ModelForm):
    class Meta:
        model = index_tb
        fields = ('title','subtitle','index_image','description')
        labels = {
                'title':'Title',
                'subtitle':'Subtitle',
                'description':'Description',
                'index_image':'Index_Image',
                

        }
        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control','placeholder':'Name'}),
            'subtitle': forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'description': forms.TextInput(attrs={'class':'form-control','placeholder':''}),
            'index_image':forms.FileInput(attrs={'class':'form-control','type':'file','placeholder': ''}),
            
            
        }  

class ContactUs_tbForm(forms.ModelForm):
    class Meta:
        model = ContactUs_tb
        fields = ('name','last_name','email','phone','subject','details')
        # labels = {
        #         'name':'Name',
        #         'last_name':'Last Name',
        #         'email':'Email',
        #         'phone':'Phone',
        #         'subject':'Subject',
        #         'details':'Comments',
                

        # }
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control','placeholder':'First Name*'}),
            'last_name': forms.TextInput(attrs={'class':'form-control','placeholder':'Last Name*'}),
            'email': forms.TextInput(attrs={'class':'form-control','placeholder':'Email*'}),
            'phone': forms.TextInput(attrs={'class':'form-control','placeholder':'Phone*'}),
            'subject': forms.TextInput(attrs={'class':'form-control','placeholder':'Subject*'}),
            'details': forms.Textarea(attrs={'class':'form-control','placeholder':'Comments'}),
            
            
            
        }                     
