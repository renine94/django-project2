# Generated by Django 4.1.6 on 2023-02-10 08:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_user_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='confirm_code',
            field=models.CharField(max_length=6, null=True, unique=True, verbose_name='임시코드'),
        ),
    ]
