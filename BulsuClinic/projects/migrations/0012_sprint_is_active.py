# Generated by Django 5.1.3 on 2024-12-11 11:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0011_alter_project_color_alter_project_emoji_icon'),
    ]

    operations = [
        migrations.AddField(
            model_name='sprint',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
    ]
