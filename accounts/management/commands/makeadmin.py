import hashlib
from django.core.management.base import BaseCommand
from accounts.models import AppUser

class Command(BaseCommand):
    help = 'Creates an admin user or promotes an existing user to admin using their email and password'

    def add_arguments(self, parser):
        parser.add_argument('email', type=str, help='The email address of the admin')
        parser.add_argument('password', type=str, help='The password for the admin')
        parser.add_argument('--name', type=str, default='Admin User', help='The display name for the admin')

    def handle(self, *args, **options):
        email = options['email']
        password = options['password']
        name = options['name']

        # Check if user exists
        user = AppUser.objects.filter(email=email).first()
        created = False
        
        if not user:
            # Create a dummy phone_hash since it's required and unique
            phone_hash = f"admin_{hashlib.sha256(email.encode('utf-8')).hexdigest()}"
            user = AppUser(
                email=email,
                phone_hash=phone_hash,
                display_name=name
            )
            created = True

        user.is_admin = True
        user.set_password(password)
        user.save()
        
        if created:
            self.stdout.write(self.style.SUCCESS(f'Successfully created new admin user with email "{email}"'))
        else:
            self.stdout.write(self.style.SUCCESS(f'Successfully updated existing user with email "{email}" to admin'))
