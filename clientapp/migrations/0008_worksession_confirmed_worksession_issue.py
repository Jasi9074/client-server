# Generated by Django 5.0.7 on 2024-09-19 07:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clientapp', '0007_worksession_complaint'),
    ]

    operations = [
        migrations.AddField(
            model_name='worksession',
            name='confirmed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='worksession',
            name='issue',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
