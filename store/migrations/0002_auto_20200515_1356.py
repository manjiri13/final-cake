# Generated by Django 3.0.3 on 2020-05-15 08:26

from django.db import migrations


class Migration(migrations.Migration):
    atomic = False
    
    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ProductDetails',
            new_name='ProductDetail',
        ),
    ]
