# Generated by Django 2.0 on 2018-01-21 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AccessApplication',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('appName', models.CharField(max_length=200)),
                ('appSecret', models.CharField(max_length=200)),
                ('life', models.IntegerField()),
                ('created', models.TimeField()),
            ],
        ),
    ]
