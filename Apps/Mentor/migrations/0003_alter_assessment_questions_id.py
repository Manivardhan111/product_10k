# Generated by Django 5.0 on 2023-12-29 07:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Mentor', '0002_assessment_questions'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assessment_questions',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
