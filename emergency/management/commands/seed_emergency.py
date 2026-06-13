"""Seeds the national emergency hotlines.

Port of the app's kEmergencyContacts (the 10 hub hotlines) and
kQuickDialContacts (the 4 home-screen tiles) from app_constants.dart.
Idempotent — keyed on (name_key, number). Re-run safely.
"""

from django.core.management.base import BaseCommand
from django.db import transaction

from emergency.models import EmergencyHotline

# (name_key, number, icon_key, color)
HOTLINES = [
    ('em_police', '119', 'shield', '#A32D2D'),
    ('em_ambulance', '1990', 'medical', '#185FA5'),
    ('em_fire', '111', 'fire', '#854F0B'),
    ('em_disaster', '117', 'warning', '#3B6D11'),
    ('em_women_child', '1938', 'family', '#72243E'),
    ('em_mental', '1926', 'mental', '#534AB7'),
    ('em_ceb', '1987', 'bolt', '#0F6E56'),
    ('em_water', '1954', 'water', '#185FA5'),
    ('em_tourist', '1912', 'travel', '#3C3489'),
    ('em_consumer', '1977', 'gavel', '#5F5E5A'),
]

# (name_key, number, icon_key, color) — home quick-dial row.
QUICK_DIAL = [
    ('em_police', '119', 'shield', '#A32D2D'),
    ('em_ambulance_short', '110', 'medical', '#185FA5'),
    ('em_fire', '111', 'fire', '#854F0B'),
    ('em_disaster', '117', 'warning', '#3B6D11'),
]


class Command(BaseCommand):
    help = 'Seed the emergency_hotlines table with the national hotlines.'

    @transaction.atomic
    def handle(self, *args, **options):
        EmergencyHotline.objects.all().delete()  # Small fixed set — rebuild

        rows = []
        order = 0
        for name_key, number, icon, color in HOTLINES:
            rows.append(EmergencyHotline(
                name_key=name_key, number=number, icon_key=icon, color=color,
                is_quick_dial=False, sort_order=order))
            order += 1
        for name_key, number, icon, color in QUICK_DIAL:
            rows.append(EmergencyHotline(
                name_key=name_key, number=number, icon_key=icon, color=color,
                is_quick_dial=True, sort_order=order))
            order += 1

        EmergencyHotline.objects.bulk_create(rows)
        self.stdout.write(self.style.SUCCESS(
            f'Seeded {len(rows)} hotlines '
            f'({len(HOTLINES)} hub + {len(QUICK_DIAL)} quick-dial).'))
