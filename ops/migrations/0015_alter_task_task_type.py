# Generated by Django 4.0.4 on 2022-05-09 02:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ops', '0014_task_service_group'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='task_type',
            field=models.CharField(choices=[('---', '---'), ('Service Group', 'Service Group'), ('Objective', 'Objective'), ('Prepayment', 'Prepayment'), ('Wait List', 'Wait List'), ('Survey', 'Survey'), ('ALAN', 'ALAN'), ('Cancellation Request', 'Cancellation Request'), ('Cancellation Action', 'Cancellation Action')], default='---', max_length=50),
        ),
    ]
