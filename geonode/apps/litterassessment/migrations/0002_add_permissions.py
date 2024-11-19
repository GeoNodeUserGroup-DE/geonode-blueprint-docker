import logging
from django.db import migrations
from django.contrib.auth.management import create_permissions
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
    
    # Migrations run in transactions. Permissions have to be created on 1st run
    app_config = apps.get_app_config("litterassessment")
    app_config.models_module = True
    create_permissions(app_config, verbosity=0)
    app_config.models_module = None
    for permission in PermissionsModel._meta.permissions:
        if create:
            perm = Permission.objects.get(codename=permission[0])
            group_profile.group.permissions.add(perm)
        group_profile.save()


class Migration(migrations.Migration):
    dependencies = [
        ("auth", "__latest__"),
        ("groups", "__latest__"),
        # ("contenttypes", "__latest__"),
        ("litterassessment", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(add_permissions),
    ]