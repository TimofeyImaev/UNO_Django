# Generated by Django 4.2.2 on 2023-06-20 11:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('uno', '0014_student_lobby_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='game_index',
            field=models.CharField(default=1, max_length=20, verbose_name='номер игры'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='student',
            name='game_id',
            field=models.CharField(max_length=20, verbose_name='номер человека в игре'),
        ),
    ]