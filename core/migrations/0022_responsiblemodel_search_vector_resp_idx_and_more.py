# Generated by Django 4.2.16 on 2025-02-17 11:09

import django.contrib.postgres.indexes
import django.contrib.postgres.search
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0021_auto_20250217_1156"),
    ]

    operations = [
        migrations.AddIndex(
            model_name="responsiblemodel",
            index=django.contrib.postgres.indexes.GinIndex(
                django.contrib.postgres.search.SearchVector(
                    "last_name", "first_name", config="fr_unaccent"
                ),
                name="search_vector_resp_idx",
            ),
        ),
        migrations.AddIndex(
            model_name="studentmodel",
            index=django.contrib.postgres.indexes.GinIndex(
                django.contrib.postgres.search.SearchVector(
                    "last_name", "first_name", config="fr_unaccent"
                ),
                name="search_vector_stud_idx",
            ),
        ),
    ]
