# Generated by Django 2.2.3 on 2022-07-13 15:23

from django.db import migrations
import mdeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20220413_2151'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='body',
            field=mdeditor.fields.MDTextField(verbose_name='正文'),
        ),
    ]
