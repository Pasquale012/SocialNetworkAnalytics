# Generated by Django 3.1.4 on 2021-01-02 18:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0003_auto_20201230_1928'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='nDatePostSaved',
            field=models.CharField(default='', max_length=200),
        ),
    ]