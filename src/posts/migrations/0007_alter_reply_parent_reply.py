# Generated by Django 5.0.7 on 2024-07-10 02:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("posts", "0006_remove_autoreplyconfig_comment_autoreplyconfig_post"),
    ]

    operations = [
        migrations.AlterField(
            model_name="reply",
            name="parent_reply",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="child_replies",
                to="posts.reply",
            ),
        ),
    ]
