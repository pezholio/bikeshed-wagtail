# Generated by Django 3.0.8 on 2020-07-08 13:18

from django.db import migrations
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('authors', '0001_initial'),
        ('blog_posts', '0002_auto_20200707_1437'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='authors',
            field=modelcluster.fields.ParentalManyToManyField(related_name='pages_blogpost', to='authors.Author'),
        ),
    ]
