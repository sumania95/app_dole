# Generated by Django 3.1.6 on 2021-04-06 22:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_dole', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Barangay',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AddField(
            model_name='profile',
            name='barangay',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='app_dole.barangay'),
            preserve_default=False,
        ),
    ]