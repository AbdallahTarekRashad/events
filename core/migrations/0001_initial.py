# Generated by Django 3.1.5 on 2021-01-20 08:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, verbose_name='title')),
                ('description', models.CharField(max_length=500, verbose_name='description')),
                ('date', models.DateField(verbose_name='date')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='my_events', to=settings.AUTH_USER_MODEL, verbose_name='owner')),
                ('participants', models.ManyToManyField(related_name='signup_events', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Event',
                'verbose_name_plural': 'Events',
            },
        ),
    ]
