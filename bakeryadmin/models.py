from __future__ import unicode_literals
from django.db import models

CHOICE_UNITS = (('Ltr', 'Ltr'), ('Kg', 'Kg'), ('Dozen', 'Dozen'), ('Piece', 'Piece'))


class IngredientListModel(models.Model):
    created = models.DateTimeField(auto_now_add=True, null=False, blank=False)
    Ingredient_Name = models.CharField(max_length=100)


class IngredientInventoryModel(models.Model):
    created = models.DateTimeField(auto_now_add=True, null=False, blank=False)
    # Ingredient_Name = models.CharField(max_length=100)
    Ingredient_ID = models.ForeignKey(IngredientListModel,
                                      related_name='inventory',
                                      on_delete=models.CASCADE)
    Quantity = models.FloatField()
    QuantityUnit = models.CharField(max_length=20, choices=CHOICE_UNITS)
    price = models.FloatField()
    UnitInPricePerUnit = models.CharField(max_length=20, choices=CHOICE_UNITS)

    def type(self):
        return ''


class BakeryItems(models.Model):
    created = models.DateTimeField(auto_now_add=True, null=False, blank=False)
    Bakery_Item_Name = models.CharField(max_length=100)
    IngredientComposition = models.JSONField(default=dict)
    Item_quantity = models.IntegerField()
    Cost_price = models.FloatField()
    Sell_price = models.FloatField()
    Sold_count = models.IntegerField(default=0)

