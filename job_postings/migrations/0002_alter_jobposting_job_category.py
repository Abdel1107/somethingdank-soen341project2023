# Generated by Django 4.1.2 on 2023-03-26 02:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job_postings', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobposting',
            name='job_category',
            field=models.CharField(choices=[('Other', 'Other'), ('Business', 'Business'), ('Technology', 'Technology'), ('Healthcare', 'Healthcare'), ('Education', 'Education'), ('Arts and entertainment', 'Arts and entertainment')], max_length=255),
        ),
    ]
