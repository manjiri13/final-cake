# Generated by Django 3.1.2 on 2020-12-07 14:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0012_auto_20201207_2008'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='price',
            field=models.DecimalField(decimal_places=2, default=199, max_digits=6),
        ),
    ]
