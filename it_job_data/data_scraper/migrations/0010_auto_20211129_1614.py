# Generated by Django 3.2.9 on 2021-11-29 16:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('data_scraper', '0009_rename_offer_id_offerskills_offer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offerskills',
            name='offer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='offer_skills', to='data_scraper.offer'),
        ),
        migrations.AlterField(
            model_name='offerskills',
            name='skill',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='offer_skills', to='data_scraper.skills'),
        ),
    ]
