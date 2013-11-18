from django.db import models
from django.utils import timezone
from fields import CurrencyField
from decimal import Decimal
import datetime

class Category(models.Model):
    product_category = models.CharField(max_length=200, unique=True)
    def __unicode__(self):
        return self.product_category

class Inventory(models.Model):
    inventory_name = models.CharField(max_length=200)
    def __unicode__(self):
        return self.inventory_name

class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_category = models.ForeignKey(Category, db_column="product_category")
    product_name = models.CharField(max_length=200)
    product_unit_price = CurrencyField()
    product_sell_price = CurrencyField()
    product_description = models.TextField(default="None")

    def __unicode__(self):
        return unicode(self.product_name)

class InventoryProduct(models.Model):
    inventory = models.ForeignKey(Inventory)
    product = models.ForeignKey(Product)
    quantity_on_hand = models.IntegerField(default=0)
    quantity_sold = models.IntegerField(default=0)
    
    def __unicode__(self):
        # return unicode(unicode(self.inventory) + " - " + unicode(self.product))
        return unicode(self.product)
        

from django.http import HttpResponse

# class Product_Reports(models.Model):
#     report_date = models.DateField(auto_now=True)
#     product = models.ForeignKey(InventoryProduct)
#     total_quantity_sold = models.IntegerField(blank=True, null=True)
#     total_sell_amt_earned = CurrencyField(blank=True, null=True)
#     total_unit_amt_earned = CurrencyField(blank=True, null=True)
#     total_profit_earned = CurrencyField(blank=True, null=True)

class Product_Reports(models.Model):
    report_date = models.DateField(auto_now=True)
    product = models.ForeignKey(InventoryProduct)
    total_quantity_sold = models.IntegerField(blank=True, null=True)
    total_sell_amt_earned = models.IntegerField(blank=True, null=True)
    total_unit_amt_earned = models.IntegerField(blank=True, null=True)
    total_profit_earned = models.IntegerField(blank=True, null=True)



# class Product_Reports(models.Model):
#     report_date = models.DateField(auto_now=True)
#     product = models.ForeignKey(InventoryProduct)
#     total_quantity_sold = models.IntegerField(blank=True, null=True)
#     total_sell_amt_earned = models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=2)
#     total_unit_amt_earned = models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=2)
#     total_profit_earned = models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=2)

    # if product is not None:
    # def _get_qs(self):
    #     "Returns quantity_sold"
    #     return self.product.quantity_sold

    # def _get_up(self):
    #     "Return Unit Price"
    #     return self.product.product.product_unit_price * self.product.quantity_sold

    # def _get_sp(self):
    #     "Return Sell Price"
    #     return self.product.product.product_sell_price * self.product.quantity_sold

    # def _get_profit():
    #     "Return Profit"
    #     return total_sell_amt_earned - total_unit_amt_earned

        # total_quantity_sold = property(_get_qs)
        # total_unit_amt_earned = property(_get_up)
        # total_sell_amt_earned = property(_get_sp)
        # total_profit_earned = property(_get_profit)

        # this is not needed if small_image is created at set_image
    # def save(self, *args, **kwargs):
    #     # if getattr(self, '_image_changed', True):
    #     #     small=rescale_image(self.image,width=100,height=100)
    #     #     self.image_small=SimpleUploadedFile(name,small_pic)
        
    #     for each in InventoryProduct.objects.all():
    #         reports=Product_Reports(product=each)
    #         if reports.product is not None:
    #             reports.total_quantity_sold = reports.product.quantity_sold
    #             reports.total_sell_amt_earned = reports.product.product.product_sell_price * reports.total_quantity_sold
    #             reports.total_unit_amt_earned = reports.product.product.product_unit_price * reports.total_quantity_sold
    #             reports.total_profit_earned = reports.total_sell_amt_earned - reports.total_unit_amt_earned
    #             reports.save()
    #     super(Product_Reports, self).save(*args, **kwargs) 


# from inventory.models import InventoryProduct, Product_Reports
# x = Product_Reports
# x.save()

    def __unicode__(self):
        return unicode(self.product)




