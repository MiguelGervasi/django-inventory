from django.contrib import admin
from inventory.models import Inventory, Product, Category, InventoryProduct, Product_Reports
from inventory.forms import RequireOneFormSet
from datetime import date

from django.utils.translation import ugettext_lazy as _
from django.contrib.admin import SimpleListFilter

from django.contrib import admin
from django.contrib import auth
from django.contrib.auth.admin import UserAdmin
from django.core.urlresolvers import reverse

##class ChoiceInline(admin.TabularInline):
##    model = Item
##    # extra = 3
##
##class PollAdmin(admin.ModelAdmin):
##    pass
##    # inlines = [ChoiceInline]
##    list_display = ('item_id','item_in_stock','item_sold')

##class InvAdmin(admin.ModelAdmin):
##    list_display = ('item_id', 'item_in_stock', 'item_sold')
##    # list_display_links = ('item_id__item_name', 'item_id__item_category')
##    list_filter = ('item_id','item_sold')
##    list_editable = ('item_sold', 'item_in_stock')

# class ReStockListFilter(SimpleListFilter):
#     # Human-readable title which will be displayed in the
#     # right admin sidebar just above the filter options.
#     title = _('In Stock')

#     # Parameter for the filter that will be used in the URL query.
#     parameter_name = 'id'

#     def lookups(self, request, model_admin):
#         """
#         Returns a list of tuples. The first element in each
#         tuple is the coded value for the option that will
#         appear in the URL query. The second element is the
#         human-readable name for the option that will appear
#         in the right sidebar.
#         """
#         return (
#             ('20', ('quantity_on_hand')),
#         )

##    def queryset(self, request, queryset):
##        """
##        Returns the filtered queryset based on the value
##        provided in the query string and retrievable via
##        `self.value()`.
##        """
##        # Compare the requested value (either '80s' or '90s')
##        # to decide how to filter the queryset.
##        return InventoryProduct.objects.get(InventoryProduct.quantity_on_hand>20)

# class InvAdmin(admin.ModelAdmin):
    # ordering = ('item_id__item_name',)
    # search_fields = ['item_id__item_id','item_id__item_name',]
    # list_display = ('item_in_stock','item_sold',)
    # list_display_links = ('customer_admin_link',)
    # list_per_page = 20
    # prepopulated_fields = {"item_in_stock": ("item_in_stock",)}
    # list_filter = ('item_id__item_id', 'item_id__item_name',)
    # inlines = [ItemInline,]

# class InvAdmin(UserAdmin):
    # list_filter = ('item_id',)

# admin.site.register(Inventory, InvAdmin)
# admin.site.register(Item)

from django.contrib.contenttypes import generic

class InventoryProductInline(admin.StackedInline):
    model = InventoryProduct
    max_num = 1
    formset = RequireOneFormSet

class ProductAdmin(admin.ModelAdmin):
    inlines = [InventoryProductInline,]
    list_display = ('product_name','product_unit_price','product_sell_price')
    search_fields = ['product_name']
    list_filter = ('product_category',)

class InventoryProductAdmin(admin.ModelAdmin):
    search_fields = ['product__product_name',]
    list_display = ('inventory','product','quantity_on_hand','quantity_sold',)
    list_filter = ('inventory__inventory_name','product__product_category',)


admin.site.register(Category)
admin.site.register(Inventory)
admin.site.register(Product_Reports)
admin.site.register(Product, ProductAdmin)
admin.site.register(InventoryProduct,InventoryProductAdmin)

