# Generated by Django 3.0.5 on 2020-11-07 16:41

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PostBlog',
            fields=[
                ('title', models.CharField(max_length=150)),
                ('desc', models.TextField(default='')),
                ('name', models.CharField(default='', max_length=150)),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
            ],
        ),
    ]
