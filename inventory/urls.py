from django.conf.urls import patterns, url
from inventory.models import *
from inventory.views import *
from django.views.generic import DetailView, ListView, TemplateView
from django.db.models import Count
from inventory.forms import ProductForm, CategoryForm, InventoryForm
from django.core.urlresolvers import reverse_lazy


urlpatterns = patterns('',
   

   url(r'delete_product_confirm/$', delete_product_confirm.as_view(), name='delete_product_confirm'),
   url(r'delete_product/$', delete_product.as_view(), name='delete_product'),
   
   url(r'^$',
    index.as_view(
        queryset=InventoryProduct.objects.all(),
        context_object_name='inventory_product',
        template_name='inventory/index.html'),
    name='index'),

   url(r'product_select_view/$',
    ListView.as_view(
        queryset=InventoryProduct.objects.all(),
        context_object_name='inventory_product',
        template_name='inventory/product_select_view.html'),
    name='product_select_view'),

   url(r'product_update_view/$',
    index.as_view(
        queryset=InventoryProduct.objects.all(),
        context_object_name='inventory_product',
        template_name='inventory/product_update_view.html'),
    name='product_update_view'),

   url(r'product_delete_view/$',
    ListView.as_view(
        queryset=InventoryProduct.objects.all(),
        context_object_name='inventory_product',
        template_name='inventory/product_delete_view.html'),
    name='product_delete_view'),

   url(r'reports/$',
    ListView.as_view(
        queryset=Product_Reports.objects.all(),
        context_object_name='Product_Reports',
        template_name='inventory/reports.html'),
    name='reports'),

   url(r'report_table_view/$',
    ListView.as_view(
        queryset=Product_Reports.objects.all(),
        context_object_name='Product_Reports',
        template_name='inventory/report_table_view.html'),
    name='report_table_view'),

   url(r'report_chart_view/$',
    report_chart_view.as_view(
        queryset=Product_Reports.objects.values('product__product__product_name','product__id').annotate(p=Count('product', flat=True)).distinct(),
        context_object_name='Product_Reports',
        template_name='inventory/report_chart_view.html'),
    name='report_chart_view'),
   
   url('^prod_form/$',
    ProductFormView.as_view(
    template_name = 'inventory/index.html',
      form_class = ProductForm,
      success_url = '/inventory/'),
    name='prod_form_view_url'),

   url('^cat_form/$',
    CategoryFormView.as_view(
    template_name = 'inventory/index.html',
      form_class = CategoryForm,
      success_url = '/inventory/'),
    name='cat_form_view_url'),

   url('^inv_form/$',
    InventoryFormView.as_view(
    template_name = 'inventory/index.html',
      form_class = InventoryForm,
      success_url = '/inventory/'),
    name='inv_form_view_url'),
   url(r'^(?P<product>\d+)/post$', ajax_post, name="ajax_post"), 
   
   url(r'^reports_generate$', reports_generate, name="reports_generate"), 

   # url('post/$',
   #  ajax_post.as_view(),
   #  name='ajax_post'),


   # url(r'report_table_view/$',
   #  TemplateView.as_view(
   #      template_name='inventory/report_table_view.html'),
   #  name='report_table_view'),


   # url(r'^(?P<product>\d+)/report_table_view/$', views.report_table_view, name='report_table_view'),
   # url(r'reports/$', views.reports, name='reports'),
   # url(r'report_chart_view/$', views.report_chart_view, name='report_chart_view'),
   # url(r'^(?P<product>\d+)/$', views.edit, name='edit'),
   # url(r'^(?P<product>\d+)/post2$', views.ajax_post2, name="ajax_post2"), 
   # url(r'^(?P<product>\d+)/update$', views.update_member, name="update_member"), 
   # url(r'^search_result$', views.search_result, name="search_result"), 
)

# from django.conf.urls import patterns, url
# from inventory.models import Inventory, InventoryProduct, Product

# urlpatterns = patterns('',
#     url(r'^$',
#         ListView.as_view(
#             queryset=InventoryProduct.objects.order_by('-id'),
#             context_object_name='inventory_product',
#             template_name='inventory/index.html'),
#         name='index'),
#     url(r'^(?P<pk>\d+)/$',
#         DetailView.as_view(
#             model=Product,
#             context_object_name='followform',
#             template_name='inventory/detail.html'),
#         name='detail'),
#     url(r'^(?P<pk>\d+)/results/$',
#         DetailView.as_view(
#             model=Product,
#             template_name='inventory/results.html'),
#         name='results'),
#     url(r'^(?P<product__product_id>\d+)/vote/$', 'inventory.views.vote', name='vote'),

# )


