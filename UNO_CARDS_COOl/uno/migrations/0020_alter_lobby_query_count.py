# Generated by Django 4.2.2 on 2023-06-20 15:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('uno', '0019_alter_lobby_player_count_alter_lobby_query_count'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lobby',
            name='Query_Count',
            field=models.CharField(default='0', max_length=20, verbose_name='количество запросов'),
        ),
    ]
