# Generated by Django 5.1 on 2024-09-03 16:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('advertisement', '0002_alter_advertisement_author'),
    ]

    operations = [
        migrations.AlterField(
            model_name='advertisement',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='advertisement.author'),
        ),
    ]
