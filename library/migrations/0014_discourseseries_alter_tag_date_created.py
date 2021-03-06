# Generated by Django 4.0.4 on 2022-05-10 17:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0013_alter_libraryrecord_principal_cosmic_author_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='DiscourseSeries',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('discourse_series', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['discourse_series'],
            },
        ),
        migrations.AlterField(
            model_name='tag',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
