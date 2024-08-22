# Generated by Django 4.2 on 2024-04-15 12:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


def migrate_from_student_absence(apps, schema_editor):
    if "student_absence" not in settings.INSTALLED_APPS:
        return

    OldStudentAbsence = apps.get_model("student_absence", "StudentAbsenceModel")
    OldPeriod = apps.get_model("student_absence", "PeriodModel")
    OldSettings = apps.get_model("student_absence", "StudentAbsenceSettingsModel")

    StudentAbsenceTeacherSettingsModel = apps.get_model(
        "student_absence_teacher", "StudentAbsenceTeacherSettingsModel"
    )
    PeriodEducModel = apps.get_model("student_absence_teacher", "PeriodEducModel")
    StudentAbsenceEducModel = apps.get_model("student_absence_teacher", "StudentAbsenceEducModel")

    # First, migrate settings.
    student_abs_teacher_settings = StudentAbsenceTeacherSettingsModel.objects.all().first()
    old_settings = OldSettings.objects.all().first()
    student_abs_teacher_settings.sync_with_proeco = old_settings.sync_with_proeco
    student_abs_teacher_settings.save()

    # Second, migrate periods.
    for old_period in OldPeriod.objects.all().order_by("id"):
        period = PeriodEducModel(
            id=old_period.id,
            start=old_period.start,
            end=old_period.end,
            name=old_period.name,
            day_of_week=old_period.day_of_week,
        )
        period.save()

    # Finally, migrate absences.
    for o_abs in OldStudentAbsence.objects.all():
        n_abs = StudentAbsenceEducModel(
            student=o_abs.student,
            date_absence=o_abs.date_absence,
            period=PeriodEducModel.objects.get(id=o_abs.period.id),
            status="A" if o_abs.is_absent else "P",
            is_processed=o_abs.is_processed,
            user=o_abs.user,
            datetime_creation=o_abs.datetime_creation,
            datetime_update=o_abs.datetime_update,
        )
        n_abs.save()


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0019_auto_20220524_1007"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        (
            "student_absence_teacher",
            "0014_studentabsenceteachermodel_student_abs_date_ab_74186b_idx",
        ),
    ]

    operations = [
        migrations.CreateModel(
            name="PeriodEducModel",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("start", models.TimeField()),
                ("end", models.TimeField()),
                ("name", models.CharField(max_length=200)),
                ("day_of_week", models.CharField(default="1-5", max_length=10)),
            ],
        ),
        migrations.AddField(
            model_name="studentabsenceteachersettingsmodel",
            name="sync_with_proeco",
            field=models.BooleanField(
                default=False, verbose_name="Synchronise les absences avec ProEco"
            ),
        ),
        migrations.CreateModel(
            name="StudentAbsenceEducModel",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("date_absence", models.DateField(verbose_name="Absence date")),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("P", "Présence"),
                            ("R", "Retard"),
                            ("A", "Absence"),
                            ("Q", "Départ anticipé"),
                        ],
                        max_length=2,
                        verbose_name="Student status",
                    ),
                ),
                ("is_processed", models.BooleanField(default=False)),
                ("datetime_creation", models.DateTimeField(auto_now_add=True)),
                ("datetime_update", models.DateTimeField(auto_now=True)),
                (
                    "period",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="student_absence_teacher.periodeducmodel",
                    ),
                ),
                (
                    "student",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="core.studentmodel"
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.AddIndex(
            model_name="studentabsenceeducmodel",
            index=models.Index(
                fields=["-date_absence", "student", "status"], name="student_abs_date_ab_66579c_idx"
            ),
        ),
        migrations.RunPython(migrate_from_student_absence),
    ]