# Generated by Django 3.1.7 on 2021-03-01 15:04

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Cards', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='card',
            options={'ordering': ['created_at'], 'verbose_name': 'Карточка', 'verbose_name_plural': 'Карточки'},
        ),
        migrations.AddField(
            model_name='card',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
