# Generated by Django 5.0.7 on 2024-09-12 07:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clientapp', '0006_worksession_machine'),
    ]

    operations = [
        migrations.AddField(
            model_name='worksession',
            name='complaint',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
