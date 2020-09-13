# Generated by Django 3.1 on 2020-09-13 02:26

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='tweet',
            fields=[
                ('id', models.BigIntegerField(editable=False, primary_key=True, serialize=False, unique=True)),
                ('text', models.CharField(max_length=280)),
                ('author_id', models.BigIntegerField(editable=False)),
            ],
        ),
    ]