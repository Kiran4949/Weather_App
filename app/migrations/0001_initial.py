# Generated by Django 4.2.4 on 2023-09-04 06:48

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CityWeather',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('temperature', models.DecimalField(decimal_places=2, max_digits=5)),
                ('condition', models.CharField(max_length=100)),
                ('humidity', models.DecimalField(decimal_places=2, max_digits=5)),
                ('wind_speed', models.DecimalField(decimal_places=2, max_digits=5)),
            ],
        ),
    ]