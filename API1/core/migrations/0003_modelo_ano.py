# Generated by Django 4.2.2 on 2023-07-03 02:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_marcas_options_alter_marcas_codigo'),
    ]

    operations = [
        migrations.CreateModel(
            name='Modelo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.CharField(max_length=250)),
                ('nome', models.CharField(max_length=250)),
                ('marca', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='modelo', to='core.marcas')),
            ],
            options={
                'ordering': ['nome'],
            },
        ),
        migrations.CreateModel(
            name='Ano',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.CharField(max_length=250)),
                ('nome', models.CharField(max_length=250)),
                ('marca', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ano', to='core.marcas')),
            ],
            options={
                'ordering': ['nome'],
            },
        ),
    ]
