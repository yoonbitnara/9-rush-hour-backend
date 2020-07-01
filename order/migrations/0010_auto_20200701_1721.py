# Generated by Django 3.0.7 on 2020-07-01 17:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_auto_20200625_2106'),
        ('order', '0009_order_price'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShippingList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('recipient', models.CharField(max_length=50)),
                ('address', models.CharField(max_length=300)),
                ('phone_no', models.CharField(max_length=100, null=True)),
                ('default', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shipping_info', to='user.UserInfo')),
            ],
            options={
                'db_table': 'shipping_lists',
            },
        ),
        migrations.DeleteModel(
            name='Shipping',
        ),
        migrations.AddField(
            model_name='shippinginfo',
            name='shipping_list',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='order.ShippingList'),
        ),
    ]
