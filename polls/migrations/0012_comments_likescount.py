# Generated by Django 3.1.4 on 2021-01-05 15:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0011_comments_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='comments',
            name='likesCount',
            field=models.IntegerField(default=0),
        ),
    ]
