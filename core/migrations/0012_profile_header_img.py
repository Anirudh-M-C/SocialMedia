# Generated by Django 3.2.20 on 2024-06-13 09:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='header_img',
            field=models.ImageField(blank=True, default='blank-header-image.webp', upload_to='header_images'),
        ),
    ]
