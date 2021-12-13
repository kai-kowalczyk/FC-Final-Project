# Generated by Django 3.2.9 on 2021-11-29 11:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('data_scraper', '0006_offerchanges'),
    ]

    operations = [
        migrations.CreateModel(
            name='Skills',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('skill', models.CharField(max_length=50)),
            ],
        ),
        migrations.AlterField(
            model_name='offer',
            name='max_salary',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='offer',
            name='min_salary',
            field=models.IntegerField(default=0),
        ),
        migrations.CreateModel(
            name='OfferSkills',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('offer_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='offer_skill', to='data_scraper.offer')),
                ('skill', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='offer_skill', to='data_scraper.skills')),
            ],
        ),
        migrations.AddConstraint(
            model_name='offerskills',
            constraint=models.UniqueConstraint(fields=('offer_id', 'skill'), name='unique_offer_skill'),
        ),
    ]