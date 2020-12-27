from datetime import datetime

from rest_framework import serializers

from .models import *


class GetBakeryAvailableProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BakeryItems
        fields = ['Bakery_Item_Name', 'Item_quantity', 'Sell_price']


class CreateAddressDetailsSerializer(serializers.Serializer):

    cust_id = serializers.PrimaryKeyRelatedField(queryset=UserProfileModel.objects.all(), write_only=True)
    Street_Address = serializers.CharField()
    City = serializers.CharField()
    Pincode = serializers.IntegerField()
    State = serializers.CharField()
    phone_number = serializers.CharField()
    address_type = serializers.CharField()

    def create(self, validated_data):
        print(validated_data)

        CustomerAddressDetails.objects.create(**validated_data)

        response = "Address Details Added"

        return {"Response": response}


class GetAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerAddressDetails
        fields = ['Street_Address', 'City', 'Pincode', 'State', 'phone_number', 'address_type']


class PlaceOrderSerializer(serializers.Serializer):
    cust_id = serializers.PrimaryKeyRelatedField(queryset=UserProfileModel.objects.all(), write_only=True)
    address_id = serializers.PrimaryKeyRelatedField(queryset=CustomerAddressDetails.objects.all(), write_only=True)
    Bakery_item_id = serializers.PrimaryKeyRelatedField(queryset=BakeryItems.objects.all(), write_only=True)
    Ordered_Quantity = serializers.IntegerField()

    def create(self, validated_data):
        print(validated_data)

        iq = list(BakeryItems.objects.filter(id=validated_data['Bakery_item_id'].id).values('Item_quantity'))[0][
            'Item_quantity']

        if iq >= validated_data['Ordered_Quantity']:

            cust_id = str(validated_data['cust_id'].id)
            date_today = str(datetime.now().strftime("%d%m%Y%H%M"))
            order_no = "ZB-ORDER" + cust_id + date_today

            iq = list(BakeryItems.objects.filter(id=validated_data['Bakery_item_id'].id).values('Item_quantity'))[0][
                'Item_quantity']

            item_name = list(BakeryItems.objects.filter(id=validated_data['Bakery_item_id'].id).values(
                'Bakery_Item_Name'))[0][
                'Bakery_Item_Name']
            ordercount = OrderParticularsModel.objects.filter(cust_id=validated_data['cust_id']).values()
            sp = list(BakeryItems.objects.filter(id=validated_data['Bakery_item_id'].id).values('Sell_price'))[0][
                'Sell_price']

            # BONUS POINT 3
            # Discount of 25% is given to First Time Customers

            if len(ordercount) == 0:
                sp = sp - sp * 0.25
            else:
                sp = sp

            total = validated_data['Ordered_Quantity'] * sp

            OrderParticularsModel.objects.create(cust_id=validated_data['cust_id'],
                                                 address_id=validated_data['address_id'],
                                                 Bakery_item_id=validated_data['Bakery_item_id'],
                                                 Total=total, Ordered_Quantity=validated_data['Ordered_Quantity'],
                                                 order_no=order_no)

            sc = list(BakeryItems.objects.filter(id=validated_data['Bakery_item_id'].id).values('Sold_count'))[0][
                'Sold_count']
            updated_sc = sc + validated_data['Ordered_Quantity']
            updated_iq = iq - validated_data['Ordered_Quantity']

            BakeryItems.objects.filter(id=validated_data['Bakery_item_id'].id).update(Sold_count=updated_sc,
                                                                                      Item_quantity=updated_iq)

            return {"Response": "Order Placed for " + item_name + "," + "with order id " + order_no}

        elif iq < validated_data['Ordered_Quantity']:

            item_name = list(BakeryItems.objects.filter(id=validated_data['Bakery_item_id'].id).values(
                'Bakery_Item_Name'))[0][
                'Bakery_Item_Name']

            return {"Response": "Order Can't be Placed for " + item_name}


class GetOrderBillSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderParticularsModel
        fields = ['created', 'first_name', 'last_name', 'phone_number', 'Bakery_Item_Name', 'order_no',
                  'Ordered_Quantity', 'Total',
                  'Street_Address', 'City', 'Pincode',
                  'State', 'Total_Amount']