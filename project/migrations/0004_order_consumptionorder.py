# Generated by Django 5.1.3 on 2024-11-21 21:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0003_alter_music_genres'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='consumptionOrder',
            field=models.BooleanField(blank=True, null=True),
        ),
    ]
