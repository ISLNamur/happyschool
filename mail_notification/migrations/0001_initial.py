# Generated by Django 2.0.9 on 2019-01-07 12:30

from django.db import migrations, models
import django.db.models.deletion
import mail_notification.models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("auth", "0009_alter_user_last_name_max_length"),
        ("mail_answer", "0001_initial"),
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="EmailAttachment",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                (
                    "attachment",
                    models.FileField(upload_to=mail_notification.models.unique_file_name),
                ),
            ],
        ),
        migrations.CreateModel(
            name="EmailNotification",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("email_to", models.CharField(max_length=500)),
                ("to_type", models.CharField(default="", max_length=50)),
                ("email_from", models.EmailField(max_length=254)),
                ("subject", models.CharField(max_length=200)),
                ("body", models.TextField()),
                ("errors", models.CharField(max_length=4000)),
                ("teaching", models.CharField(max_length=50)),
                ("datetime_created", models.DateTimeField(verbose_name="Date de création")),
                (
                    "answers",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="mail_answer.MailTemplateModel",
                    ),
                ),
                ("attachments", models.ManyToManyField(to="mail_notification.EmailAttachment")),
            ],
            options={
                "permissions": (("access_mail_notification", "Can access to mail notification"),),
            },
        ),
        migrations.CreateModel(
            name="EmailNotificationSettingsModel",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("use_email_school", models.BooleanField(default=False)),
                (
                    "add_cc_parents",
                    models.ManyToManyField(
                        help_text="When sending an email to parents send a copy to those emails.",
                        related_name="add_cc_parents",
                        to="core.EmailModel",
                    ),
                ),
                (
                    "add_cc_teachers",
                    models.ManyToManyField(
                        help_text="When sending an email to teachers send a copy to those emails.",
                        related_name="add_cc_teachers",
                        to="core.EmailModel",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="EmailSender",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("sender_email", models.EmailField(max_length=254)),
                ("sender_email_name", models.CharField(max_length=100)),
                ("teaching", models.CharField(max_length=30)),
                ("groups", models.ManyToManyField(to="auth.Group")),
            ],
        ),
        migrations.CreateModel(
            name="EmailTag",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("name", models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name="OtherEmailGroupModel",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("name", models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name="OtherEmailModel",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("email", models.EmailField(max_length=254)),
                ("last_name", models.CharField(max_length=200)),
                ("first_name", models.CharField(max_length=200)),
                (
                    "group",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="mail_notification.OtherEmailGroupModel",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="emailnotification",
            name="tags",
            field=models.ManyToManyField(to="mail_notification.EmailTag"),
        ),
    ]
