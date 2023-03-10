# Generated by Django 4.1.5 on 2023-01-08 15:05

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Prize',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prize_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('img', models.FileField(max_length=255, upload_to='team/prize/')),
                ('text', models.TextField(default='', max_length=255)),
            ],
        ),
    ]
