# Generated by Django 2.2 on 2020-04-18 14:14

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('futsalApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='futsal',
            name='description',
            field=ckeditor.fields.RichTextField(),
        ),
    ]
