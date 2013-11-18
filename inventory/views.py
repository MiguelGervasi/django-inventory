from django.template import Context, loader, RequestContext
from django.views.generic import ListView, CreateView, FormView, DeleteView
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404, render_to_response
from django.contrib.auth.decorators import login_required
from django.forms.models import inlineformset_factory
from django.utils import simplejson
from chartit import DataPool, Chart
from django.db.models import Count
from datetime import datetime, timedelta
from django.core.exceptions import ValidationError
from inventory.models import *
from inventory.forms import InventoryForm, CategoryForm, ProductForm, ProdInvFormSet
from django.core.urlresolvers import reverse_lazy

from django.utils.decorators import method_decorator



# @login_required(login_url='/accounts/login/')
class index(ListView):
    def get_context_data(self, **kwargs):
        context = super(index, self).get_context_data(**kwargs)
        context['inv_form'] = InventoryForm
        context['cat_form'] = CategoryForm
        context['product_form'] = ProductForm()
        context['formset'] = ProdInvFormSet
        context['allinv'] = Inventory.objects.all()
        context['allcats'] = Category.objects.all()
        return context


# doesn't work atm
class delete_product(ListView):
    def post(self, request):
        if request.method == "POST":
            # context = self.get_context_data()
            del_list = InventoryProduct.objects.filter(id__in=request.POST.getlist('product_list'))
            del_list.delete()
            return HttpResponseRedirect('/inventory')
            

class delete_product_confirm(ListView):
    model=InventoryProduct
    template_name = "inventory/product_confirm_delete.html"
    def post(self, request):
        if 'product_list' in request.POST:
            del_list = InventoryProduct.objects.filter(id__in=request.POST.getlist('product_list'))
            return render_to_response('inventory/product_confirm_delete.html', {'object' : del_list }, context_instance=RequestContext(request))

    # def get_context_data(self, **kwargs):
    #     context = super(delete_product, self).get_context_data(**kwargs)
    #     return context
    # def post(self, request):
    #     if request.method == "POST":
    #         del_list = InventoryProduct.objects.filter(id__in=request.POST.getlist('product_list'))
    #         return HttpResponse(render_to_response('inventory/product_confirm_delete.html', {'object' : del_list }, context_instance=RequestContext(request)))
    #     else:
    #         return super(delete_product, self).get_context_data(**kwargs)

            
