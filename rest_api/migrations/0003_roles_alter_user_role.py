# Generated by Django 5.1.2 on 2024-10-19 18:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rest_api', '0002_invitation_participant_question_quiz_room_user_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Roles',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('is_admin', models.BooleanField(default=False)),
            ],
        ),
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='rest_api.roles'),
        ),
    ]
