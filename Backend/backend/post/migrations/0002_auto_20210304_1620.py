# Generated by Django 3.1.5 on 2021-03-04 10:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='author',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
