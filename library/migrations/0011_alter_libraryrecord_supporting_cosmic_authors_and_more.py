# Generated by Django 4.0.4 on 2022-05-08 18:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0010_alter_libraryrecord_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='libraryrecord',
            name='supporting_cosmic_authors',
            field=models.ManyToManyField(blank=True, to='library.cosmicauthor'),
        ),
        migrations.AlterField(
            model_name='libraryrecord',
            name='tags',
            field=models.ManyToManyField(blank=True, to='library.tag'),
        ),
    ]
