# Generated by Django 3.1.6 on 2022-05-15 22:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_dole', '0008_auto_20210505_1608'),
    ]

    operations = [
        migrations.AddField(
            model_name='programs',
            name='category',
            field=models.CharField(choices=[('1', 'TUPAD'), ('2', 'SPES')], default=1, max_length=10),
        ),
    ]
