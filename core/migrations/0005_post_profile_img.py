# Generated by Django 3.2.20 on 2024-06-12 08:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_post_posted_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='Profile_img',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='core.profile'),
            preserve_default=False,
        ),
    ]
