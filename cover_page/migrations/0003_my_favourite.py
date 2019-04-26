# Generated by Django 2.1.7 on 2019-03-21 08:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cover_page', '0002_product'),
    ]

    operations = [
        migrations.CreateModel(
            name='My_Favourite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_link', models.TextField()),
                ('product_image_link', models.TextField()),
                ('product_name', models.TextField()),
                ('product_price', models.TextField()),
                ('product_tag', models.TextField()),
                ('user', models.ForeignKey(default=None, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]