# Generated by Django 4.0.4 on 2022-05-06 18:05

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CosmicAuthor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('date_created', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('date_created', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='LibraryRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, default='', max_length=200, null=True)),
                ('body', models.TextField(blank=True, default='', null=True)),
                ('series_title', models.CharField(blank=True, default='', max_length=200, null=True)),
                ('date_communicated', models.DateField(default=datetime.date.today)),
                ('year_communicated', models.IntegerField(default=2022)),
                ('pdf_url', models.CharField(blank=True, default='', max_length=200, null=True)),
                ('doc_url', models.CharField(blank=True, default='', max_length=200, null=True)),
                ('mp3_url', models.CharField(blank=True, default='', max_length=200, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('principal_cosmic_author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='principal_cosmic_author', to='library.cosmicauthor')),
                ('supporting_cosmic_authors', models.ManyToManyField(to='library.cosmicauthor')),
                ('tags', models.ManyToManyField(to='library.tag')),
            ],
        ),
    ]