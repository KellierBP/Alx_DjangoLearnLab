from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission

class Command(BaseCommand):
    help = 'Create groups and assign permissions'

    def handle(self, *args, **options):
        # Get permissions
        can_view = Permission.objects.get(codename='can_view')
        can_create = Permission.objects.get(codename='can_create')
        can_edit = Permission.objects.get(codename='can_edit')
        can_delete = Permission.objects.get(codename='can_delete')

        # Create groups
        viewers, created = Group.objects.get_or_create(name='Viewers')
        editors, created = Group.objects.get_or_create(name='Editors')
        admins, created = Group.objects.get_or_create(name='Admins')

        # Assign permissions
        viewers.permissions.add(can_view)
        editors.permissions.add(can_view, can_create, can_edit)
        admins.permissions.add(can_view, can_create, can_edit, can_delete)

        self.stdout.write(self.style.SUCCESS('Groups and permissions created successfully.'))