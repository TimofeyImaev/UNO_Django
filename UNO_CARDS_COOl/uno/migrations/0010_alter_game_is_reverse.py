# Generated by Django 4.2.2 on 2023-06-11 07:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('uno', '0009_winner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='is_reverse',
            field=models.IntegerField(default=1, max_length=10),
        ),
    ]
