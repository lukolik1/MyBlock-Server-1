# Generated by Django 3.2 on 2023-08-22 13:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapi', '0002_rename_email_loginformdata_emaill'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='customuser',
            managers=[
            ],
        ),
        migrations.RenameField(
            model_name='loginformdata',
            old_name='emaill',
            new_name='email',
        ),
        migrations.AlterField(
            model_name='block',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
