# Generated by Django 4.2.5 on 2023-10-08 02:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0011_user_actie'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='actie',
            new_name='active',
        ),
    ]