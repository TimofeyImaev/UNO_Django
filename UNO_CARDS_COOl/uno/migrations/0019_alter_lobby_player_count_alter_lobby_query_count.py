# Generated by Django 4.2.2 on 2023-06-20 15:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('uno', '0018_lobby_query_count_lobby_query1_lobby_query2_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lobby',
            name='Player_Count',
            field=models.CharField(default='1', max_length=20, verbose_name='количество игроков'),
        ),
        migrations.AlterField(
            model_name='lobby',
            name='Query_Count',
            field=models.CharField(default='1', max_length=20, verbose_name='количество запросов'),
        ),
    ]