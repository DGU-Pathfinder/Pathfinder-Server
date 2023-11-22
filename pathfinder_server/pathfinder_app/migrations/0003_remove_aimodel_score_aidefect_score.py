# Generated by Django 4.2.7 on 2023-11-23 01:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pathfinder_app', '0002_alter_expert_rt_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='aimodel',
            name='score',
        ),
        migrations.AddField(
            model_name='aidefect',
            name='score',
            field=models.FloatField(default=12),
            preserve_default=False,
        ),
    ]
