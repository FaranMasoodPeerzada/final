# Generated by Django 4.2.4 on 2023-09-24 19:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatapp', '0002_rename_response_message_answer_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='conversation',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]
