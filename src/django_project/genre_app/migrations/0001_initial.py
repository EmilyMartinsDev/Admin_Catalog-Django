# Generated by Django 5.0.7 on 2024-07-30 12:35

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('category_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('is_active', models.BooleanField(default=True)),
                ('categories', models.ManyToManyField(related_name='genres', to='category_app.category')),
            ],
            options={
                'db_table': 'genres',
            },
        ),
    ]
