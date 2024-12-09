# Generated by Django 5.1.2 on 2024-12-08 11:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0004_rename_name_question_quiz_subject_delete_quiz'),
        ('room', '0005_delete_question'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='questions',
            field=models.ManyToManyField(blank=True, related_name='rooms', to='quiz.question'),
        ),
    ]