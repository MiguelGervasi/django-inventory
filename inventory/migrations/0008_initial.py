# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Category'
        db.create_table(u'inventory_category', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('product_category', self.gf('django.db.models.fields.CharField')(unique=True, max_length=200)),
        ))
        db.send_create_signal(u'inventory', ['Category'])

        # Adding model 'Inventory'
        db.create_table(u'inventory_inventory', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('inventory_name', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal(u'inventory', ['Inventory'])

        # Adding model 'Product'
        db.create_table(u'inventory_product', (
            ('product_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('product_category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['inventory.Category'], db_column='product_category')),
            ('product_name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('product_unit_price', self.gf('inventory.fields.CurrencyField')(max_digits=10, decimal_places=2)),
            ('product_sell_price', self.gf('inventory.fields.CurrencyField')(max_digits=10, decimal_places=2)),
            ('product_description', self.gf('django.db.models.fields.TextField')(default='None')),
        ))
        db.send_create_signal(u'inventory', ['Product'])

        # Adding model 'InventoryProduct'
        db.create_table(u'inventory_inventoryproduct', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('inventory', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['inventory.Inventory'])),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['inventory.Product'])),
            ('quantity_on_hand', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('quantity_sold', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'inventory', ['InventoryProduct'])

        # Adding model 'Product_Reports'
        db.create_table(u'inventory_product_reports', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('report_date', self.gf('django.db.models.fields.DateField')(auto_now=True, blank=True)),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['inventory.InventoryProduct'])),
            ('total_quantity_sold', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('total_sell_amt_earned', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('total_unit_amt_earned', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('total_profit_earned', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'inventory', ['Product_Reports'])


    def backwards(self, orm):
        # Deleting model 'Category'
        db.delete_table(u'inventory_category')

        # Deleting model 'Inventory'
        db.delete_table(u'inventory_inventory')

        # Deleting model 'Product'
        db.delete_table(u'inventory_product')

        # Deleting model 'InventoryProduct'
        db.delete_table(u'inventory_inventoryproduct')

        # Deleting model 'Product_Reports'
        db.delete_table(u'inventory_product_reports')


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