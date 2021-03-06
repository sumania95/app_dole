# Generated by Django 3.1.6 on 2021-04-06 22:36

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('surname', models.CharField(max_length=200)),
                ('firstname', models.CharField(max_length=200)),
                ('middlename', models.CharField(blank=True, max_length=200)),
                ('ext_name', models.CharField(blank=True, max_length=200)),
                ('date_of_birth', models.DateField(default=django.utils.timezone.now)),
                ('gender', models.CharField(choices=[('1', 'Male'), ('2', 'Female')], max_length=10)),
                ('civil_status', models.CharField(choices=[('1', 'Single'), ('2', 'Married'), ('3', 'Widowed'), ('4', 'Separated'), ('5', 'Annulled')], max_length=10)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['surname', 'firstname', 'middlename'],
            },
        ),
        migrations.CreateModel(
            name='Programs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=200)),
                ('sponsored_by', models.CharField(blank=True, max_length=200)),
                ('date_from', models.DateField(default=django.utils.timezone.now)),
                ('date_to', models.DateField(default=django.utils.timezone.now)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Programs_Detail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_dole.profile')),
                ('programs', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_dole.programs')),
            ],
        ),
    ]
