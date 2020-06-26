# Generated by Django 3.0.7 on 2020-06-25 15:16

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(max_length=50, null=True)),
                ('password', models.CharField(max_length=100)),
                ('nickname', models.CharField(max_length=50, null=True)),
                ('email', models.EmailField(max_length=200)),
                ('name', models.CharField(max_length=50)),
                ('phone_no', models.CharField(max_length=50)),
                ('address', models.CharField(max_length=300)),
                ('marketing_agreed', models.BooleanField(default=False)),
                ('is_guest', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'users',
            },
        ),
    ]
