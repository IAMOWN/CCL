# Generated by Django 4.0.4 on 2022-05-10 17:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0014_discourseseries_alter_tag_date_created'),
    ]

    operations = [
        migrations.AddField(
            model_name='libraryrecord',
            name='discourse_series',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='discourse_series_title', to='library.discourseseries', verbose_name='Discourse series title'),
        ),
    ]
