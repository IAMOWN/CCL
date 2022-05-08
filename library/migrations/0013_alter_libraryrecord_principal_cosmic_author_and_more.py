# Generated by Django 4.0.4 on 2022-05-08 18:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0012_alter_libraryrecord_principal_cosmic_author_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='libraryrecord',
            name='principal_cosmic_author',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='principal_cosmic_author', to='library.cosmicauthor', verbose_name='Principal author'),
        ),
        migrations.AlterField(
            model_name='libraryrecord',
            name='supporting_cosmic_authors',
            field=models.ManyToManyField(blank=True, to='library.cosmicauthor', verbose_name='Supporting authors'),
        ),
    ]
