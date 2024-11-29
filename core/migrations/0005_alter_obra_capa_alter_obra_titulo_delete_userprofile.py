# Generated by Django 5.0 on 2024-11-28 23:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_alter_obra_capa_alter_obra_titulo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='obra',
            name='capa',
            field=models.ImageField(blank=True, null=True, upload_to='capas/'),
        ),
        migrations.AlterField(
            model_name='obra',
            name='titulo',
            field=models.CharField(max_length=200, unique=True),
        ),
        migrations.DeleteModel(
            name='UserProfile',
        ),
    ]
