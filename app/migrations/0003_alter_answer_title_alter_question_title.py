# Generated by Django 5.1.3 on 2024-12-23 12:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_answer_created_at_question_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='title',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='question',
            name='title',
            field=models.CharField(max_length=50),
        ),
    ]
