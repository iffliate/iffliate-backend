# Generated by Django 4.0 on 2022-10-29 17:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='shop',
            name='phone',
            field=models.CharField(default='090...', max_length=255),
        ),
    ]
