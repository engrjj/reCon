# Generated by Django 3.2.20 on 2023-08-07 10:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contractors', '0004_photos_caption'),
    ]

    operations = [
        migrations.AddField(
            model_name='contractor',
            name='company_description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='contractor',
            name='logo',
            field=models.ImageField(blank=True, null=True, upload_to='logos/'),
        ),
    ]
