# Generated by Django 3.1.4 on 2021-01-05 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0012_comments_likescount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comments',
            name='id_social',
            field=models.BigIntegerField(default=0),
        ),
    ]
