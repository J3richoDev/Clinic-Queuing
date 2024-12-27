# Generated by Django 5.1.3 on 2024-12-08 01:01

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0007_alter_project_color'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='assigned_members',
            field=models.ManyToManyField(blank=True, related_name='tasks', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='ProjectTeam',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('color', models.CharField(choices=[('purple', 'Purple'), ('red', 'Red'), ('amber', 'Amber'), ('blue', 'Blue'), ('green', 'Green'), ('teal', 'Teal'), ('yellow', 'Yellow'), ('orange', 'Orange'), ('pink', 'Pink'), ('gray', 'Grey')], default='blue', max_length=20)),
                ('members', models.ManyToManyField(related_name='teams', to=settings.AUTH_USER_MODEL)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='teams', to='projects.project')),
            ],
        ),
        migrations.AddField(
            model_name='task',
            name='assigned_teams',
            field=models.ManyToManyField(blank=True, related_name='tasks', to='projects.projectteam'),
        ),
        migrations.CreateModel(
            name='Sprint',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sprints', to='projects.project')),
            ],
        ),
        migrations.AddField(
            model_name='task',
            name='sprint',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to='projects.sprint'),
        ),
    ]