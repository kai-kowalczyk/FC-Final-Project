#created by me on 2021-11-25 15:20
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data_scraper', '0003_auto_20211124_1133'),
    ]

    operations = [
        migrations.AddField(
            model_name='offer',
            name='from_site',
            field=models.CharField(max_length=100)

        ),
        migrations.AddField(
            model_name='offer',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, editable=False),
        ),
        migrations.AddField(
            model_name='offer',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, editable=False),
        ),
    ]