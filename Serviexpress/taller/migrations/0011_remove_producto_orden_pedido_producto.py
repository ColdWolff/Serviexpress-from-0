# Generated by Django 4.2.1 on 2023-11-18 21:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('taller', '0010_alter_cliente_rut_cli_alter_empleado_rut_emp'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='producto',
            name='orden',
        ),
        migrations.AddField(
            model_name='pedido',
            name='producto',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='taller.producto'),
            preserve_default=False,
        ),
    ]
