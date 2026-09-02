"""Seeds the government places directory.

Port of the mobile app's offline ServiceDataSource (service_data_source.dart):
nine core services for each of the 25 districts plus the curated National
Hospital flagship entry. Idempotent — re-running updates existing rows.
"""

import random

from django.core.management.base import BaseCommand
from django.db import transaction

from services.models import (
    Category, OpeningHourSlot, OpeningHours, Service, ServicePhone,
)

# The nine core categories this command assigns to services. Kept in sync with
# the first block of seed_national.CATEGORIES so this command is self-sufficient
# (services.category is a FK to categories.code).
CORE_CATEGORIES = [
    # code, name_en, name_si, name_ta, icon, color
    ('hospital',    'Hospitals',         'රෝහල්',          'மருத்துவமனைகள்',    'local_hospital',    '0xFF1B4F72'),
    ('police',      'Police Stations',   'පොලිස් ස්ථාන',   'காவல் நிலையங்கள்',  'local_police',      '0xFF1A252F'),
    ('secretariat', 'Government Offices', 'රාජ්‍ය කාර්යාල', 'அரசு அலுவலகங்கள்',  'account_balance',   '0xFF1B2A3B'),
    ('ceb',         'Electricity',       'විදුලිය',        'மின்சாரம்',         'electric_bolt',     '0xFF7B3F00'),
    ('water',       'Water Supply',      'ජල සැපයුම',      'நீர் வழங்கல்',      'water_drop',        '0xFF154360'),
    ('post',        'Post Offices',      'තැපැල් කාර්යාල', 'தபால் அலுவலகங்கள்', 'local_post_office', '0xFF4A235A'),
    ('court',       'Courts',            'අධිකරණ',         'நீதிமன்றங்கள்',     'gavel',             '0xFF1C2833'),
    ('school',      'Schools',           'පාසල්',          'பள்ளிகள்',          'school',            '0xFF0B3D0B'),
    ('transport',   'Transport',         'ප්‍රවාහනය',      'போக்குவரத்து',      'directions_bus',    '0xFF1A1A2E'),
]

# (name, province, lat, lng) — district capitals, from app_constants.dart.
DISTRICTS = [
    ('Colombo', 'Western', 6.9271, 79.8612),
    ('Gampaha', 'Western', 7.0917, 79.9999),
    ('Kalutara', 'Western', 6.5854, 79.9607),
    ('Kandy', 'Central', 7.2906, 80.6337),
    ('Matale', 'Central', 7.4675, 80.6234),
    ('Nuwara Eliya', 'Central', 6.9497, 80.7891),
    ('Galle', 'Southern', 6.0535, 80.2210),
    ('Matara', 'Southern', 5.9549, 80.5550),
    ('Hambantota', 'Southern', 6.1429, 81.1212),
    ('Jaffna', 'Northern', 9.6615, 80.0255),
    ('Kilinochchi', 'Northern', 9.3803, 80.3770),
    ('Mannar', 'Northern', 8.9810, 79.9044),
    ('Mullaitivu', 'Northern', 9.2671, 80.8142),
    ('Vavuniya', 'Northern', 8.7514, 80.4971),
    ('Batticaloa', 'Eastern', 7.7170, 81.7000),
    ('Ampara', 'Eastern', 7.2975, 81.6820),
    ('Trincomalee', 'Eastern', 8.5874, 81.2152),
    ('Kurunegala', 'North Western', 7.4818, 80.3609),
    ('Puttalam', 'North Western', 8.0362, 79.8283),
    ('Anuradhapura', 'North Central', 8.3114, 80.4037),
    ('Polonnaruwa', 'North Central', 7.9403, 81.0188),
    ('Badulla', 'Uva', 6.9934, 81.0550),
    ('Monaragala', 'Uva', 6.8714, 81.3487),
    ('Ratnapura', 'Sabaragamuwa', 6.7056, 80.3847),
    ('Kegalle', 'Sabaragamuwa', 7.2513, 80.3464),
]

