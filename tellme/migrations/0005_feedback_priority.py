# Generated by Django 2.2 on 2020-02-13 23:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tellme', '0004_auto'),
    ]

    operations = [
        migrations.AddField(
            model_name='feedback',
            name='priority',
            field=models.CharField(blank=True, choices=[('U', 'Urgent'), ('H', 'High'), ('N', 'Normal'), ('L', 'Low'), ('F', 'Floor'), ('-', 'Unassigned')], default='-', max_length=1),
        ),
    ]