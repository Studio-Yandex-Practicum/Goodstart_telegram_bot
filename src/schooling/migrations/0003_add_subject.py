# Generated by Django 5.0.4 on 2024-05-08 10:46

from django.db import migrations


def create_subject_mathematics(apps, schema_editor):
    """Create name of subject 'Mathematics'."""
    Subject = apps.get_model("schooling", "Subject")
    Subject.objects.create(
        name="Математика",
    )


def remove_subject_mathematics(apps, schema_editor):
    """Remove subject 'Mathematics' instance."""
    Subject = apps.get_model("schooling", "Subject")
    remove_subject = Subject.objects.get(name="Математика")
    remove_subject.delete()


def create_subject_algebra(apps, schema_editor):
    """Create name of subject 'Algebra'."""
    Subject = apps.get_model("schooling", "Subject")
    Subject.objects.create(
        name="Алгебра",
    )


def remove_subject_algebra(apps, schema_editor):
    """Remove subject 'Algebra' instance."""
    Subject = apps.get_model("schooling", "Subject")
    remove_subject = Subject.objects.get(name="Алгебра")
    remove_subject.delete()


def create_subject_geometry(apps, schema_editor):
    """Create name of subject 'Geometry'."""
    Subject = apps.get_model("schooling", "Subject")
    Subject.objects.create(
        name="Геометрия",
    )


def remove_subject_geometry(apps, schema_editor):
    """Remove subject 'Geometry' instance."""
    Subject = apps.get_model("schooling", "Subject")
    remove_subject = Subject.objects.get(name="Геометрия")
    remove_subject.delete()


def create_subject_russian(apps, schema_editor):
    """Create name of subject 'Russian'."""
    Subject = apps.get_model("schooling", "Subject")
    Subject.objects.create(
        name="Русский язык",
    )


def remove_subject_russian(apps, schema_editor):
    """Remove subject 'Russian' instance."""
    Subject = apps.get_model("schooling", "Subject")
    remove_subject = Subject.objects.get(name="Русский язык")
    remove_subject.delete()


def create_subject_english(apps, schema_editor):
    """Create name of subject 'English'."""
    Subject = apps.get_model("schooling", "Subject")
    Subject.objects.create(
        name="Английский язык",
    )


def remove_subject_english(apps, schema_editor):
    """Remove subject 'English' instance."""
    Subject = apps.get_model("schooling", "Subject")
    remove_subject = Subject.objects.get(name="Английский язык")
    remove_subject.delete()


def create_subject_spanish(apps, schema_editor):
    """Create name of subject 'Spanish'."""
    Subject = apps.get_model("schooling", "Subject")
    Subject.objects.create(
        name="Испанский язык",
    )


def remove_subject_spanish(apps, schema_editor):
    """Remove subject 'Spanish' instance."""
    Subject = apps.get_model("schooling", "Subject")
    remove_subject = Subject.objects.get(name="Испанский язык")
    remove_subject.delete()


def create_subject_literature(apps, schema_editor):
    """Create name of subject 'Literature'."""
    Subject = apps.get_model("schooling", "Subject")
    Subject.objects.create(
        name="Литература",
    )


def remove_subject_literature(apps, schema_editor):
    """Remove subject 'Literature' instance."""
    Subject = apps.get_model("schooling", "Subject")
    remove_subject = Subject.objects.get(name="Литература")
    remove_subject.delete()


def create_subject_geography(apps, schema_editor):
    """Create name of subject 'Geography'."""
    Subject = apps.get_model("schooling", "Subject")
    Subject.objects.create(
        name="География",
    )


def remove_subject_geography(apps, schema_editor):
    """Remove subject 'Geography' instance."""
    Subject = apps.get_model("schooling", "Subject")
    remove_subject = Subject.objects.get(name="География")
    remove_subject.delete()


def create_subject_history(apps, schema_editor):
    """Create name of subject 'History'."""
    Subject = apps.get_model("schooling", "Subject")
    Subject.objects.create(
        name="История",
    )


def remove_subject_history(apps, schema_editor):
    """Remove subject 'History' instance."""
    Subject = apps.get_model("schooling", "Subject")
    remove_subject = Subject.objects.get(name="История")
    remove_subject.delete()


def create_subject_chemistry(apps, schema_editor):
    """Create name of subject 'Chemistry'."""
    Subject = apps.get_model("schooling", "Subject")
    Subject.objects.create(
        name="Химия",
    )


def remove_subject_chemistry(apps, schema_editor):
    """Remove subject 'Chemistry' instance."""
    Subject = apps.get_model("schooling", "Subject")
    remove_subject = Subject.objects.get(name="Химия")
    remove_subject.delete()


def create_subject_science(apps, schema_editor):
    """Create name of subject 'Science'."""
    Subject = apps.get_model("schooling", "Subject")
    Subject.objects.create(
        name="Физика",
    )


def remove_subject_science(apps, schema_editor):
    """Remove subject 'Science' instance."""
    Subject = apps.get_model("schooling", "Subject")
    remove_subject = Subject.objects.get(name="Физика")
    remove_subject.delete()


def create_subject_information_technology(apps, schema_editor):
    """Create name of subject 'Information Technology'."""
    Subject = apps.get_model("schooling", "Subject")
    Subject.objects.create(
        name="Информатика",
    )


def remove_subject_information_technology(apps, schema_editor):
    """Remove subject 'Information Technology' instance."""
    Subject = apps.get_model("schooling", "Subject")
    remove_subject = Subject.objects.get(name="Информатика")
    remove_subject.delete()


class Migration(migrations.Migration):
    dependencies = [
        ("schooling", '0002_add_study_classes'),
    ]

    operations = [
        migrations.RunPython(
            create_subject_mathematics, reverse_code=remove_subject_mathematics
        ),
        migrations.RunPython(
            create_subject_algebra, reverse_code=remove_subject_algebra
        ),
        migrations.RunPython(
            create_subject_geometry, reverse_code=remove_subject_geometry
        ),
        migrations.RunPython(
            create_subject_russian, reverse_code=remove_subject_russian
        ),
        migrations.RunPython(
            create_subject_english, reverse_code=remove_subject_english
        ),
        migrations.RunPython(
            create_subject_spanish, reverse_code=remove_subject_spanish
        ),
        migrations.RunPython(
            create_subject_literature, reverse_code=remove_subject_literature
        ),
        migrations.RunPython(
            create_subject_history, reverse_code=remove_subject_history
        ),
        migrations.RunPython(
            create_subject_geography, reverse_code=remove_subject_geography
        ),
        migrations.RunPython(
            create_subject_chemistry, reverse_code=remove_subject_chemistry
        ),
        migrations.RunPython(
            create_subject_science, reverse_code=remove_subject_science
        ),
        migrations.RunPython(
            create_subject_information_technology,
            reverse_code=remove_subject_information_technology
        ),
    ]
