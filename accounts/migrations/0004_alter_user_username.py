# Generated by Django 5.0.1 on 2024-02-03 08:25

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0003_alter_user_username"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="username",
            field=models.CharField(default=1, max_length=10, unique=True),
            preserve_default=False,
        ),
    ]
