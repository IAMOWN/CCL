# Generated by Django 4.0.4 on 2022-05-06 18:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0003_libraryrecord_benediction_libraryrecord_invocation_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='libraryrecord',
            name='part_number',
            field=models.IntegerField(default=1),
        ),
    ]