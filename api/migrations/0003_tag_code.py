# Generated by Django 4.0 on 2021-12-12 06:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_purchasehistory_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='tag',
            name='code',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]
