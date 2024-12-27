# Generated by Django 5.1.3 on 2024-12-13 08:03

import users.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_alter_customuser_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='profile_picture',
            field=models.ImageField(blank=True, null=True, upload_to='profile_pictures/', validators=[users.models.validate_profile_picture]),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='role',
            field=models.CharField(choices=[('member', 'Member'), ('manager', 'Manager')], default='manager', max_length=10),
        ),
    ]