# (weekday 1=Mon..7=Sun, open, close)
OFFICE_HOURS = [(d, '08:30', '16:15') for d in range(1, 6)]
SLTB_HOURS = [(d, '05:00', '21:00') for d in range(1, 7)] + [(7, '06:00', '20:00')]


class Command(BaseCommand):
    help = 'Seed the services tables with the national government places directory.'

    def add_arguments(self, parser):
        parser.add_argument('--fresh', action='store_true',
                            help='Delete all existing services first.')

    @transaction.atomic
    def handle(self, *args, **options):
        for code, name_en, name_si, name_ta, icon, color in CORE_CATEGORIES:
            Category.objects.update_or_create(
                code=code,
                defaults=dict(name_en=name_en, name_si=name_si, name_ta=name_ta,
                              icon=icon, color=color),
            )
        self.stdout.write(f'Ensured {len(CORE_CATEGORIES)} core categories.')

        if options['fresh']:
            Service.objects.all().delete()
            self.stdout.write('Cleared existing services.')

        rng = random.Random(7)  # Fixed seed → stable phone numbers / pins
        created = updated = 0

        def phone_number():
            return f'0{11 + rng.randrange(80)}{2000000 + rng.randrange(7999999)}'

        def jitter(value):
            return value + (rng.random() - 0.5) * 0.05

        def save(service_id, *, name, department, category, district, lat, lng,
                 address, phones, hours, website=None, whatsapp=None,
                 is_emergency=False):
            nonlocal created, updated
            _, was_created = Service.objects.update_or_create(
                code=service_id,  # stable slug; integer id is auto-assigned
                defaults={
                    'name_en': name[0], 'name_si': name[1], 'name_ta': name[2],
                    'department_en': department[0], 'department_si': department[1],
                    'department_ta': department[2],
                    'category_id': category, 'district': district,
                    'address_en': address[0], 'address_si': address[1],
                    'address_ta': address[2],
                    'lat': lat, 'lng': lng,
                    'website': website, 'whatsapp': whatsapp,
                    'is_emergency': is_emergency,
                },
            )
            service = Service.objects.get(code=service_id)
            service.phones.all().delete()
            ServicePhone.objects.bulk_create([
                ServicePhone(service=service, label_en=p[0][0], label_si=p[0][1],
                             label_ta=p[0][2], number=p[1],
                             is_primary=(i == 0))
                for i, p in enumerate(phones)
            ])
            record, _ = OpeningHours.objects.update_or_create(
                service=service,
                defaults={'is_always_open': hours == 'always', 'notes': None},
            )
            record.slots.all().delete()
            if hours != 'always':
                OpeningHourSlot.objects.bulk_create([
                    OpeningHourSlot(hours=record, weekday=wd,
                                    open_time=open_t, close_time=close_t)
                    for wd, open_t, close_t in hours
                ])
            created += was_created
            updated += not was_created

        for name, province, lat, lng in DISTRICTS:
            base = name.lower().replace(' ', '_')

            save(f'{base}_hospital',
                 name=(f'{name} General Hospital', f'{name} මහ රෝහල',
                       f'{name} பொது மருத்துவமனை'),
                 department=('Ministry of Health', 'සෞඛ්‍ය අමාත්‍යාංශය',
                             'சுகாதார அமைச்சு'),
                 category='hospital', district=name,
                 lat=jitter(lat), lng=jitter(lng),
                 address=(f'Hospital Road, {name}', f'රෝහල් පාර, {name}',
                          f'மருத்துவமனை சாலை, {name}'),
                 phones=[(('Main line', 'ප්‍රධාන මාර්ගය', 'முதன்மை இணைப்பு'), phone_number()),
                         (('Emergency / ETU', 'හදිසි ඒකකය', 'அவசர பிரிவு'), '1990')],
                 hours='always', is_emergency=True)

            save(f'{base}_police',
                 name=(f'{name} Police Station', f'{name} පොලිස් ස්ථානය',
                       f'{name} காவல் நிலையம்'),
                 department=('Sri Lanka Police', 'ශ්‍රී ලංකා පොලිසිය',
                             'இலங்கை காவல்துறை'),
                 category='police', district=name,
                 lat=jitter(lat), lng=jitter(lng),
                 address=(f'Station Road, {name}', f'ස්ටේෂන් පාර, {name}',
                          f'நிலைய சாலை, {name}'),
                 phones=[(('OIC', 'ස්ථානාධිපති', 'OIC'), phone_number()),
                         (('Emergency', 'හදිසි', 'அவசரம்'), '119')],
                 hours='always', is_emergency=True)

            save(f'{base}_secretariat',
                 name=(f'{name} District Secretariat',
                       f'{name} දිස්ත්‍රික් ලේකම් කාර්යාලය',
                       f'{name} மாவட்ட செயலகம்'),
                 department=('Ministry of Public Administration',
                             'රාජ්‍ය පරිපාලන අමාත්‍යාංශය',
                             'பொது நிர்வாக அமைச்சு'),
                 category='secretariat', district=name,
                 lat=jitter(lat), lng=jitter(lng),
                 address=(f'District Secretariat, {name}',
                          f'දිස්ත්‍රික් ලේකම් කාර්යාලය, {name}',
                          f'மாவட்ட செயலகம், {name}'),
                 phones=[(('General', 'පොදු', 'பொது'), phone_number())],
                 hours=OFFICE_HOURS,
                 website=f"https://www.{base.replace('_', '')}.dist.gov.lk")

            save(f'{base}_ceb',
                 name=(f'CEB Area Office — {name}',
                       f'ලංවිම ප්‍රාදේශීය කාර්යාලය — {name}',
                       f'CEB பகுதி அலுவலகம் — {name}'),
                 department=('Ceylon Electricity Board', 'ලංකා විදුලිබල මණ්ඩලය',
                             'இலங்கை மின்சார சபை'),
                 category='ceb', district=name,
                 lat=jitter(lat), lng=jitter(lng),
                 address=(f'Main Street, {name}', f'ප්‍රධාන වීදිය, {name}',
                          f'பிரதான வீதி, {name}'),
                 phones=[(('Breakdown hotline', 'බිඳවැටීම් අංකය', 'பழுது இணைப்பு'), '1987'),
                         (('Area office', 'ප්‍රාදේශීය කාර්යාලය', 'பகுதி அலுவலகம்'), phone_number())],
                 hours='always', website='https://www.ceb.lk')

            save(f'{base}_water',
                 name=(f'NWSDB Regional Office — {name}',
                       f'ජල මණ්ඩල කාර්යාලය — {name}',
                       f'NWSDB பிராந்திய அலுவலகம் — {name}'),
                 department=('National Water Supply & Drainage Board',
                             'ජාතික ජල සම්පාදන මණ්ඩලය',
                             'தேசிய நீர் வழங்கல் வாரியம்'),
                 category='water', district=name,
                 lat=jitter(lat), lng=jitter(lng),
                 address=(f'Water Board Road, {name}', f'ජල මණ්ඩල පාර, {name}',
                          f'நீர் வாரிய சாலை, {name}'),
                 phones=[(('Hotline', 'ක්ෂණික අංකය', 'அவசர இணைப்பு'), '1954')],
                 hours=OFFICE_HOURS, website='https://www.waterboard.lk')

            save(f'{base}_post',
                 name=(f'{name} Main Post Office',
                       f'{name} ප්‍රධාන තැපැල් කාර්යාලය',
                       f'{name} பிரதான அஞ்சலகம்'),
                 department=('Sri Lanka Post', 'ශ්‍රී ලංකා තැපැල්', 'இலங்கை அஞ்சல்'),
                 category='post', district=name,
                 lat=jitter(lat), lng=jitter(lng),
                 address=(f'Post Office Road, {name}', f'තැපැල් කාර්යාල පාර, {name}',
                          f'அஞ்சலக சாலை, {name}'),
                 phones=[(('Counter', 'කවුන්ටරය', 'கவுண்டர்'), phone_number())],
                 hours=OFFICE_HOURS, website='https://slpost.gov.lk')

            save(f'{base}_court',
                 name=(f"{name} Magistrate's Court",
                       f'{name} මහේස්ත්‍රාත් අධිකරණය',
                       f'{name} நீதவான் நீதிமன்றம்'),
                 department=('Ministry of Justice', 'අධිකරණ අමාත්‍යාංශය',
                             'நீதி அமைச்சு'),
                 category='court', district=name,
                 lat=jitter(lat), lng=jitter(lng),
                 address=(f'Courts Complex, {name}', f'අධිකරණ සංකීර්ණය, {name}',
                          f'நீதிமன்ற வளாகம், {name}'),
                 phones=[(('Registrar', 'රෙජිස්ට්‍රාර්', 'பதிவாளர்'), phone_number())],
                 hours=OFFICE_HOURS)

            save(f'{base}_school',
                 name=(f'{name} Zonal Education Office',
                       f'{name} කලාප අධ්‍යාපන කාර්යාලය',
                       f'{name} வலயக் கல்வி அலுவலகம்'),
                 department=('Ministry of Education', 'අධ්‍යාපන අමාත්‍යාංශය',
                             'கல்வி அமைச்சு'),
                 category='school', district=name,
                 lat=jitter(lat), lng=jitter(lng),
                 address=(f'Education Office Road, {name}',
                          f'අධ්‍යාපන කාර්යාල පාර, {name}',
                          f'கல்வி அலுவலக சாலை, {name}'),
                 phones=[(('Office', 'කාර්යාලය', 'அலுவலகம்'), phone_number())],
                 hours=OFFICE_HOURS)

            save(f'{base}_transport',
                 name=(f'SLTB Depot — {name}', f'ලංගම ඩිපෝව — {name}',
                       f'SLTB டிப்போ — {name}'),
                 department=('Sri Lanka Transport Board',
                             'ශ්‍රී ලංකා ගමනාගමන මණ්ඩලය',
                             'இலங்கை போக்குவரத்து சபை'),
                 category='transport', district=name,
                 lat=jitter(lat), lng=jitter(lng),
                 address=(f'Bus Stand Road, {name}', f'බස් නැවතුම් පාර, {name}',
                          f'பேருந்து நிலைய சாலை, {name}'),
                 phones=[(('Depot', 'ඩිපෝව', 'டிப்போ'), phone_number())],
                 hours=SLTB_HOURS)

        # Curated national flagship entry (richer detail).
        save('colombo_nhsl',
             name=('National Hospital of Sri Lanka', 'ශ්‍රී ලංකා ජාතික රෝහල',
                   'இலங்கை தேசிய மருத்துவமனை'),
             department=('Ministry of Health', 'සෞඛ්‍ය අමාත්‍යාංශය',
                         'சுகாதார அமைச்சு'),
             category='hospital', district='Colombo',
             lat=6.9176, lng=79.8672,
             address=('Regent Street, Colombo 10', 'රීජන්ට් වීදිය, කොළඹ 10',
                      'ரீஜண்ட் தெரு, கொழும்பு 10'),
             phones=[(('General', 'පොදු', 'பொது'), '0112691111'),
                     (('Accident service', 'හදිසි අනතුරු', 'விபத்து சேவை'), '0112691111')],
             hours='always',
             website='https://www.nhsl.health.gov.lk', whatsapp='+94112691111',
             is_emergency=True)

        self.stdout.write(self.style.SUCCESS(
            f'Seeded services: {created} created, {updated} updated '
            f'({Service.objects.count()} total).'))
