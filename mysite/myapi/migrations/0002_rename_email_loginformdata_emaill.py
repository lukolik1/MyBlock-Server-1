# Generated by Django 3.2 on 2023-08-22 12:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapi', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='loginformdata',
            old_name='email',
            new_name='emaill',
        ),
    ]