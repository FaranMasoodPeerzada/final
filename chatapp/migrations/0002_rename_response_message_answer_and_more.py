# Generated by Django 4.2.4 on 2023-09-22 17:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chatapp', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='message',
            old_name='response',
            new_name='answer',
        ),
        migrations.RenameField(
            model_name='message',
            old_name='text',
            new_name='question',
        ),
    ]
