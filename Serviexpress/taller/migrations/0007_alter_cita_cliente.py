# Generated by Django 4.1.5 on 2023-11-17 18:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('taller', '0006_remove_cita_num_fb_fabo_cita_alter_cita_fecha_aten'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cita',
            name='cliente',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='taller.cliente'),
        ),
    ]