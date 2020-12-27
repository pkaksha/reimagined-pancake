from django.core.validators import *
from phonenumber_field.modelfields import *

from bakeryadmin.models import *
from registerlogin.models import UserProfileModel

# Create your models here.
address_choices = (("Home", "Home"), ("Office", "Office"), ("Others", "Others"))
states_choices = (("AN", "Andaman and Nicobar Islands"),
                  ("AP", "Andhra Pradesh"),
                  ("AR", "Arunachal Pradesh"),
                  ("AS", "Assam"),
                  ("BR", "Bihar"),
                  ("CG", "Chhattisgarh"),
                  ("CH", "Chandigarh"),
                  ("DN", "Dadra and Nagar Haveli"),
                  ("DD", "Daman and Diu"),
                  ("DL", "Delhi"),
                  ("GA", "Goa"),
                  ("GJ", "Gujarat"),
                  ("HR", "Haryana"),
                  ("HP", "Himachal Pradesh"),
                  ("JK", "Jammu and Kashmir"),
                  ("JH", "Jharkhand"),
                  ("KA", "Karnataka"),
                  ("KL", "Kerala"),
                  ("LA", "Ladakh"),
                  ("LD", "Lakshadweep"),
                  ("MP", "Madhya Pradesh"),
                  ("MH", "Maharashtra"),
                  ("MN", "Manipur"),
                  ("ML", "Meghalaya"),
                  ("MZ", "Mizoram"),
                  ("NL", "Nagaland"),
                  ("OD", "Odisha"),
                  ("PB", "Punjab"),
                  ("PY", "Pondicherry"),
                  ("RJ", "Rajasthan"),
                  ("SK", "Sikkim"),
                  ("TN", "Tamil Nadu"),
                  ("TS", "Telangana"),
                  ("TR", "Tripura"),
                  ("UP", "Uttar Pradesh"),
                  ("UK", "Uttarakhand"),
                  ("WB", "West Bengal")
                  )


class CustomerAddressDetails(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    cust_id = models.ForeignKey(UserProfileModel,
                                related_name='address',
                                on_delete=models.CASCADE)
    Street_Address = models.TextField()
    City = models.CharField(max_length=50)
    Pincode = models.IntegerField(validators=[MaxLengthValidator(6), MinLengthValidator(6)])
    State = models.CharField(choices=states_choices, max_length=50)
    phone_number = PhoneNumberField(default='0')
    address_type = models.CharField(choices=address_choices, max_length=10, default="Others")


class OrderParticularsModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    order_no = models.CharField(max_length=50, default="")
    cust_id = models.ForeignKey(UserProfileModel,
                                related_name='order',
                                on_delete=models.CASCADE)
    address_id = models.ForeignKey(CustomerAddressDetails,
                                   related_name='order',
                                   on_delete=models.CASCADE)
    Bakery_item_id = models.ForeignKey(BakeryItems,
                                       related_name='order',
                                       on_delete=models.CASCADE)
    Ordered_Quantity = models.IntegerField()
    Total = models.FloatField()

    # Bakery_Item_Name

    def Bakery_Item_Name(self):
        return ''

    def Street_Address(self):
        return ''

    def City(self):
        return ''

    def Pincode(self):
        return ''

    def State(self):
        return ''

    def first_name(self):
        return ''

    def last_name(self):
        return ''

    def phone_number(self):
        return ''

    def Total_Amount(self):
        return ''