# Generated by Django 3.1.5 on 2021-02-05 10:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_product_sold_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='stock',
            field=models.IntegerField(default=5),
        ),
    ]
