# Generated by Django 4.1 on 2024-08-02 04:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("files", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="file",
            name="url",
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="file",
            name="file",
            field=models.FileField(blank=True, null=True, upload_to="uploads/"),
        ),
    ]
