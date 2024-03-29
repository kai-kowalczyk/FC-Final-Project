# Generated by Django 3.2.9 on 2021-11-24 11:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data_scraper', '0002_auto_20211122_2211'),
    ]

    operations = [
        migrations.CreateModel(
            name='Offer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('offer_id', models.CharField(max_length=100)),
                ('offer_full_link', models.CharField(max_length=200)),
                ('position_title', models.CharField(max_length=100)),
                ('exp_lvl', models.CharField(max_length=100)),
                ('company_name', models.CharField(max_length=100)),
                ('skills', models.CharField(max_length=200)),
                ('min_salary', models.IntegerField()),
                ('max_salary', models.IntegerField()),
            ],
        ),
        migrations.DeleteModel(
            name='Offers',
        ),
    ]
