# Generated by Django 3.2 on 2021-10-02 10:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('buildApp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='gallery',
            name='gallery_row',
            field=models.ImageField(blank=True, null=True, upload_to='gallery'),
        ),
        migrations.AddField(
            model_name='gallery',
            name='gallery_side',
            field=models.ImageField(blank=True, null=True, upload_to='gallery'),
        ),
    ]
