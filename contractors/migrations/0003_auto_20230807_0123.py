# Generated by Django 3.2.20 on 2023-08-06 17:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contractors', '0002_project_project_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photos',
            name='contractor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='photos', to='contractors.contractor'),
        ),
        migrations.AlterField(
            model_name='photos',
            name='project',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='photos', to='contractors.project'),
        ),
        migrations.AlterField(
            model_name='photos',
            name='update',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='photos', to='contractors.update'),
        ),
    ]
