# Generated by Django 3.2.20 on 2024-06-13 10:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_alter_profile_header_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='header_img',
            field=models.ImageField(default='timelineheader.jpg', upload_to='header_images'),
        ),
    ]
