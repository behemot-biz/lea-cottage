# Generated by Django 4.2.16 on 2024-09-20 10:01

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('content', models.TextField()),
            ],
        ),
    ]
