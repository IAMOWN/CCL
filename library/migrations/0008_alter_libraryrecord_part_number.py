# Generated by Django 4.0.4 on 2022-05-07 21:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0007_alter_libraryrecord_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='libraryrecord',
            name='part_number',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
