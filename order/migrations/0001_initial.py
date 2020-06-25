# Generated by Django 3.0.7 on 2020-06-25 16:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0001_initial'),
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_date', models.DateTimeField(auto_now_add=True)),
                ('order_no', models.CharField(max_length=200)),
                ('amount', models.IntegerField()),
                ('message', models.TextField(blank=True)),
            ],
            options={
                'db_table': 'orders',
            },
        ),
        migrations.CreateModel(
            name='OrderStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'status',
            },
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'payments',
            },
        ),
        migrations.CreateModel(
            name='Shpping',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('recipient', models.CharField(max_length=50)),
                ('address', models.CharField(max_length=300)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shpping_info', to='user.UserInfo')),
            ],
            options={
                'db_table': 'shpping',
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order.Order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.Product')),
            ],
            options={
                'db_table': 'order_items',
            },
        ),
        migrations.AddField(
            model_name='order',
            name='order_status',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='order_list', to='order.OrderStatus'),
        ),
        migrations.AddField(
            model_name='order',
            name='payment',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='order.Payment'),
        ),
        migrations.AddField(
            model_name='order',
            name='product',
            field=models.ManyToManyField(related_name='order', through='order.OrderItem', to='product.Product'),
        ),
        migrations.AddField(
            model_name='order',
            name='shopping',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='order.Shpping'),
        ),
        migrations.AddField(
            model_name='order',
            name='user_info',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ordered', to='user.UserInfo'),
        ),
    ]