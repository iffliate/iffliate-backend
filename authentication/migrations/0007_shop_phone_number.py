# Generated by Django 4.0 on 2022-12-18 19:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0006_alter_shop_account_holder_email_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='shop',
            name='phone_number',
            field=models.CharField(default='081', max_length=14),
        ),
    ]
