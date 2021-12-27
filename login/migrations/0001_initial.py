# Generated by Django 2.2 on 2021-12-19 04:23

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CityWeather',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cityname', models.CharField(max_length=20)),
                ('date', models.CharField(max_length=10)),
                ('high', models.CharField(max_length=20)),
                ('low', models.CharField(max_length=10)),
                ('fx', models.CharField(max_length=20)),
                ('fl', models.CharField(max_length=20)),
                ('type', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='WebUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=50)),
                ('password', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254, null=True)),
            ],
        ),
    ]