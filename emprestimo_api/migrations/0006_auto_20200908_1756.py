# Generated by Django 3.1 on 2020-09-08 17:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emprestimo_api', '0005_auto_20200908_1755'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emprestimo',
            name='endereco_ip',
            field=models.CharField(max_length=20),
        ),
    ]