# Generated by Django 5.1.2 on 2024-11-09 20:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('voter_analytics', '0004_alter_voter_precinct'),
    ]

    operations = [
        migrations.AlterField(
            model_name='voter',
            name='state',
            field=models.BooleanField(),
        ),
    ]
