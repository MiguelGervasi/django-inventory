# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Product_Reports.total_sell_amt_earned'
        db.alter_column(u'inventory_product_reports', 'total_sell_amt_earned', self.gf('django.db.models.fields.IntegerField')(null=True))

        # Changing field 'Product_Reports.total_unit_amt_earned'
        db.alter_column(u'inventory_product_reports', 'total_unit_amt_earned', self.gf('django.db.models.fields.IntegerField')(null=True))

        # Changing field 'Product_Reports.total_profit_earned'
        db.alter_column(u'inventory_product_reports', 'total_profit_earned', self.gf('django.db.models.fields.IntegerField')(null=True))

    def backwards(self, orm):

        # Changing field 'Product_Reports.total_sell_amt_earned'
        db.alter_column(u'inventory_product_reports', 'total_sell_amt_earned', self.gf('inventory.fields.CurrencyField')(null=True, max_digits=10, decimal_places=2))

        # Changing field 'Product_Reports.total_unit_amt_earned'
        db.alter_column(u'inventory_product_reports', 'total_unit_amt_earned', self.gf('inventory.fields.CurrencyField')(null=True, max_digits=10, decimal_places=2))

        # Changing field 'Product_Reports.total_profit_earned'
        db.alter_column(u'inventory_product_reports', 'total_profit_earned', self.gf('inventory.fields.CurrencyField')(null=True, max_digits=10, decimal_places=2))

    models = {
        u'inventory.category': {
            'Meta': {'object_name': 'Category'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'product_category': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'})
        },
        u'inventory.inventory': {
            'Meta': {'object_name': 'Inventory'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inventory_name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'inventory.inventoryproduct': {
            'Meta': {'object_name': 'InventoryProduct'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inventory': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['inventory.Inventory']"}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['inventory.Product']"}),
            'quantity_on_hand': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'quantity_sold': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'inventory.monthlyweatherbycity': {
            'Meta': {'object_name': 'MonthlyWeatherByCity'},
            'boston_temp': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '1'}),
            'houston_temp': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '1'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'month': ('django.db.models.fields.IntegerField', [], {})
        },
        u'inventory.product': {
            'Meta': {'object_name': 'Product'},
            'product_category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['inventory.Category']", 'db_column': "'product_category'"}),
            'product_description': ('django.db.models.fields.TextField', [], {'default': "'None'"}),
            'product_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'product_name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'product_sell_price': ('inventory.fields.CurrencyField', [], {'max_digits': '10', 'decimal_places': '2'}),
            'product_unit_price': ('inventory.fields.CurrencyField', [], {'max_digits': '10', 'decimal_places': '2'})
        },
        u'inventory.product_reports': {
            'Meta': {'object_name': 'Product_Reports'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['inventory.InventoryProduct']"}),
            'report_date': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'}),
            'total_profit_earned': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'total_quantity_sold': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'total_sell_amt_earned': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'total_unit_amt_earned': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['inventory']