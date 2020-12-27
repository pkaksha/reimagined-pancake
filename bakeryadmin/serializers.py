from rest_framework import serializers
from .models import *


class AddIngredientSerializer(serializers.Serializer):
    Ingredient_Name = serializers.CharField()

    def create(self, validated_data):

        existing = IngredientListModel.objects.filter(Ingredient_Name=validated_data['Ingredient_Name']).values()
        if len(existing) == 0:
            IngredientListModel.objects.create(**validated_data)
            response = "Ingredient Added to List"
        else:
            response = "Item Already Exist"
        return {"Response": response}


class AddInventoryItemSerializer(serializers.Serializer):
    Ingredient_ID = serializers.PrimaryKeyRelatedField(queryset=IngredientListModel.objects.all(), write_only=True)
    Quantity = serializers.IntegerField()
    QuantityUnit = serializers.CharField()
    price = serializers.IntegerField()
    UnitInPricePerUnit = serializers.CharField()

    def create(self, validated_data):
        existing = IngredientInventoryModel.objects.filter(Ingredient_ID=validated_data['Ingredient_ID']).values()
        if len(existing) == 0:
            IngredientInventoryModel.objects.create(**validated_data)
            response = "Item Added to Inventory list with quantity and price details"

        else:
            response = "Item Already Exist"
        return {"Response":response}


class UpdateInventorySerializer(serializers.ModelSerializer):
    QuantityUnit = serializers.ReadOnlyField()
    UnitInPricePerUnit = serializers.ReadOnlyField()
    Quantity = serializers.IntegerField()
    price = serializers.FloatField(required=False)
    type = serializers.CharField()

    class Meta:
        model = IngredientInventoryModel
        fields = ['Quantity', 'QuantityUnit', 'price', 'UnitInPricePerUnit', 'type', ]

    def update(self, instance, validated_data):
        if validated_data['type'] == 'Add':
            origin_quantity = instance.Quantity
            instance.Quantity = instance.Quantity + validated_data['Quantity']
            instance.price = (instance.price * origin_quantity + validated_data['price'] * validated_data[
                'Quantity']) / (
                                     origin_quantity + validated_data['Quantity'])

            instance.save()

        if validated_data['type'] == 'Subtract':
            instance.Quantity = instance.Quantity - validated_data['Quantity']
            if instance.Quantity < 0:
                instance.Quantity = 0
            else:
                instance.Quantity = instance.Quantity

            instance.save()

        if validated_data['type'] == 'Replace':
            instance.Quantity = validated_data['Quantity']
            instance.price = validated_data['price']

            instance.save()

        return instance


class CookItemSerializer(serializers.ModelSerializer):
    Bakery_Item_Name = serializers.CharField()
    IngredientComposition = serializers.DictField()
    Item_quantity = serializers.IntegerField()

    class Meta:
        model = BakeryItems
        fields = ['Bakery_Item_Name', 'IngredientComposition', 'Item_quantity', ]

    def create(self, validated_data):

        response = ""
        cost_price = 0
        remaining_quantity_list = []

        existing = BakeryItems.objects.filter(Bakery_Item_Name=validated_data['Bakery_Item_Name']).values()
        for key, value in validated_data['IngredientComposition'].items():
            Ing_ID = list(IngredientListModel.objects.filter(
                Ingredient_Name__iexact=key).values('id'))[0]['id']
            Inv_Quantity = list(IngredientInventoryModel.objects.filter(Ingredient_ID_id=Ing_ID).values('Quantity'))[0][
                'Quantity']
            Inv_price = list(IngredientInventoryModel.objects.filter(Ingredient_ID_id=Ing_ID).values('price'))[0][
                'price']
            remaining_quantiy = Inv_Quantity - validated_data['Item_quantity'] * value[0]
            remaining_quantity_list.append(remaining_quantiy)

            cost_price = cost_price + value[0] * Inv_price

        if any(i < 0 for i in remaining_quantity_list):
            response = "Please Check for required Stock, Some or All of Stock is not sufficient to Cook the item"

        elif len(existing) == 0 & all(i >= 0 for i in remaining_quantity_list):
            validated_data['Cost_price'] = cost_price
            validated_data['Sell_price'] = cost_price + cost_price * 0.4

            BakeryItems.objects.create(**validated_data)
            for key, value in validated_data['IngredientComposition'].items():
                Ing_ID = list(IngredientListModel.objects.filter(
                    Ingredient_Name__iexact=key).values('id'))[0]['id']
                Inv_id = list(IngredientInventoryModel.objects.filter(Ingredient_ID_id=Ing_ID).values('id'))[0][
                    'id']
                Inv_Quantity = \
                    list(IngredientInventoryModel.objects.filter(Ingredient_ID_id=Ing_ID).values('Quantity'))[0][
                        'Quantity']

                updated_quantiy = Inv_Quantity - validated_data['Item_quantity'] * value[0]

                IngredientInventoryModel.objects.filter(id=Inv_id).update(Quantity=updated_quantiy)

            response = "Baked. Enjoy ;)"

        elif len(existing) > 0 & all(i >= 0 for i in remaining_quantity_list):
            validated_data['Cost_price'] = cost_price
            validated_data['Sell_price'] = cost_price + cost_price * 0.4
            BakeryItems.objects.filter(Bakery_Item_Name=validated_data['Bakery_Item_Name']).update(**validated_data)
            for key, value in validated_data['IngredientComposition'].items():
                Ing_ID = list(IngredientListModel.objects.filter(
                    Ingredient_Name__iexact=key).values('id'))[0]['id']
                Inv_id = list(IngredientInventoryModel.objects.filter(Ingredient_ID_id=Ing_ID).values('id'))[0][
                    'id']
                Inv_Quantity = \
                    list(IngredientInventoryModel.objects.filter(Ingredient_ID_id=Ing_ID).values('Quantity'))[0][
                        'Quantity']

                updated_quantiy = Inv_Quantity - validated_data['Item_quantity'] * value[0]

                IngredientInventoryModel.objects.filter(id=Inv_id).update(Quantity=updated_quantiy)
            response = "Baked. Enjoy ;)"

        return {"Response": response}


class GetBakeryItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = BakeryItems
        fields = ['Bakery_Item_Name', 'IngredientComposition', 'Item_quantity', 'Cost_price', 'Sell_price']


class GetPopularItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = BakeryItems
        fields = ['Bakery_Item_Name', 'Sold_count']