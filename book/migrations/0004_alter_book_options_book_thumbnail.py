# Generated by Django 4.1.4 on 2023-01-09 06:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("book", "0003_review"),
    ]

    operations = [
        migrations.AlterModelOptions(name="book", options={"verbose_name": "本のデータ"},),
        migrations.AddField(
            model_name="book",
            name="thumbnail",
            field=models.ImageField(blank=True, null=True, upload_to=""),
        ),
    ]