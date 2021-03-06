# Generated by Django 4.0.4 on 2022-05-08 23:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ops', '0008_objective_objective_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='PEeP',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('process_function', models.CharField(default='', help_text='Enter the Team member job title or functional activity. Note: Whurthy will only be able to act on this record if the applicable feature has been built into the application. However, please feel free to enter PEeP records for your own reference, and to identify future automation opportunities.', max_length=50, unique=True)),
                ('process_code', models.CharField(default='', help_text="Enter the process code for this process activity. The recommended format should be abbreviations of the organization's name and the process name. For example, the Whurthy employee on-boarding process could have the process code of LFON. There is a limit of 20 characters for the Process Code.", max_length=20)),
                ('display_name', models.CharField(default='', max_length=30)),
                ('whurthy_team', models.CharField(choices=[('Finance', 'Finance'), ('Operations', 'Operations'), ('People', 'People'), ('Product Management', 'Product Management'), ('Sales', 'Sales'), ('Support', 'Support')], max_length=50)),
                ('detailed_description', models.TextField(blank=True, null=True)),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('responsible', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('supervisor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='PEeP_entry_supervisor', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'PEeP',
                'verbose_name_plural': 'PEeP',
                'ordering': ['whurthy_team', 'process_code', 'date_created'],
            },
        ),
        migrations.CreateModel(
            name='LEE',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('process_role', models.CharField(default='', help_text='Enter the specific task name. This should not be changed once it has been coded into the Whurthy application, as it will be used in task assignment.', max_length=100, unique=True)),
                ('whurthy_application', models.CharField(choices=[('Events', 'Events'), ('Ops', 'Ops'), ('Users', 'Users'), ('Whurthy', 'Whurthy'), ('Other', 'Other')], default='PIPS', help_text='Please select the application that this entry applies to.', max_length=100)),
                ('relevant_file', models.CharField(blank=True, default='events/ views.py', help_text='If applicable, enter the specific file path and file name.', max_length=100, null=True)),
                ('process_description', models.TextField(default='', help_text='Enter the process description for the task. Whatever is entered into this field will be the process description provided for the task assignment/notification to the assignee.')),
                ('process_code', models.CharField(default='WEVENT', help_text="Enter the process code for this process activity. The recommended format should be abbreviations of the organization's name and the process name. For example, the Whurthy employee on-boarding process could have the process code of WON. There is a limit of 10 characters for the Process Code.", max_length=10)),
                ('process_outcome', models.TextField(blank=True, help_text='If applicable, enter a description of the outcome of the process.', null=True)),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('entry_owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='lEE_entry_owner', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'LEE',
                'verbose_name_plural': 'LEE',
                'ordering': ['process_role'],
            },
        ),
    ]
