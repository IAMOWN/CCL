# Generated by Django 4.0.4 on 2022-05-07 20:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ops', '0002_alter_servicegroup_date_created'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='servicegroup',
            options={'ordering': ['service_group_type', 'service_group'], 'verbose_name': 'Service Group', 'verbose_name_plural': 'Service Groups'},
        ),
    ]
