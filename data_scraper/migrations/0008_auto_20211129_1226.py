# Generated by Django 3.2.9 on 2021-11-29 12:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('data_scraper', '0007_auto_20211129_1139'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='offer',
            name='skills',
        ),
        migrations.AlterField(
            model_name='offerskills',
            name='offer_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='offer_skills_id', to='data_scraper.offer'),
        ),
        migrations.AlterField(
            model_name='offerskills',
            name='skill',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='offer_skills_skill', to='data_scraper.skills'),
        ),
        migrations.AlterField(
            model_name='skills',
            name='skill',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
