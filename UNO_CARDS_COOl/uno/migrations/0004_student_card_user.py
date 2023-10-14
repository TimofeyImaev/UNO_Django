# Generated by Django 4.2.2 on 2023-06-10 04:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('uno', '0003_rename_cards_card'),
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Имя')),
            ],
        ),
        migrations.AddField(
            model_name='card',
            name='user',
            field=models.CharField(default=1, max_length=20, verbose_name='user'),
            preserve_default=False,
        ),
    ]
