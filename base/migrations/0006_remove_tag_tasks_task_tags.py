# Generated by Django 4.0.2 on 2022-02-17 21:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0005_attachment_delete_attachments_task_category_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tag',
            name='tasks',
        ),
        migrations.AddField(
            model_name='task',
            name='tags',
            field=models.ManyToManyField(related_name='tags', to='base.Tag'),
        ),
    ]