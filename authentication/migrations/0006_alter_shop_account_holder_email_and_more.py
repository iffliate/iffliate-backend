# Generated by Django 4.0 on 2022-12-04 17:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0005_remove_shop_paystack_recipient'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shop',
            name='account_holder_email',
            field=models.EmailField(default='nil@mail.com', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='shop',
            name='account_holder_name',
            field=models.CharField(default='..', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='shop',
            name='account_number',
            field=models.CharField(default='..', max_length=255, null=True),
        ),
    ]
