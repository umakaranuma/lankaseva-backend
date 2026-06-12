"""Grant or revoke the admin flag for a user by phone number.

Usage:
    python manage.py set_admin 0771234567
    python manage.py set_admin 0771234567 --revoke
"""

from django.core.management.base import BaseCommand, CommandError

from accounts.models import AppUser
from accounts.views import hash_phone, normalize_phone


class Command(BaseCommand):
    help = 'Grant (or revoke with --revoke) service-management rights for a phone number.'

    def add_arguments(self, parser):
        parser.add_argument('phone', help="Sri Lankan mobile, e.g. 0771234567 or +94771234567")
        parser.add_argument('--revoke', action='store_true')

    def handle(self, *args, **options):
        phone = normalize_phone(options['phone'])
        if not phone:
            raise CommandError('Invalid Sri Lankan mobile number.')

        phone_hash = hash_phone(phone)
        user, created = AppUser.objects.get_or_create(
            phone_hash=phone_hash, defaults={'display_name': 'Admin'})
        user.is_admin = not options['revoke']
        user.save(update_fields=['is_admin'])

        state = 'revoked from' if options['revoke'] else 'granted to'
        suffix = ' (new user created)' if created else ''
        self.stdout.write(self.style.SUCCESS(f'Admin {state} {phone}{suffix}.'))
