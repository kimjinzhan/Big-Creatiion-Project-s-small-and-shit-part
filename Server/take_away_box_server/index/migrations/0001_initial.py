# Generated by Django 4.1.5 on 2023-01-16 02:50

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='staff_info',
            fields=[
                ('staff_id', models.CharField(max_length=5, primary_key=True, serialize=False)),
                ('stuff_name', models.CharField(max_length=5)),
                ('staff_pwd', models.CharField(max_length=10)),
            ],
        ),
    ]