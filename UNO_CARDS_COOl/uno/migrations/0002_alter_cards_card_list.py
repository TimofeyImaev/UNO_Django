# Generated by Django 4.2.2 on 2023-06-09 12:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('uno', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cards',
            name='card_list',
            field=models.CharField(max_length=100, verbose_name='Рука'),
        ),
    ]
