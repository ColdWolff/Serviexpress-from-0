# Generated by Django 4.2.1 on 2023-11-16 00:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taller', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cita',
            name='hora_aten',
        ),
        migrations.AlterField(
            model_name='cita',
            name='fecha_aten',
            field=models.DateTimeField(),
        ),
    ]
