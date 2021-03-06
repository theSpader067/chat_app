# Generated by Django 2.2 on 2020-04-23 00:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social_app', '0014_profile_group_rooms'),
    ]

    operations = [
        migrations.CreateModel(
            name='groupProfile',
            fields=[
                ('group_profile_id', models.AutoField(primary_key=True, serialize=False)),
                ('group_room', models.CharField(blank=True, max_length=200, null=True)),
                ('message', models.CharField(blank=True, max_length=200, null=True)),
                ('time_stamp', models.DateTimeField(auto_now_add=True)),
                ('author', models.CharField(blank=True, max_length=200, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='profile',
            name='group_rooms',
        ),
    ]
