# Generated by Django 3.0.7 on 2020-06-06 10:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teacher',
            name='name',
            field=models.CharField(max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='teacherid',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]