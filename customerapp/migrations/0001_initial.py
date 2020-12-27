# Generated by Django 3.1.4 on 2020-12-27 11:40

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('bakeryadmin', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerAddressDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('Street_Address', models.TextField()),
                ('City', models.CharField(max_length=50)),
                ('Pincode', models.IntegerField(validators=[django.core.validators.MaxLengthValidator(6), django.core.validators.MinLengthValidator(6)])),
                ('State', models.CharField(choices=[('AN', 'Andaman and Nicobar Islands'), ('AP', 'Andhra Pradesh'), ('AR', 'Arunachal Pradesh'), ('AS', 'Assam'), ('BR', 'Bihar'), ('CG', 'Chhattisgarh'), ('CH', 'Chandigarh'), ('DN', 'Dadra and Nagar Haveli'), ('DD', 'Daman and Diu'), ('DL', 'Delhi'), ('GA', 'Goa'), ('GJ', 'Gujarat'), ('HR', 'Haryana'), ('HP', 'Himachal Pradesh'), ('JK', 'Jammu and Kashmir'), ('JH', 'Jharkhand'), ('KA', 'Karnataka'), ('KL', 'Kerala'), ('LA', 'Ladakh'), ('LD', 'Lakshadweep'), ('MP', 'Madhya Pradesh'), ('MH', 'Maharashtra'), ('MN', 'Manipur'), ('ML', 'Meghalaya'), ('MZ', 'Mizoram'), ('NL', 'Nagaland'), ('OD', 'Odisha'), ('PB', 'Punjab'), ('PY', 'Pondicherry'), ('RJ', 'Rajasthan'), ('SK', 'Sikkim'), ('TN', 'Tamil Nadu'), ('TS', 'Telangana'), ('TR', 'Tripura'), ('UP', 'Uttar Pradesh'), ('UK', 'Uttarakhand'), ('WB', 'West Bengal')], max_length=50)),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(default='0', max_length=128, region=None)),
                ('address_type', models.CharField(choices=[('Home', 'Home'), ('Office', 'Office'), ('Others', 'Others')], default='Others', max_length=10)),
                ('cust_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='address', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OrderParticularsModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('order_no', models.CharField(default='', max_length=50)),
                ('Ordered_Quantity', models.IntegerField()),
                ('Total', models.FloatField()),
                ('Bakery_item_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order', to='bakeryadmin.bakeryitems')),
                ('address_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order', to='customerapp.customeraddressdetails')),
                ('cust_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
