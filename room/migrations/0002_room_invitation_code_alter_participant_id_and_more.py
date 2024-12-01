# Generated by Django 5.1.2 on 2024-11-25 18:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('room', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='invitation_code',
            field=models.CharField(blank=True, max_length=5, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='participant',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='room',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]