# Generated by Django 5.1.4 on 2025-01-19 08:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='city',
        ),
        migrations.RemoveField(
            model_name='user',
            name='pincode',
        ),
        migrations.RemoveField(
            model_name='user',
            name='state',
        ),
        migrations.RemoveField(
            model_name='user',
            name='street',
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(blank=True, max_length=50, null=True)),
                ('pincode', models.CharField(blank=True, max_length=10, null=True)),
                ('state', models.CharField(blank=True, max_length=50, null=True)),
                ('street', models.CharField(blank=True, max_length=255, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='addresses', to='api.user')),
            ],
        ),
    ]
