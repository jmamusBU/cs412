# Generated by Django 5.1.2 on 2024-10-17 15:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_article_image_url'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='image_url',
        ),
        migrations.AddField(
            model_name='article',
            name='image_file',
            field=models.ImageField(blank=True, upload_to=''),
        ),
    ]