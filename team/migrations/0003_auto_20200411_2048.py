# Generated by Django 2.2 on 2020-04-11 15:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('team', '0002_team_timestamp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='slug',
            field=models.SlugField(blank=True, max_length=100, null=True, unique=True),
        ),
    ]