class InventoryFormView(CreateView):
    def get_context_data(self, **kwargs):
        context = super(InventoryFormView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['inv_form'] = InventoryForm(self.request.POST)
        else:
            context['inv_form'] = InventoryForm()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        inv_form = context['inv_form']
        if inv_form.is_valid():
            self.object = form.save()
            inv_form.instance = self.object
            inv_form.save()
            return HttpResponseRedirect('/inventory/')
        else:
            return self.render_to_response(self.get_context_data(form=form))

class CategoryFormView(CreateView):
    def get_context_data(self, **kwargs):
        context = super(CategoryFormView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['cat_form'] = CategoryForm(self.request.POST)
        else:
            context['cat_form'] = CategoryForm()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        cat_form = context['cat_form']
        if cat_form.is_valid():
            self.object = form.save()
            cat_form.instance = self.object
            cat_form.save()
            return HttpResponseRedirect('/inventory/')
        else:
            return self.render_to_response(self.get_context_data(form=form))


class ProductFormView(CreateView):
    def get_context_data(self, **kwargs):
        context = super(ProductFormView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = ProdInvFormSet(self.request.POST)
        else:
            context['formset'] = ProdInvFormSet()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        prodinv_form = context['formset']
        if prodinv_form.is_valid():
            self.object = form.save()
            prodinv_form.instance = self.object
            prodinv_form.save()
            return HttpResponseRedirect('/inventory/')
        else:
            return HttpResponse("form is invalid.. this is just an HttpResponse object")

            # return self.render_to_response(self.get_context_data(form=form))

    def form_invalid(self, form):
        return HttpResponse("form is invalid.. this is just an HttpResponse object")

# class ProductFormView(CreateView):
#     def get_context_data(self, **kwargs):
#         context = super(ProductFormView, self).get_context_data(**kwargs)
#         if self.request.POST:
#             context['formset'] = ProdInvFormSet(self.request.POST)
#         else:
#             context['formset'] = ProdInvFormSet()
#         return context

#     def form_valid(self, form):
#         context = self.get_context_data()
#         prodinv_form = context['formset']
#         if prodinv_form.is_valid():
#             self.object = form.save()
#             prodinv_form.instance = self.object
#             prodinv_form.save()
#             return HttpResponseRedirect('/inventory/')
#         else:
#             return self.render_to_response(self.get_context_data(form=form))

def ajax_post(request, product):
    if request.method == 'POST':
        pk = request.POST['pk']
        name = request.POST['name']
        pro = InventoryProduct.objects.get(pk=pk)
        data = request.POST
        if(name == 'quantity_sold'+pk):
            pro.quantity_sold = pro.quantity_sold + int(request.POST['value']) 
            pro.quantity_on_hand = pro.quantity_on_hand - int(request.POST['value'])
            pro.save()
        elif(name == 'quantity_on_hand'+pk):
            pro.quantity_on_hand = pro.quantity_on_hand + int(request.POST['value'])
            pro.save()
        elif(name == 'inventory'+pk):
            x = Inventory.objects.get(pk=request.POST['value'])
            pro.inventory = x
            pro.save()
        elif(name == 'product'+pk):
            prod = Product.objects.get(pk=pk)
            cat = Category.objects.get(product_category=request.POST['value[product_category]'])
            prod.product_category = cat
            prod.product_name = request.POST['value[product_name]']
            prod.product_unit_price = request.POST['value[product_unit_price]']
            prod.product_sell_price = request.POST['value[product_sell_price]']
            prod.product_description = request.POST['value[product_description]']
            prod.save()
        elif(name == 'qis'+pk):
            pro.quantity_on_hand = request.POST['value']
            pro.save()
            data = { 'qis': pro.quantity_on_hand}
        elif(name == 'qs'+pk):
            pro.quantity_sold = request.POST['value']
            pro.save()
        json_dump = simplejson.dumps(data)
        return HttpResponse(json_dump, mimetype='application/json')  



def reports_generate(request):
        if request.method == "POST":
            for each in InventoryProduct.objects.all():
                reports=Product_Reports()
                reports.product=each
                if reports.product is not None:
                    reports.total_quantity_sold = reports.product.quantity_sold
                    reports.total_sell_amt_earned = reports.product.product.product_sell_price * reports.total_quantity_sold
                    reports.total_unit_amt_earned = reports.product.product.product_unit_price * reports.total_quantity_sold
                    reports.total_profit_earned = reports.total_sell_amt_earned - reports.total_unit_amt_earned
                    reports.save()
            inventory_product = InventoryProduct.objects.update(quantity_sold='0')    
        return HttpResponseRedirect('/inventory/reports')

# class reports(ListView):
#        def get_context_data(self, **kwargs):
#         context = super(reports, self).get_context_data(**kwargs)
#         if request.is_ajax():
#             for each in InventoryProduct.objects.all():
#                 reports=Product_Reports()
#                 reports.product=each
#                 if reports.product is not None:
#                     reports.total_quantity_sold = reports.product.quantity_sold
#                     reports.total_sell_amt_earned = reports.product.product.product_sell_price * reports.total_quantity_sold
#                     reports.total_unit_amt_earned = reports.product.product.product_unit_price * reports.total_quantity_sold
#                     reports.total_profit_earned = reports.total_sell_amt_earned - reports.total_unit_amt_earned
#                     reports.save()
#             inventory_product = InventoryProduct.objects.update(quantity_sold='0')
#         return context



        # for each in InventoryProduct.objects.all():
        #     reports=Product_Reports()
        #     reports.product=each
        #     if reports.product is not None:
        #         reports.total_quantity_sold = reports.product.quantity_sold
        #         reports.total_sell_amt_earned = reports.product.product.product_sell_price * reports.total_quantity_sold
        #         reports.total_unit_amt_earned = reports.product.product.product_unit_price * reports.total_quantity_sold
        #         reports.total_profit_earned = reports.total_sell_amt_earned - reports.total_unit_amt_earned
        #         reports.save()
        # inventory_product = InventoryProduct.objects.update(quantity_sold='0')
        # return HttpResponseRedirect("/inventory/reports/")
        # else:
        #     return super(reports, self).post(request, *args, **kwargs)


    # if request.method == "POST":
    #     for each in InventoryProduct.objects.all():
    #         reports=Product_Reports()
    #         reports.product=each
    #         if reports.product is not None:
    #             reports.total_quantity_sold = reports.product.quantity_sold
    #             reports.total_sell_amt_earned = reports.product.product.product_sell_price * reports.total_quantity_sold
    #             reports.total_unit_amt_earned = reports.product.product.product_unit_price * reports.total_quantity_sold
    #             reports.total_profit_earned = reports.total_sell_amt_earned - reports.total_unit_amt_earned
    #             reports.save()
    #     inventory_product = InventoryProduct.objects.update(quantity_sold='0')
    #     return HttpResponseRedirect("/inventory/reports/")

class report_chart_view(ListView):
    def get_context_data(self, **kwargs):
        context = super(report_chart_view, self).get_context_data(**kwargs)   
        if 'val' in self.request.GET:    
            date_object = datetime.datetime.now()
            startDate = date_object - timedelta(days=7)
            product = self.request.GET['val']
            
            if self.request.GET['view'] == "week":
                obj = Product_Reports.objects.filter(report_date__range=[startDate, date_object], product__product=product).order_by('report_date')
            elif self.request.GET['view'] == "month":
                obj = Product_Reports.objects.filter(report_date__year=date_object.year, report_date__month=date_object.month, product__product=product).order_by('report_date')
            elif self.request.GET['view'] == "year":
                obj = Product_Reports.objects.filter(report_date__year=date_object.year, product__product=product).order_by('report_date')
            else:
                obj = Product_Reports.objects.filter(report_date__range=[startDate, date_object], product__product=product).order_by('report_date')
        else:
            obj = Product_Reports.objects.filter(product__product=None)

        weatherdata = \
            DataPool(
               series=
                [{'options': {
                   'source': obj},
                  'terms': [
                    'report_date',
                    'total_quantity_sold',
                    'total_unit_amt_earned',
                    'total_sell_amt_earned',
                    'total_profit_earned'
                    ]}
                 ])

        #Step 2: Create the Chart object
        cht = Chart(
                datasource = weatherdata,
                series_options =
                  [{'options':{
                      'type': 'line',
                      'stacking': False},
                    'terms':{
                      'report_date': [
                        'total_quantity_sold',
                        'total_unit_amt_earned',
                        'total_sell_amt_earned',
                        'total_profit_earned'
                  ]
                      }}],
                chart_options =
                  {'title': {
                       'text': 'Product Report Data'},
                   'xAxis': {
                        'title': {
                           'text': 'Date'}},
                   'yAxis': {
                    'title': {
                       'text': 'Total Quantity Sold & Total Profit'}}
                       })
        context['weatherchart'] = cht
        return context

    