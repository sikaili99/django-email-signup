# Generated by Django 4.0 on 2022-11-25 10:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_customuser_email_verified_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='email_verified_hash',
            field=models.CharField(default='01', max_length=200),
        ),
    ]
