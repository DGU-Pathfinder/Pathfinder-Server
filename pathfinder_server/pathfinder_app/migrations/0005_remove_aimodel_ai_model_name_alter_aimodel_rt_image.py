# Generated by Django 4.2.7 on 2023-11-29 17:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pathfinder_app', '0004_alter_aidefect_xmax_alter_aidefect_xmin_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='aimodel',
            name='ai_model_name',
        ),
        migrations.AlterField(
            model_name='aimodel',
            name='rt_image',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='ai_model_set', to='pathfinder_app.rtimage'),
        ),
    ]