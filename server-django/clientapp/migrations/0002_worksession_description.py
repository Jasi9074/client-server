# Generated by Django 5.0.7 on 2024-08-31 16:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clientapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='worksession',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
