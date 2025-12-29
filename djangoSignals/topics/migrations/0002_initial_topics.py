from django.db import migrations


def create_topics(apps, schema_editor):
    Topic = apps.get_model("topics", "Topic")
    for name in ["Python", "Django", "DevOps"]:
        Topic.objects.get_or_create(name=name)


class Migration(migrations.Migration):
    dependencies = [
        ("topics", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(create_topics),
    ]
