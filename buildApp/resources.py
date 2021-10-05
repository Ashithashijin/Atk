from import_export import resources
from .models import Brands_tb,User,Category_tb,Products_tb
import datetime
from import_export.fields import Field
from import_export.widgets import ForeignKeyWidget
class PersonResource(resources.ModelResource):
    brand_name = Field(attribute='brand_name', column_name='Brands')
    class Meta:
        model = Brands_tb
        fields = ('id','brand_name',)

    def after_import_instance(self, instance, new, **kwargs):
        # user=User.objects.get(id=kwargs['current_user'])
        instance.created_by = kwargs['current_user']
        instance.created_date = datetime.datetime.now().date()
class categoryResource(resources.ModelResource):
    brand_name = Field(attribute='category_name', column_name='Category')
    class Meta:
        model = Category_tb
        fields = ('id','category_name',)

    def after_import_instance(self, instance, new, **kwargs):
        # user=User.objects.get(id=kwargs['current_user'])
        instance.created_by = kwargs['current_user']
        instance.created_date = datetime.datetime.now().date()
class productResource(resources.ModelResource):
    product_name = Field(attribute='product_name', column_name='Product Name')
    brand = Field(column_name='Brands', attribute='brand',
                           widget=ForeignKeyWidget(Brands_tb, field='brand_name'))
    category = Field(column_name='Category', attribute='category',
                            widget=ForeignKeyWidget(Category_tb, field='category_name'))
    price = Field(attribute='price', column_name='Price')
    product_description = Field(attribute="product_description", column_name='Product Description')
    product_details = Field(attribute='product_details', column_name='Product Details')
    product_priority = Field(attribute="product_priority", column_name='Product Priority')
    class Meta:
        model = Products_tb
        fields = ('id','product_name','brand','category','product_description','product_details','product_priority','price',)
        import_id_fields = ('product_name','brand','category',)
    def after_import_instance(self, instance, new, **kwargs):
        # user=User.objects.get(id=kwargs['current_user']
        instance.created_by = kwargs['current_user']
        instance.created_date = datetime.datetime.now()
