# Generated by Django 4.1.1 on 2022-10-10 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_alter_user_first_name_alter_user_last_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='shipping_address',
            field=models.TextField(default='nil'),
        ),
    ]
