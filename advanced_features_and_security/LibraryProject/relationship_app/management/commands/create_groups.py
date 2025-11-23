from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from relationship_app.models import Book

class Command(BaseCommand):
    help = 'Create user groups and assign permissions'

    def handle(self, *args, **options):
        # Get the content type for the Book model
        book_content_type = ContentType.objects.get_for_model(Book)

        # Get permissions
        can_view = Permission.objects.get(content_type=book_content_type, codename='can_view')
        can_create = Permission.objects.get(content_type=book_content_type, codename='can_create')
        can_edit = Permission.objects.get(content_type=book_content_type, codename='can_edit')
        can_delete = Permission.objects.get(content_type=book_content_type, codename='can_delete')

        # Create groups
        viewers_group, created = Group.objects.get_or_create(name='Viewers')
        if created:
            viewers_group.permissions.add(can_view)
            self.stdout.write(self.style.SUCCESS('Created Viewers group with can_view permission'))

        editors_group, created = Group.objects.get_or_create(name='Editors')
        if created:
            editors_group.permissions.add(can_create, can_edit)
            self.stdout.write(self.style.SUCCESS('Created Editors group with can_create and can_edit permissions'))

        admins_group, created = Group.objects.get_or_create(name='Admins')
        if created:
            admins_group.permissions.add(can_view, can_create, can_edit, can_delete)
            self.stdout.write(self.style.SUCCESS('Created Admins group with all permissions'))

        self.stdout.write(self.style.SUCCESS('Groups and permissions setup completed'))