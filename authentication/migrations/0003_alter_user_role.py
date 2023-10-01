# Generated by Django 4.2.5 on 2023-09-26 07:25

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("authentication", "0002_user_role"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="role",
            field=models.CharField(
                choices=[
                    ("Admin", "Admin"),
                    ("Teacher", "Teacher"),
                    ("Student", "Student"),
                ],
                default="Student",
                max_length=10,
            ),
        ),
    ]