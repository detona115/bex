# Generated by Django 4.2.2 on 2023-07-01 18:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='marcas',
            options={'ordering': ['nome']},
        ),
        migrations.AlterField(
            model_name='marcas',
            name='codigo',
            field=models.CharField(max_length=250, unique=True),
        ),
    ]
