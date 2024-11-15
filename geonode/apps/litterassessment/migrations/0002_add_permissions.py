import logging
from django.db import migrations
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission

from geonode.groups.models import GroupProfile

logger = logging.getLogger(__name__)

def add_permissions(apps, schema_editor):
    PermissionsModel = apps.get_model("litterassessment", "PermissionsModel")
    group_profile, create = GroupProfile.objects.get_or_create(
        slug="ai-inference",
        title="ai-inference",
        access="private"
    )
    for permission in PermissionsModel._meta.permissions:
        if create:
            ctype = ContentType.objects.get_for_model(group_profile)
            perm, _ = Permission.objects.get_or_create(
                codename=permission[0],
                name=permission[1],
                content_type=ctype,
            )
            group_profile.group.permissions.add(perm)
        group_profile.save()


class Migration(migrations.Migration):
    dependencies = [
        ("auth", "__latest__"),
        ("groups", "__latest__"),
        ("contenttypes", "__latest__"),
        ("litterassessment", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(add_permissions),
    ]