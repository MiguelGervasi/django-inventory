from django.db import models
from django.forms import ModelForm, Form
from django.forms.models import inlineformset_factory, BaseInlineFormSet
from inventory.models import Inventory, Product, InventoryProduct, Category, Inventory, Product_Reports

class ProductForm(ModelForm):
    class Meta:
        model = Product

class InventoryProductForm(ModelForm):
    class Meta:
        model = InventoryProduct

class CategoryForm(ModelForm):
    class Meta:
        model = Category

class InventoryForm(ModelForm):
    class Meta:
        model = Inventory

class ProductReportsForm(ModelForm):
	class Meta:
		model = Product_Reports

ProdInvFormSet = inlineformset_factory(Product, InventoryProduct, max_num=1, exclude=("product",), can_delete=False)
    

__all__ = ('RequireOneFormSet',)

class RequireOneFormSet(BaseInlineFormSet):
    """Require at least one form in the formset to be completed."""
    def clean(self):
        """Check that at least one form has been completed."""
        super(RequireOneFormSet, self).clean()
        for error in self.errors:
            if error:
                return
        completed = 0
        for cleaned_data in self.cleaned_data:
            # form has data and we aren't deleting it.
            if cleaned_data and not cleaned_data.get('DELETE', False):
                completed += 1

        if completed < 1:
            raise forms.ValidationError("At least one %s is required." %
                self.model._meta.object_name.lower())