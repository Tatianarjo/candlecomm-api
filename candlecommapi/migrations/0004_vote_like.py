# Generated by Django 4.0.3 on 2022-03-12 23:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('candlecommapi', '0003_discussionboard'),
    ]

    operations = [
        migrations.AddField(
            model_name='vote',
            name='like',
            field=models.BooleanField(default=False),
        ),
    ]