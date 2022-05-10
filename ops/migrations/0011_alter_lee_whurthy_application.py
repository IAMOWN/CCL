# Generated by Django 4.0.4 on 2022-05-09 00:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ops', '0010_peep_service_group_alter_lee_whurthy_application'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lee',
            name='whurthy_application',
            field=models.CharField(choices=[('CCL', 'CCL'), ('Events', 'Events'), ('Ops', 'Ops'), ('Users', 'Users'), ('CCL', 'CCL'), ('Other', 'Other')], default='PIPS', help_text='Please select the application that this entry applies to.', max_length=100, verbose_name='CCL Application'),
        ),
    ]
