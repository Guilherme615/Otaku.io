# Generated by Django 5.0 on 2024-11-29 01:29

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_alter_obra_capa_alter_obra_titulo_delete_userprofile'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='SolicitacaoObra',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=200)),
                ('data_solicitacao', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('Pendente', 'Pendente'), ('Aprovada', 'Aprovada'), ('Recusada', 'Recusada')], default='Pendente', max_length=20)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='solicitacoes', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]