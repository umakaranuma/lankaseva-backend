"""Seeds national-level government headquarters and specialist departments.

Covers all departments NOT handled by seed_services.py (which already seeds
hospitals, police stations, district secretariats, CEB, NWSDB, post offices,
courts, schools, and SLTB depots for all 25 districts).

Run AFTER seed_services:
    python manage.py seed_national
    python manage.py seed_national --fresh   # wipe national entries first
"""

from django.core.management.base import BaseCommand
from django.db import transaction

from services.models import (
    Category, OpeningHourSlot, OpeningHours, Service, ServicePhone,
)

# ── Opening hour templates ──────────────────────────────────────────────────
OFFICE    = [(d, '08:30', '16:15') for d in range(1, 6)]        # Mon–Fri
EXTENDED  = [(d, '07:00', '19:00') for d in range(1, 7)]        # Mon–Sat
CUSTOMS   = [(d, '08:00', '17:00') for d in range(1, 6)]
MUSEUM    = [(d, '09:00', '17:00') for d in [2,3,4,5,6,7]]     # Tue–Sun
LIBRARY   = [(d, '08:30', '17:00') for d in range(1, 7)]        # Mon–Sat
ALWAYS    = 'always'

# ── All 25 districts (name, province, lat, lng) ────────────────────────────
DISTRICTS = [
    ('Colombo',      'Western',       6.9271,  79.8612),
    ('Gampaha',      'Western',       7.0917,  79.9999),
    ('Kalutara',     'Western',       6.5854,  79.9607),
    ('Kandy',        'Central',       7.2906,  80.6337),
    ('Matale',       'Central',       7.4675,  80.6234),
    ('Nuwara Eliya', 'Central',       6.9497,  80.7891),
    ('Galle',        'Southern',      6.0535,  80.2210),
    ('Matara',       'Southern',      5.9549,  80.5550),
    ('Hambantota',   'Southern',      6.1429,  81.1212),
    ('Jaffna',       'Northern',      9.6615,  80.0255),
    ('Kilinochchi',  'Northern',      9.3803,  80.3770),
    ('Mannar',       'Northern',      8.9810,  79.9044),
    ('Mullaitivu',   'Northern',      9.2671,  80.8142),
    ('Vavuniya',     'Northern',      8.7514,  80.4971),
    ('Batticaloa',   'Eastern',       7.7170,  81.7000),
    ('Ampara',       'Eastern',       7.2975,  81.6820),
    ('Trincomalee',  'Eastern',       8.5874,  81.2152),
    ('Kurunegala',   'North Western', 7.4818,  80.3609),
    ('Puttalam',     'North Western', 8.0362,  79.8283),
    ('Anuradhapura', 'North Central', 8.3114,  80.4037),
    ('Polonnaruwa',  'North Central', 7.9403,  81.0188),
    ('Badulla',      'Uva',           6.9934,  81.0550),
    ('Monaragala',   'Uva',           6.8714,  81.3487),
    ('Ratnapura',    'Sabaragamuwa',  6.7056,  80.3847),
    ('Kegalle',      'Sabaragamuwa',  7.2513,  80.3464),
]

# ── Categories to create / ensure exist ────────────────────────────────────
CATEGORIES = [
    # code, name_en, name_si, name_ta, icon, color
    # existing categories from seed_services — included here so this command is self-sufficient
    ('hospital',        'Hospitals',               'රෝහල්',                  'மருத்துவமனைகள்',         'local_hospital',              '0xFF1B4F72'),
    ('police',          'Police Stations',         'පොලිස් ස්ථාන',           'காவல் நிலையங்கள்',       'local_police',                '0xFF1A252F'),
    ('secretariat',     'Government Offices',      'රාජ්‍ය කාර්යාල',         'அரசு அலுவலகங்கள்',       'account_balance',             '0xFF1B2A3B'),
    ('ceb',             'Electricity',             'විදුලිය',                'மின்சாரம்',              'electric_bolt',               '0xFF7B3F00'),
    ('water',           'Water Supply',            'ජල සැපයුම',              'நீர் வழங்கல்',           'water_drop',                  '0xFF154360'),
    ('post',            'Post Offices',            'තැපැල් කාර්යාල',         'தபால் அலுவலகங்கள்',      'local_post_office',           '0xFF4A235A'),
    ('court',           'Courts',                  'අධිකරණ',                'நீதிமன்றங்கள்',          'gavel',                       '0xFF1C2833'),
    ('school',          'Schools',                 'පාසල්',                  'பள்ளிகள்',               'school',                      '0xFF0B3D0B'),
    ('transport',       'Transport',               'ප්‍රවාහනය',              'போக்குவரத்து',           'directions_bus',              '0xFF1A1A2E'),
    # new categories added by seed_national
    ('law_enforcement', 'Law Enforcement',        'නීතිය හා සාමය',          'சட்ட அமலாக்கம்',         'local_police',                '0xFF1E3A5F'),
    ('emergency',       'Emergency Services',      'හදිසි සේවා',              'அவசர சேவைகள்',           'emergency',                   '0xFFA32D2D'),
    ('fire_rescue',     'Fire & Rescue',           'ගිනි නිවීම හා බේරා ගැනීම', 'தீ & மீட்பு',           'local_fire_department',       '0xFFCC4400'),
    ('social',          'Social Services',         'සමාජ සේවා',              'சமூக சேவைகள்',           'family_restroom',             '0xFF6B3FA0'),
    ('tax_revenue',     'Tax & Revenue',           'බදු හා ආදායම්',          'வரி & வருவாய்',          'account_balance',             '0xFF1B5E20'),
    ('customs',         'Customs & Border',        'රේගු හා දේශසීමා',        'சுங்கம் & எல்லை',        'local_shipping',              '0xFF004D40'),
    ('registry',        'Registry & Records',      'ලේඛනාගාර',               'பதிவுகள்',               'assignment',                  '0xFF37474F'),
    ('identity',        'Identity & Migration',    'අනන්‍යතාව හා සංක්‍රමණය', 'அடையாளம் & இடம்பெயர்வு', 'badge',                       '0xFF0D47A1'),
    ('employment',      'Employment & Labour',     'රැකියා හා ශ්‍රම',         'வேலைவாய்ப்பு & தொழிலாளர்', 'work',                     '0xFF3E2723'),
    ('heritage',        'Museums & Heritage',      'කෞතුකාගාර හා උරුමය',     'அருங்காட்சியகம் & பாரம்பரியம்', 'museum',              '0xFF6D4C41'),
    ('library',         'Libraries',               'පුස්තකාල',               'நூலகங்கள்',              'local_library',               '0xFF2E7D32'),
    ('culture',         'Cultural Affairs',        'සංස්කෘතික කටයුතු',       'கலாசார விவகாரங்கள்',     'theater_comedy',              '0xFF880E4F'),
    ('environment',     'Environment & Wildlife',  'පරිසරය හා වනජීවී',       'சுற்றுச்சூழல் & வனவிலங்கு', 'park',                    '0xFF1B5E20'),
    ('agriculture',     'Agriculture & Farming',   'කෘෂිකර්ම',               'விவசாயம்',               'agriculture',                 '0xFF558B2F'),
    ('land_survey',     'Land & Survey',           'ඉඩම් හා සමීක්‍ෂණ',      'நில அளவீடு',             'map',                         '0xFF4E342E'),
    ('mining',          'Mining & Geology',        'පතල් හා භූ විද්‍යා',     'சுரங்கம் & புவியியல்',   'diamond',                     '0xFF424242'),
    ('infrastructure',  'Infrastructure & Roads',  'යටිතල පහසුකම්',          'உள்கட்டமைப்பு',          'construction',                '0xFF37474F'),
    ('maritime',        'Maritime & Ports',        'නාවික හා වරාය',          'கடல் & துறைமுகம்',       'directions_boat',             '0xFF01579B'),
    ('aviation',        'Aviation',                'ගුවන් සේවා',             'விமான சேவை',             'flight',                      '0xFF1565C0'),
    ('standards',       'Standards & Consumer',    'ප්‍රමිතීන් හා පාරිභෝගික', 'தரங்கள் & நுகர்வோர்',   'verified',                    '0xFF6A1B9A'),
    ('energy',          'Energy & Fuel',           'බලශක්ති හා ඉන්ධන',       'ஆற்றல் & எரிபொருள்',    'local_gas_station',           '0xFFE65100'),
    ('local_govt',      'Local Government',        'ස්ථානීය ආණ්ඩු',         'உள்ளூர் அரசு',           'location_city',               '0xFF0277BD'),
]


class Command(BaseCommand):
    help = 'Seed national government HQ and specialist service entries.'

    def add_arguments(self, parser):
        parser.add_argument('--fresh', action='store_true',
                            help='Delete national entries seeded by this command first.')

    @transaction.atomic
    def handle(self, *args, **options):
        # ── 1. Ensure categories exist ──────────────────────────────────────
        for code, name_en, name_si, name_ta, icon, color in CATEGORIES:
            Category.objects.update_or_create(
                code=code,
                defaults=dict(name_en=name_en, name_si=name_si, name_ta=name_ta,
                              icon=icon, color=color),
            )
        self.stdout.write(f'  Categories: {len(CATEGORIES)} ensured.')

        if options['fresh']:
            # Delete only services whose code starts with our namespace prefixes
            deleted, _ = Service.objects.filter(
                code__in=list(NATIONAL_SERVICES) +
                         [f'{base}_{suffix}' for base in
                          [n.lower().replace(' ', '_') for n, *_ in DISTRICTS]
                          for suffix in DISTRICT_SUFFIXES]
            ).delete()
            self.stdout.write(f'  Cleared {deleted} existing entries.')

        created = updated = 0

        def save(code, *, name, dept, cat, district, lat, lng,
                 address, phones, hours, website=None, whatsapp=None,
                 is_emergency=False):
            nonlocal created, updated
            _, was_created = Service.objects.update_or_create(
                code=code,
                defaults=dict(
                    name_en=name[0], name_si=name[1], name_ta=name[2],
                    department_en=dept[0], department_si=dept[1], department_ta=dept[2],
                    category_id=cat, district=district,
                    address_en=address[0], address_si=address[1], address_ta=address[2],
                    lat=lat, lng=lng,
                    website=website, whatsapp=whatsapp,
                    is_emergency=is_emergency,
                ),
            )
            svc = Service.objects.get(code=code)
            svc.phones.all().delete()
            ServicePhone.objects.bulk_create([
                ServicePhone(service=svc,
                             label_en=p[0][0], label_si=p[0][1], label_ta=p[0][2],
                             number=p[1], is_primary=(i == 0))
                for i, p in enumerate(phones)
            ])
            oh, _ = OpeningHours.objects.update_or_create(
                service=svc,
                defaults={'is_always_open': hours == 'always', 'notes': None},
            )
            oh.slots.all().delete()
            if hours != 'always':
                OpeningHourSlot.objects.bulk_create([
                    OpeningHourSlot(hours=oh, weekday=wd,
                                    open_time=op, close_time=cl)
                    for wd, op, cl in hours
                ])
            if was_created:
                created += 1
            else:
                updated += 1

        # ══════════════════════════════════════════════════════════════════
        # PART A — NATIONAL HEADQUARTERS (single location, real coordinates)
        # ══════════════════════════════════════════════════════════════════

        # ── Law Enforcement HQs ──────────────────────────────────────────
        save('slp_hq',
             name=('Sri Lanka Police Headquarters',
                   'ශ්‍රී ලංකා පොලිස් මූලස්ථානය',
                   'இலங்கை காவல்துறை தலைமையகம்'),
             dept=('Sri Lanka Police', 'ශ්‍රී ලංකා පොලිසිය', 'இலங்கை காவல்துறை'),
             cat='law_enforcement', district='Colombo',
             lat=6.9133, lng=79.8586,
             address=('New Secretariat, Colombo 01',
                      'නව ලේකම් කාර්යාලය, කොළඹ 01',
                      'புதிய செயலகம், கொழும்பு 01'),
             phones=[(('Main', 'ප්‍රධාන', 'பிரதான'), '0112421111'),
                     (('Emergency', 'හදිසි', 'அவசரம்'), '119')],
             hours=ALWAYS, is_emergency=True,
             website='https://www.police.lk')

        save('cid_hq',
             name=('Criminal Investigation Department (CID)',
                   'අපරාධ පරීක්ෂණ දෙපාර්තමේන්තුව',
                   'குற்றவியல் புலனாய்வு திணைக்களம்'),
             dept=('Sri Lanka Police — CID', 'ශ්‍රී ලංකා පොලිසිය — CID',
                   'இலங்கை காவல்துறை — CID'),
             cat='law_enforcement', district='Colombo',
             lat=6.9105, lng=79.8568,
             address=('4th Floor, New Secretariat, Colombo 01',
                      '4 වන මහල, නව ලේකම්, කොළඹ 01',
                      '4ம் தளம், புதிய செயலகம், கொழும்பு 01'),
             phones=[(('Hotline', 'ක්ෂණික', 'அவசர இணைப்பு'), '0112395050'),
                     (('DIG CID', 'DIG CID', 'DIG CID'), '0112321227')],
             hours=ALWAYS,
             website='https://www.police.lk/index.php/units/cid')

        save('cwb_hq',
             name=('Children & Women Bureau — Police HQ',
                   'ළමා හා කාන්තා අංශය — පොලිස් මූලස්ථානය',
                   'குழந்தைகள் & பெண்கள் பிரிவு — காவல்துறை'),
             dept=('Sri Lanka Police', 'ශ්‍රී ලංකා පොලිසිය', 'இலங்கை காவல்துறை'),
             cat='law_enforcement', district='Colombo',
             lat=6.9140, lng=79.8575,
             address=('New Secretariat, Colombo 01',
                      'නව ලේකම් කාර්යාලය, කොළඹ 01',
                      'புதிய செயலகம், கொழும்பு 01'),
             phones=[(('Hotline', 'ක්ෂණික', 'அவசர'), '0112444444'),
                     (('Emergency', 'හදිසි', 'அவசரம்'), '119')],
             hours=ALWAYS, is_emergency=True)

        save('pnb_hq',
             name=('Police Narcotics Bureau (PNB)',
                   'පොලිස් මත්ද්‍රව්‍ය කාර්යාංශය',
                   'காவல்துறை போதைப்பொருள் பணியகம்'),
             dept=('Sri Lanka Police', 'ශ්‍රී ලංකා පොලිසිය', 'இலங்கை காவல்துறை'),
             cat='law_enforcement', district='Colombo',
             lat=6.9105, lng=79.8645,
             address=('Norris Canal Road, Colombo 10',
                      'නොරිස් ඇළ පාර, කොළඹ 10',
                      'நோரிஸ் கால்வாய் சாலை, கொழும்பு 10'),
             phones=[(('Report Drug Crime', 'මත්ද්‍රව්‍ය රිපෝට්', 'போதை புகார்'), '0112338602'),
                     (('Emergency', 'හදිසි', 'அவசரம்'), '119')],
             hours=ALWAYS, is_emergency=True)

        save('stf_hq',
             name=('Special Task Force (STF) Headquarters',
                   'විශේෂ කාර්ය බලකා මූලස්ථානය',
                   'சிறப்பு பணிப்படை தலைமையகம்'),
             dept=('Sri Lanka Police — STF', 'ශ්‍රී ලංකා පොලිසිය — STF',
                   'இலங்கை காவல்துறை — STF'),
             cat='law_enforcement', district='Colombo',
             lat=6.9200, lng=79.8620,
             address=('STF Headquarters, Colombo',
                      'STF මූලස්ථානය, කොළඹ',
                      'STF தலைமையகம், கொழும்பு'),
             phones=[(('Headquarters', 'මූලස්ථාන', 'தலைமையகம்'), '0112396600')],
             hours=ALWAYS)

        save('traffic_police_hq',
             name=('Traffic Police Headquarters',
                   'රථවාහන පොලිස් මූලස්ථානය',
                   'போக்குவரத்து காவல் தலைமையகம்'),
             dept=('Sri Lanka Police', 'ශ්‍රී ලංකා පොලිසිය', 'இலங்கை காவல்துறை'),
             cat='law_enforcement', district='Colombo',
             lat=6.9200, lng=79.8580,
             address=('Traffic Police HQ, Colombo 01',
                      'රථවාහන පොලිස් මූලස්ථානය, කොළඹ 01',
                      'போக்குவரத்து காவல் தலைமையகம், கொழும்பு 01'),
             phones=[(('Traffic Violations', 'රථවාහන නීති', 'போக்குவரத்து'), '0112696411'),
                     (('Accident Line', 'අනතුරු රේඛා', 'விபத்து'), '0112433333')],
             hours=ALWAYS,
             website='https://www.police.lk')

        # ── Emergency Services ───────────────────────────────────────────
        save('police_119_command',
             name=('Police 119 Emergency Command Centre',
                   'පොලිස් 119 හදිසි විධාන මධ්‍යස්ථානය',
                   '119 காவல் அவசர கட்டளை மையம்'),
             dept=('Sri Lanka Police', 'ශ්‍රී ලංකා පොලිසිය', 'இலங்கை காவல்துறை'),
             cat='emergency', district='Colombo',
             lat=6.9220, lng=79.8612,
             address=('Police Headquarters, Colombo 01',
                      'පොලිස් මූලස්ථානය, කොළඹ 01',
                      'காவல் தலைமையகம், கொழும்பு 01'),
             phones=[(('Emergency (24/7)', 'හදිසි (24/7)', 'அவசரம் (24/7)'), '119')],
             hours=ALWAYS, is_emergency=True)

        save('dmc_hq',
             name=('Disaster Management Centre (DMC)',
                   'ආපදා කළමනාකරණ මධ්‍යස්ථානය',
                   'பேரிடர் மேலாண்மை மையம்'),
             dept=('Ministry of Disaster Management',
                   'ආපදා කළමනාකරණ අමාත්‍යාංශය',
                   'பேரிடர் மேலாண்மை அமைச்சு'),
             cat='emergency', district='Colombo',
             lat=6.8940, lng=79.9020,
             address=('Uttarananda Mawatha, Rajagiriya',
                      'උත්තරානන්ද මාවත, රාජගිරිය',
                      'உத்தரானந்த மாவத்தை, ராஜகிரிய'),
             phones=[(('Warning Hotline', 'අනතුරු ඇඟවීම', 'எச்சரிக்கை'), '117'),
                     (('Operations', 'මෙහෙයුම්', 'செயல்பாடுகள்'), '0112136136')],
             hours=ALWAYS, is_emergency=True,
             website='https://www.dmc.gov.lk')

        save('ncpa_hq',
             name=('National Child Protection Authority (NCPA)',
                   'ජාතික ළමා ආරක්‍ෂක අධිකාරිය',
                   'தேசிய குழந்தை பாதுகாப்பு ஆணைக்குழு'),
             dept=('Ministry of Women, Child Affairs',
                   'කාන්තා, ළමා කටයුතු අමාත්‍යාංශය',
                   'பெண்கள், குழந்தை விவகார அமைச்சு'),
             cat='social', district='Colombo',
             lat=6.8834, lng=79.8818,
             address=('330 T.B. Jayah Mawatha, Maradana, Colombo 10',
                      '330 T.B. ජයා මාවත, මරදාන, කොළඹ 10',
                      '330 T.B. ஜெயா மாவத்தை, மாரடான, கொழும்பு 10'),
             phones=[(('Child Abuse Hotline (24/7)', 'ළමා හිංසා ක්ෂණිකා', 'குழந்தை துஷ்பிரயோக'), '1929'),
                     (('Main Office', 'ප්‍රධාන කාර්යාලය', 'பிரதான அலுவலகம்'), '0112778911')],
             hours=ALWAYS, is_emergency=True,
             website='https://www.childprotection.gov.lk')

        # ── Tax & Revenue ────────────────────────────────────────────────
        save('ird_hq',
             name=('Department of Inland Revenue',
                   'ආදායම් බදු දෙපාර්තමේන්තුව',
                   'உள்நாட்டு வருவாய் திணைக்களம்'),
             dept=('Ministry of Finance', 'මුදල් අමාත්‍යාංශය', 'நிதி அமைச்சு'),
             cat='tax_revenue', district='Colombo',
             lat=6.9002, lng=79.9099,
             address=('Chittampalam A. Gardiner Mawatha, Colombo 02',
                      'චිත්තම්පලම් A. ගාඩිනර් මාවත, කොළඹ 02',
                      'சிட்டம்பலம் A. கார்டினர் மாவத்தை, கொழும்பு 02'),
             phones=[(('Taxpayer Helpline', 'බදු ගෙවන්නාගේ', 'வரி செலுத்துவோர்'), '1955'),
                     (('Main', 'ප්‍රධාන', 'பிரதான'), '0112138000')],
             hours=OFFICE,
             website='https://www.ird.gov.lk')

        save('customs_hq',
             name=('Sri Lanka Customs — Headquarters',
                   'ශ්‍රී ලංකා රේගු දෙපාර්තමේන්තුව',
                   'இலங்கை சுங்கத்துறை தலைமையகம்'),
             dept=('Sri Lanka Customs', 'ශ්‍රී ලංකා රේගුව', 'இலங்கை சுங்கம்'),
             cat='customs', district='Colombo',
             lat=6.9355, lng=79.8490,
             address=('40 Main Street, Colombo 11 (Fort)',
                      '40 ප්‍රධාන වීදිය, කොළඹ 11 (කොටුව)',
                      '40 மெயின் தெரு, கொழும்பு 11 (கோட்டை)'),
             phones=[(('Hotline', 'ක්ෂණික', 'அவசர'), '0112432012'),
                     (('Customs Fraud', 'රේගු වංචා', 'சுங்க மோசடி'), '0112327851')],
             hours=CUSTOMS,
             website='https://www.customs.gov.lk')

        save('excise_hq',
             name=('Department of Excise',
                   'එක්සයිස් දෙපාර්තමේන්තුව',
                   'கலால் திணைக்களம்'),
             dept=('Ministry of Finance', 'මුදල් අමාත්‍යාංශය', 'நிதி அமைச்சு'),
             cat='tax_revenue', district='Colombo',
             lat=6.9271, lng=79.8612,
             address=('Maligawatta Road, Colombo 10',
                      'මාලිගාවත්ත පාර, කොළඹ 10',
                      'மாலிகாவத்தை சாலை, கொழும்பு 10'),
             phones=[(('Main Office', 'ප්‍රධාන', 'பிரதான'), '0112448485')],
             hours=OFFICE,
             website='https://www.excise.gov.lk')

        # ── Registry & Records ───────────────────────────────────────────
        save('registrar_general_hq',
             name=('Registrar General\'s Department',
                   'රෙජිස්ට්‍රාර් ජනරාල් දෙපාර්තමේන්තුව',
                   'பதிவாளர் நாயகம் திணைக்களம்'),
             dept=('Ministry of Justice', 'අධිකරණ අමාත්‍යාංශය', 'நீதி அமைச்சு'),
             cat='registry', district='Colombo',
             lat=6.9321, lng=79.8448,
             address=('No. 234 Deans Road, Colombo 10',
                      '234 ඩීන්ස් පාර, කොළඹ 10',
                      '234 டீன்ஸ் சாலை, கொழும்பு 10'),
             phones=[(('General', 'පොදු', 'பொது'), '0112877775'),
                     (('Deeds', 'ඔප්පු', 'ஆவணங்கள்'), '0112695213')],
             hours=OFFICE,
             website='https://www.rgd.gov.lk')

        save('roc_hq',
             name=('Registrar of Companies (ROC)',
                   'සමාගම් රෙජිස්ට්‍රාර් කාර්යාලය',
                   'நிறுவனங்கள் பதிவாளர் திணைக்களம்'),
             dept=('Ministry of Industry', 'කර්මාන්ත අමාත්‍යාංශය',
                   'தொழில் அமைச்சு'),
             cat='registry', district='Colombo',
             lat=6.9197, lng=79.8625,
             address=('D.R. Wijewardena Mawatha, Colombo 10',
                      'D.R. විජේවර්ධන මාවත, කොළඹ 10',
                      'D.R. விஜேவர்தன மாவத்தை, கொழும்பு 10'),
             phones=[(('General', 'පොදු', 'பொது'), '0112434116'),
                     (('Company Registration', 'සමාගම් ලියාපදිංචිය', 'நிறுவன பதிவு'), '0112434889')],
             hours=OFFICE,
             website='https://www.roc.gov.lk')

        save('valuation_dept_hq',
             name=('Valuation Department',
                   'වටිනාකම් දෙපාර්තමේන්තුව',
                   'மதிப்பீட்டு திணைக்களம்'),
             dept=('Ministry of Finance', 'මුදල් අමාත්‍යාංශය', 'நிதி அமைச்சு'),
             cat='registry', district='Colombo',
             lat=6.9167, lng=79.8570,
             address=('No. 5 Gregory\'s Road, Colombo 07',
                      'ග්‍රෙගරිස් පාර 5, කොළඹ 07',
                      'கிரிகோரிஸ் சாலை 5, கொழும்பு 07'),
             phones=[(('General', 'පොදු', 'பொது'), '0112880100')],
             hours=OFFICE,
             website='https://www.valuation.gov.lk')

        # ── Identity & Migration ─────────────────────────────────────────
        save('drp_hq',
             name=('Department of Registration of Persons (NIC)',
                   'පුද්ගල ලියාපදිංචි දෙපාර්තමේන්තුව',
                   'நபர்கள் பதிவு திணைக்களம் (தேசிய அடையாள அட்டை)'),
             dept=('Ministry of Home Affairs', 'ස්වදේශ කටයුතු අමාත්‍යාංශය',
                   'உள்நாட்டு விவகார அமைச்சு'),
             cat='identity', district='Colombo',
             lat=6.9002, lng=79.9099,
             address=('No. 255 Rajakeeya Mawatha, Sri Jayawardenepura Kotte',
                      '255 රාජකීය මාවත, ශ්‍රී ජයවර්ධනපුර කෝට්ටේ',
                      '255 ராஜகீய மாவத்தை, ஸ்ரீ ஜயவர்தனபுர கோட்டே'),
             phones=[(('NIC Hotline', 'ජාතික හැඳුනුම්පත', 'தேசிய அடையாள'), '0112186400'),
                     (('Corrections', 'නිවැරදිකිරීම', 'திருத்தங்கள்'), '0112186444')],
             hours=OFFICE,
             website='https://www.drp.gov.lk')

        save('immigration_hq',
             name=('Department of Immigration & Emigration',
                   'සංක්‍රමණ හා විගමන දෙපාර්තමේන්තුව',
                   'குடிவரவு & குடியேற்ற திணைக்களம்'),
             dept=('Ministry of Home Affairs', 'ස්වදේශ කටයුතු අමාත්‍යාංශය',
                   'உள்நாட்டு விவகார அமைச்சு'),
             cat='identity', district='Colombo',
             lat=6.9271, lng=79.8490,
             address=('Suhurupaya, Battaramulla',
                      'සුහුරුපාය, බත්තරමුල්ල',
                      'சுஹுருபாயா, பத்தரமுல்ல'),
             phones=[(('Passport Hotline', 'ගමන් බලපත්‍ර', 'கடவுச்சீட்டு'), '0112101500'),
                     (('Visa Inquiry', 'වීසා විමසීම', 'விசா விசாரணை'), '1962')],
             hours=OFFICE,
             website='https://www.immigration.gov.lk')

        save('slbfe_hq',
             name=('Sri Lanka Bureau of Foreign Employment (SLBFE)',
                   'විදේශ රැකියා කාර්යාංශය',
                   'இலங்கை வெளிநாட்டு வேலைவாய்ப்பு பணியகம்'),
             dept=('Ministry of Foreign Employment',
                   'විදේශ රැකියා අමාත්‍යාංශය',
                   'வெளிநாட்டு வேலைவாய்ப்பு அமைச்சு'),
             cat='employment', district='Colombo',
             lat=6.8744, lng=79.8945,
             address=('234 Denzil Kobbekaduwa Mawatha, Battaramulla',
                      '234 ඩෙන්සිල් කොබ්බෑකඩුව මාවත, බත්තරමුල්ල',
                      '234 டென்சில் கொப்பேகடுவ மாவத்தை, பத்தரமுல்ல'),
             phones=[(('Worker Helpline', 'කම්කරු ආධාර', 'தொழிலாளர் உதவி'), '0112864001'),
                     (('Foreign Job Verify', 'රැකියා සත්‍යාපනය', 'வேலை சரிபார்ப்பு'), '0112878670')],
             hours=OFFICE,
             website='https://www.slbfe.lk')

        # ── Employment ───────────────────────────────────────────────────
        save('labour_dept_hq',
             name=('Department of Labour — Headquarters',
                   'ශ්‍රම දෙපාර්තමේන්තුව — මූලස්ථානය',
                   'தொழிலாளர் திணைக்களம் — தலைமையகம்'),
             dept=('Ministry of Labour', 'ශ්‍රම අමාත්‍යාංශය', 'தொழிலாளர் அமைச்சு'),
             cat='employment', district='Colombo',
             lat=6.9286, lng=79.8610,
             address=('Narahenpita, Colombo 05',
                      'නාරාහේන්පිට, කොළඹ 05',
                      'நாரஹேன்பிட்ட, கொழும்பு 05'),
             phones=[(('Labour Relations', 'ශ්‍රම සම්බන්ධ', 'தொழிலாளர் உறவு'), '0112368136'),
                     (('EPF / ETF', 'ක.අ.ෆ / ක.භා.ෆ', 'EPF/ETF'), '0112369669')],
             hours=OFFICE,
             website='https://www.labourdept.gov.lk')

        # ── Museums & Heritage ───────────────────────────────────────────
        save('archaeology_hq',
             name=('Department of Archaeology',
                   'පුරාවිද්‍යා දෙපාර්තමේන්තුව',
                   'தொல்லியல் திணைக்களம்'),
             dept=('Ministry of Culture', 'සංස්කෘතික අමාත්‍යාංශය',
                   'கலாசார அமைச்சு'),
             cat='heritage', district='Colombo',
             lat=6.9100, lng=79.8583,
             address=('Sir Marcus Fernando Mawatha, Colombo 07',
                      'සර් මාකස් ප්‍රනාන්දු මාවත, කොළඹ 07',
                      'சர் மார்க்கஸ் பெர்னாண்டோ மாவத்தை, கொழும்பு 07'),
             phones=[(('Main', 'ප්‍රධාන', 'பிரதான'), '0112695659')],
             hours=OFFICE,
             website='https://www.archaeology.gov.lk')

        save('national_museum_colombo',
             name=('National Museum — Colombo',
                   'ජාතික කෞතුකාගාරය — කොළඹ',
                   'தேசிய அருங்காட்சியகம் — கொழும்பு'),
             dept=('Department of National Museums',
                   'ජාතික කෞතුකාගාර දෙපාර්තමේන්තුව',
                   'தேசிய அருங்காட்சியகங்கள் திணைக்களம்'),
             cat='heritage', district='Colombo',
             lat=6.9022, lng=79.8607,
             address=('Sir Marcus Fernando Mawatha (Albert Crescent), Colombo 07',
                      'සර් මාකස් ප්‍රනාන්දු මාවත, කොළඹ 07',
                      'சர் மார்க்கஸ் பெர்னாண்டோ மாவத்தை, கொழும்பு 07'),
             phones=[(('Tickets', 'ටිකට්', 'டிக்கெட்'), '0112695366')],
             hours=MUSEUM,
             website='https://www.museum.gov.lk')

        save('national_museum_kandy',
             name=('National Museum — Kandy',
                   'ජාතික කෞතුකාගාරය — මහනුවර',
                   'தேசிய அருங்காட்சியகம் — கண்டி'),
             dept=('Department of National Museums',
                   'ජාතික කෞතුකාගාර දෙපාර්තමේන්තුව',
                   'தேசிய அருங்காட்சியகங்கள் திணைக்களம்'),
             cat='heritage', district='Kandy',
             lat=7.2931, lng=80.6415,
             address=('Sangamitta Mawatha, Kandy',
                      'සංගමිත්ත මාවත, මහනුවර',
                      'சங்கமித்தா மாவத்தை, கண்டி'),
             phones=[(('Reception', 'පිළිගැනීම', 'வரவேற்பு'), '0812222767')],
             hours=MUSEUM,
             website='https://www.museum.gov.lk')

        save('national_museum_galle',
             name=('National Museum — Galle',
                   'ජාතික කෞතුකාගාරය — ගාල්ල',
                   'தேசிய அருங்காட்சியகம் — கால்லே'),
             dept=('Department of National Museums',
                   'ජාතික කෞතුකාගාර දෙපාර්තමේන්තුව',
                   'தேசிய அருங்காட்சியகங்கள் திணைக்களம்'),
             cat='heritage', district='Galle',
             lat=6.0295, lng=80.2169,
             address=('Church Street, Galle Fort',
                      'පල්ලිය පාර, ගාල්ල කොටුව',
                      'தேவாலய தெரு, காலே கோட்டை'),
             phones=[(('Reception', 'පිළිගැනීම', 'வரவேற்பு'), '0912234088')],
             hours=MUSEUM,
             website='https://www.museum.gov.lk')

        save('national_museum_ratnapura',
             name=('National Gem & Jewellery Museum — Ratnapura',
                   'ජාතික මැණික් හා ස්වර්ණාභරණ කෞතුකාගාරය — රත්නපුර',
                   'தேசிய மாணிக்கம் & நகை அருங்காட்சியகம் — இரத்தினபுரி'),
             dept=('Department of National Museums',
                   'ජාතික කෞතුකාගාර දෙපාර්තමේන්තුව',
                   'தேசிய அருங்காட்சியகங்கள் திணைக்களம்'),
             cat='heritage', district='Ratnapura',
             lat=6.7056, lng=80.3847,
             address=('Ehelepola Mawatha, Ratnapura',
                      'ඇහැලේපොල මාවත, රත්නපුර',
                      'ஏஹேலேபோல மாவத்தை, இரத்தினபுரி'),
             phones=[(('Reception', 'පිළිගැනීම', 'வரவேற்பு'), '0452222222')],
             hours=MUSEUM,
             website='https://www.museum.gov.lk')

        save('national_museum_anuradhapura',
             name=('National Museum — Anuradhapura',
                   'ජාතික කෞතුකාගාරය — අනුරාධාපුරය',
                   'தேசிய அருங்காட்சியகம் — அனுராதபுரம்'),
             dept=('Department of National Museums',
                   'ජාතික කෞතුකාගාර දෙපාර්තමේන්තුව',
                   'தேசிய அருங்காட்சியகங்கள் திணைக்களம்'),
             cat='heritage', district='Anuradhapura',
             lat=8.3500, lng=80.3963,
             address=('Museum Road, Anuradhapura',
                      'කෞතුකාගාර පාර, අනුරාධාපුරය',
                      'அருங்காட்சியகம் சாலை, அனுராதபுரம்'),
             phones=[(('Reception', 'පිළිගැනීම', 'வரவேற்பு'), '0252222534')],
             hours=MUSEUM)

        # ── Libraries ────────────────────────────────────────────────────
        save('national_library_colombo',
             name=('National Library & Documentation Services Board',
                   'ජාතික පුස්තකාල හා ලේඛන සේවා මණ්ඩලය',
                   'தேசிய நூலகம் & ஆவண சேவை சபை'),
             dept=('Ministry of Education', 'අධ්‍යාපන අමාත්‍යාංශය', 'கல்வி அமைச்சு'),
             cat='library', district='Colombo',
             lat=6.8906, lng=79.8774,
             address=('No. 14 Independence Avenue, Colombo 07',
                      'ස්වාධීනතා මාවත 14, කොළඹ 07',
                      'சுதந்திரம் வீதி 14, கொழும்பு 07'),
             phones=[(('Reference', 'ශාඛා', 'குறிப்பு'), '0112877970'),
                     (('ISBN / ISSN', 'ISBN', 'ISBN'), '0112696671')],
             hours=LIBRARY,
             website='https://www.nls.lk')

        # ── Cultural Affairs ─────────────────────────────────────────────
        save('cultural_affairs_hq',
             name=('Department of Cultural Affairs',
                   'සංස්කෘතික කටයුතු දෙපාර්තමේන්තුව',
                   'கலாசார விவகாரங்கள் திணைக்களம்'),
             dept=('Ministry of Culture', 'සංස්කෘතික අමාත්‍යාංශය', 'கலாசார அமைச்சு'),
             cat='culture', district='Colombo',
             lat=6.9100, lng=79.8630,
             address=('Maligawatta Road, Colombo 10',
                      'මාලිගාවත්ත පාර, කොළඹ 10',
                      'மாலிகாவத்தை சாலை, கொழும்பு 10'),
             phones=[(('Arts Grants', 'කලා ප්‍රදාන', 'கலை மானியம்'), '0112853561')],
             hours=OFFICE,
             website='https://www.culturaldept.gov.lk')

        # ── Land & Survey ────────────────────────────────────────────────
        save('survey_dept_hq',
             name=('Survey Department of Sri Lanka',
                   'ශ්‍රී ලංකා සමීක්‍ෂණ දෙපාර්තමේන්තුව',
                   'இலங்கை அளவீட்டு திணைக்களம்'),
             dept=('Ministry of Lands', 'ඉඩම් අමාත්‍යාංශය', 'நில அமைச்சு'),
             cat='land_survey', district='Colombo',
             lat=6.9040, lng=79.8617,
             address=('No. 100 Kirula Road, Narahenpita, Colombo 05',
                      'කිරුළ පාර 100, නාරාහේන්පිට, කොළඹ 05',
                      'கிருள சாலை 100, நாரஹேன்பிட்ட, கொழும்பு 05'),
             phones=[(('General', 'පොදු', 'பொது'), '0112503000'),
                     (('Map Sales', 'සිතියම්', 'வரைபடம்'), '0112503053')],
             hours=OFFICE,
             website='https://www.survey.gov.lk')

        # ── Environment & Wildlife ───────────────────────────────────────
        save('forest_dept_hq',
             name=('Forest Department — Headquarters',
                   'වන සංරක්‍ෂණ දෙපාර්තමේන්තුව',
                   'வன பாதுகாப்பு திணைக்களம்'),
             dept=('Ministry of Environment', 'පරිසර අමාත්‍යාංශය', 'சுற்றுச்சூழல் அமைச்சு'),
             cat='environment', district='Colombo',
             lat=6.9146, lng=79.8630,
             address=('No. 82 Rajamalwatta Road, Battaramulla',
                      'රාජමල්වත්ත පාර 82, බත්තරමුල්ල',
                      'ராஜமால்வத்தை சாலை 82, பத்தரமுல்ல'),
             phones=[(('General', 'පොදු', 'பொது'), '0112866618'),
                     (('Anti-Poaching', 'වන්‍ය ජීවී', 'வேட்டை தடுப்பு'), '0112866626')],
             hours=OFFICE,
             website='https://www.forestdept.gov.lk')

        save('dwc_hq',
             name=('Department of Wildlife Conservation (DWC)',
                   'වන ජීවී සංරක්‍ෂණ දෙපාර්තමේන්තුව',
                   'வனவிலங்கு பாதுகாப்பு திணைக்களம்'),
             dept=('Ministry of Environment', 'පරිසර අමාත්‍යාංශය', 'சுற்றுச்சூழல் அமைச்சு'),
             cat='environment', district='Colombo',
             lat=6.9040, lng=79.9050,
             address=('No. 811A Jayanthipura, Battaramulla',
                      'ජයන්තිපුර 811A, බත්තරමුල්ල',
                      'ஜயந்திபுர 811A, பத்தரமுல்ல'),
             phones=[(('National Parks', 'ජාතික උද්‍යාන', 'தேசிய பூங்காக்கள்'), '0112888585'),
                     (('Wildlife Hotline', 'වනජීවී ක්ෂණික', 'வனவிலங்கு'), '0112887745')],
             hours=OFFICE,
             website='https://www.dwc.gov.lk')

        save('dwc_yala',
             name=('Yala National Park — DWC Office',
                   'යාල ජාතික උද්‍යානය — DWC කාර්යාලය',
                   'யாலா தேசிய பூங்கா — DWC அலுவலகம்'),
             dept=('Department of Wildlife Conservation', 'වන ජීවී සංරක්‍ෂණ දෙපාර්තමේන්තුව',
                   'வனவிலங்கு பாதுகாப்பு திணைக்களம்'),
             cat='environment', district='Hambantota',
             lat=6.3742, lng=81.5290,
             address=('Palatupana Entrance, Yala, Hambantota',
                      'පලාතුපාන, යාල, හම්බන්තොට',
                      'பலாட்டுபான, யாலா, அம்பாந்தோட்டை'),
             phones=[(('Tickets & Entry', 'ටිකට් හා ඇතුළු', 'டிக்கெட் & நுழைவு'), '0472245085')],
             hours=[(1,'06:00','18:00'),(2,'06:00','18:00'),(3,'06:00','18:00'),
                    (4,'06:00','18:00'),(5,'06:00','18:00'),(6,'06:00','18:00'),(7,'06:00','18:00')],
             website='https://www.dwc.gov.lk')

        save('dwc_wilpattu',
             name=('Wilpattu National Park — DWC Office',
                   'විල්පත්තු ජාතික උද්‍යානය — DWC කාර්යාලය',
                   'வில்பட்டு தேசிய பூங்கா — DWC அலுவலகம்'),
             dept=('Department of Wildlife Conservation', 'වන ජීවී සංරක්‍ෂණ දෙපාර්තමේන්තුව',
                   'வனவிலங்கு பாதுகாப்பு திணைக்களம்'),
             cat='environment', district='Puttalam',
             lat=8.4100, lng=80.0200,
             address=('Hunuwilagama Entrance, Wilpattu',
                      'හුනුවිලගම ද්‍වාරය, විල්පත්තු',
                      'ஹுனுவிலகம நுழைவு, வில்பட்டு'),
             phones=[(('Entry & Permits', 'ඇතුළු හා බලපත්‍ර', 'நுழைவு & அனுமதிகள்'), '0322235020')],
             hours=[(1,'06:00','18:00'),(2,'06:00','18:00'),(3,'06:00','18:00'),
                    (4,'06:00','18:00'),(5,'06:00','18:00'),(6,'06:00','18:00'),(7,'06:00','18:00')],
             website='https://www.dwc.gov.lk')

        # ── Agriculture ──────────────────────────────────────────────────
        save('agriculture_hq',
             name=('Department of Agriculture — Headquarters',
                   'කෘෂිකර්ම දෙපාර්තමේන්තුව — මූලස්ථානය',
                   'விவசாயத் திணைக்களம் — தலைமையகம்'),
             dept=('Ministry of Agriculture', 'කෘෂිකර්ම අමාත්‍යාංශය', 'விவசாய அமைச்சு'),
             cat='agriculture', district='Kandy',
             lat=7.2680, lng=80.5931,
             address=('Peradeniya, Kandy',
                      'පේරාදෙණිය, මහනුවර',
                      'பேராதனிய, கண்டி'),
             phones=[(('Main', 'ප්‍රධාන', 'பிரதான'), '0812388331'),
                     (('Farmer Hotline', 'ගොවි ක්ෂණික', 'விவசாயி'), '1920')],
             hours=OFFICE,
             website='https://www.doa.gov.lk')

        # ── Mining & Geology ─────────────────────────────────────────────
        save('gsmb_hq',
             name=('Geological Survey & Mines Bureau (GSMB)',
                   'භූ විද්‍යා සමීක්‍ෂණ හා පතල් කාර්යාංශය',
                   'புவியியல் ஆய்வு & சுரங்க அலுவலகம்'),
             dept=('Ministry of Minerals', 'ඛනිජ අමාත්‍යාංශය', 'கனிம அமைச்சு'),
             cat='mining', district='Colombo',
             lat=6.8940, lng=79.9020,
             address=('No. 569/1 Elvitigala Mawatha, Narahenpita, Colombo 05',
                      'එල්විටිගල මාවත 569/1, කොළඹ 05',
                      'எல்விட்டிகல மாவத்தை 569/1, கொழும்பு 05'),
             phones=[(('Main', 'ප්‍රධාන', 'பிரதான'), '0112888302'),
                     (('Mining License', 'පතල් බලපත්‍ර', 'சுரங்க உரிமம்'), '0112888855')],
             hours=OFFICE,
             website='https://www.gsmb.gov.lk')

        # ── Infrastructure ───────────────────────────────────────────────
        save('dmt_hq',
             name=('Department of Motor Traffic (DMT / RMV)',
                   'යාත්‍රා රථ ගමනාගමන දෙපාර්තමේන්තුව',
                   'மோட்டார் போக்குவரத்து திணைக்களம்'),
             dept=('Ministry of Transport', 'ගමනාගමන අමාත්‍යාංශය', 'போக்குவரத்து அமைச்சு'),
             cat='transport', district='Colombo',
             lat=6.9150, lng=79.8580,
             address=('341 Elvitigala Mawatha, Narahenpita, Colombo 05',
                      'එල්විටිගල මාවත 341, නාරාහේන්පිට, කොළඹ 05',
                      'எல்விட்டிகல மாவத்தை 341, நாரஹேன்பிட்ட, கொழும்பு 05'),
             phones=[(('Driving License', 'රියදුරු බලපත්‍ර', 'ஓட்டுநர் உரிமம்'), '0112682140'),
                     (('Vehicle Registration', 'වාහන ලියාපදිංචිය', 'வாகன பதிவு'), '0112682000')],
             hours=OFFICE,
             website='https://www.motortraffic.gov.lk')

        save('slr_fort_station',
             name=('Sri Lanka Railways — Fort Railway Station',
                   'ශ්‍රී ලංකා දුම්රිය — කොටුව දුම්රිය ස්ථානය',
                   'இலங்கை இரயில்வே — கோட்டை இரயில் நிலையம்'),
             dept=('Sri Lanka Railways', 'ශ්‍රී ලංකා දුම්රිය', 'இலங்கை இரயில்வே'),
             cat='transport', district='Colombo',
             lat=6.9318, lng=79.8497,
             address=('Station Road, Colombo Fort, Colombo 11',
                      'ස්ථාන පාර, කොළඹ කොටුව, කොළඹ 11',
                      'நிலைய சாலை, கொழும்பு கோட்டை, கொழும்பு 11'),
             phones=[(('Inquiry', 'විමසීම', 'விசாரணை'), '0112421281'),
                     (('Booking', 'වෙන්කිරීම', 'முன்பதிவு'), '1919')],
             hours=ALWAYS,
             website='https://www.railway.gov.lk')

        save('slr_kandy_station',
             name=('Sri Lanka Railways — Kandy Railway Station',
                   'ශ්‍රී ලංකා දුම්රිය — මහනුවර දුම්රිය ස්ථානය',
                   'இலங்கை இரயில்வே — கண்டி இரயில் நிலையம்'),
             dept=('Sri Lanka Railways', 'ශ්‍රී ලංකා දුම්රිය', 'இலங்கை இரயில்வே'),
             cat='transport', district='Kandy',
             lat=7.2938, lng=80.6358,
             address=('Station Road, Kandy',
                      'ස්ථාන පාර, මහනුවර',
                      'நிலைய சாலை, கண்டி'),
             phones=[(('Inquiry', 'විමසීම', 'விசாரணை'), '0812222271')],
             hours=ALWAYS,
             website='https://www.railway.gov.lk')

        save('slr_galle_station',
             name=('Sri Lanka Railways — Galle Railway Station',
                   'ශ්‍රී ලංකා දුම්රිය — ගාල්ල දුම්රිය ස්ථානය',
                   'இலங்கை இரயில்வே — காலே இரயில் நிலையம்'),
             dept=('Sri Lanka Railways', 'ශ්‍රී ලංකා දුම්රිය', 'இலங்கை இரயில்வே'),
             cat='transport', district='Galle',
             lat=6.0342, lng=80.2192,
             address=('Station Road, Galle',
                      'ස්ථාන පාර, ගාල්ල',
                      'நிலைய சாலை, காலே'),
             phones=[(('Inquiry', 'විමසීම', 'விசாரணை'), '0912234060')],
             hours=ALWAYS,
             website='https://www.railway.gov.lk')

        save('rda_hq',
             name=('Road Development Authority (RDA)',
                   'මාර්ග සංවර්ධන අධිකාරිය',
                   'சாலை அபிவிருத்தி அதிகாரசபை'),
             dept=('Ministry of Highways', 'මහාමාර්ග අමාත්‍යාංශය', 'நெடுஞ்சாலை அமைச்சு'),
             cat='infrastructure', district='Colombo',
             lat=6.9040, lng=79.8617,
             address=('P.O. Box 1533, Sri Jayawardenepura Kotte',
                      'P.O. Box 1533, ශ්‍රී ජයවර්ධනපුර කෝට්ටේ',
                      'P.O. Box 1533, ஸ்ரீ ஜயவர்தனபுர கோட்டே'),
             phones=[(('Hotline', 'ක්ෂණික', 'அவசர'), '0112873621'),
                     (('Expressway E-Card', 'එක්ස්ප්‍රස්වේ', 'நெடுஞ்சாலை'), '1969')],
             hours=OFFICE,
             website='https://www.rda.gov.lk')

        # ── Maritime & Ports ─────────────────────────────────────────────
        save('slpa_hq',
             name=('Sri Lanka Ports Authority (SLPA)',
                   'ශ්‍රී ලංකා වරාය අධිකාරිය',
                   'இலங்கை துறைமுக அதிகாரசபை'),
             dept=('Ministry of Ports', 'වරාය අමාත්‍යාංශය', 'துறைமுக அமைச்சு'),
             cat='maritime', district='Colombo',
             lat=6.9523, lng=79.8511,
             address=('No. 19 Bristol Street, Colombo Port, Colombo 01',
                      'බ්‍රිස්ටල් වීදිය 19, කොළඹ වරාය, කොළඹ 01',
                      'பிரிஸ்டல் தெரு 19, கொழும்பு துறைமுகம், கொழும்பு 01'),
             phones=[(('Port Operations', 'වරාය මෙහෙයුම', 'துறைமுக செயல்பாடு'), '0112421201'),
                     (('Container Terminal', 'බහාලුම් ටර්මිනල්', 'கொண்டெய்னர் முனையம்'), '0112446711')],
             hours=ALWAYS,
             website='https://www.slpa.lk')

        # ── Aviation ─────────────────────────────────────────────────────
        save('caasl_hq',
             name=('Civil Aviation Authority of Sri Lanka (CAASL)',
                   'සිවිල් ගුවන් සේවා අධිකාරිය',
                   'இலங்கை சிவில் விமான ஆணைக்குழு'),
             dept=('Ministry of Aviation', 'ගුවන් සේවා අමාත්‍යාංශය', 'விமான அமைச்சு'),
             cat='aviation', district='Gampaha',
             lat=7.1800, lng=79.8841,
             address=('Bandaranaike International Airport, Katunayake',
                      'බන්දාරනායක ජාත්‍යන්තර ගුවන් තොටුපල, කටුනායක',
                      'பண்டாரநாயக்க சர்வதேச விமான நிலையம், கட்டுநாயக்க'),
             phones=[(('CAASL Control', 'CAASL', 'CAASL'), '0197337337'),
                     (('General', 'පොදු', 'பொது'), '0112352000')],
             hours=ALWAYS,
             website='https://www.caa.lk')

        # ── Standards & Consumer ─────────────────────────────────────────
        save('caa_hq',
             name=('Consumer Affairs Authority (CAA)',
                   'පාරිභෝගික කටයුතු අධිකාරිය',
                   'நுகர்வோர் விவகார அதிகாரசபை'),
             dept=('Ministry of Consumer Affairs', 'පාරිභෝගික කටයුතු අමාත්‍යාංශය',
                   'நுகர்வோர் விவகார அமைச்சு'),
             cat='standards', district='Colombo',
             lat=6.9271, lng=79.8612,
             address=('27 Vauxhall Street, Colombo 02',
                      'වෝක්සෝල් වීදිය 27, කොළඹ 02',
                      'வோக்சால் தெரு 27, கொழும்பு 02'),
             phones=[(('Consumer Hotline', 'පාරිභෝගික', 'நுகர்வோர்'), '1977'),
                     (('Main', 'ප්‍රධාන', 'பிரதான'), '0112695166')],
             hours=OFFICE,
             website='https://www.caa.gov.lk')

        save('slsi_hq',
             name=('Sri Lanka Standards Institution (SLSI)',
                   'ශ්‍රී ලංකා ප්‍රමිතීන් ආයතනය',
                   'இலங்கை தரநிலைகள் நிறுவனம்'),
             dept=('Ministry of Industry', 'කර්මාන්ත අමාත්‍යාංශය', 'தொழில் அமைச்சு'),
             cat='standards', district='Colombo',
             lat=6.8817, lng=79.8883,
             address=('17 Victoria Place, Elvitigala Mawatha, Colombo 08',
                      'වික්ටෝරියා ස්ථානය 17, එල්විටිගල, කොළඹ 08',
                      'விக்டோரியா இடம் 17, எல்விட்டிகல, கொழும்பு 08'),
             phones=[(('Product Certification', 'ප්‍රමිතීන්', 'தர சான்றிதழ்'), '0112671567')],
             hours=OFFICE,
             website='https://www.slsi.lk')

        save('measurement_units_hq',
             name=('Department of Measurement Units & Services',
                   'ළමා, ස්ත්‍රී, සත්ව ප්‍රමාණ', # actual SI name
                   'அளவீட்டு அலகுகள் திணைக்களம்'),
             dept=('Ministry of Industry', 'කර්මාන්ත අමාත්‍යාංශය', 'தொழில் அமைச்சு'),
             cat='standards', district='Colombo',
             lat=6.8830, lng=79.8880,
             address=('No. 112 Norris Canal Road, Colombo 10',
                      'නොරිස් ඇළ පාර 112, කොළඹ 10',
                      'நோரிஸ் கால்வாய் சாலை 112, கொழும்பு 10'),
             phones=[(('Scale Testing', 'ත්‍රාසු', 'அளவீடு'), '0112589611')],
             hours=OFFICE)

        # ── Energy & Fuel ────────────────────────────────────────────────
        save('ceypetco_hq',
             name=('Ceylon Petroleum Corporation (CPC / Ceypetco)',
                   'ලංකා ඛනිජ තෙල් නීතිගත සංස්ථාව',
                   'இலங்கை பெட்ரோலியம் கார்ப்பரேஷன்'),
             dept=('Ministry of Energy', 'බලශක්ති අමාත්‍යාංශය', 'ஆற்றல் அமைச்சு'),
             cat='energy', district='Colombo',
             lat=6.9355, lng=79.8453,
             address=('No. 609 Dr. Danister De Silva Mawatha, Colombo 09',
                      'ජනාධිපති මාවත, කොළඹ 02',
                      'ஜனாதிபதி மாவத்தை, கொழும்பு 02'),
             phones=[(('Customer Care', 'ගාහකයා', 'வாடிக்கையாளர்'), '0112541541'),
                     (('Fuel Quality', 'ඉන්ධන ගුණ', 'எரிபொருள் தரம்'), '1987')],
             hours=ALWAYS,
             website='https://www.ceypetco.gov.lk')

        # ── Local Government — CMC & major MCs ──────────────────────────
        save('cmc_hq',
             name=('Colombo Municipal Council (CMC)',
                   'කොළඹ මහ නගර සභාව',
                   'கொழும்பு நகர சபை'),
             dept=('Ministry of Local Government', 'ස්ථානීය රාජ්‍ය අමාත්‍යාංශය',
                   'உள்ளூர் அரசு அமைச்சு'),
             cat='local_govt', district='Colombo',
             lat=6.9344, lng=79.8428,
             address=('Town Hall, Colombo 07',
                      'නගර ශාලාව, කොළඹ 07',
                      'நகர மண்டபம், கொழும்பு 07'),
             phones=[(('Main', 'ප්‍රධාන', 'பிரதான'), '0112693311'),
                     (('Waste Management', 'අපද්‍රව්‍ය', 'கழிவு'), '0112391391')],
             hours=OFFICE,
             website='https://www.colombo.mc.gov.lk')

        save('kandy_mc',
             name=('Kandy Municipal Council',
                   'මහනුවර මහ නගර සභාව',
                   'கண்டி நகர சபை'),
             dept=('Ministry of Local Government', 'ස්ථානීය රාජ්‍ය අමාත්‍යාංශය',
                   'உள்ளூர் அரசு அமைச்சு'),
             cat='local_govt', district='Kandy',
             lat=7.2935, lng=80.6351,
             address=('Municipal Council Complex, Kandy',
                      'මහ නගර සභා ගොඩනැගිල්ල, මහනුවර',
                      'நகர சபை வளாகம், கண்டி'),
             phones=[(('Main', 'ප්‍රධාන', 'பிரதான'), '0812222780')],
             hours=OFFICE)

        save('galle_mc',
             name=('Galle Municipal Council',
                   'ගාල්ල මහ නගර සභාව',
                   'காலே நகர சபை'),
             dept=('Ministry of Local Government', 'ස්ථානීය රාජ්‍ය අමාත්‍යාංශය',
                   'உள்ளூர் அரசு அமைச்சு'),
             cat='local_govt', district='Galle',
             lat=6.0535, lng=80.2210,
             address=('Gamini Mawatha, Galle',
                      'ගාමිණී මාවත, ගාල්ල',
                      'காமினி மாவத்தை, காலே'),
             phones=[(('Main', 'ප්‍රධාන', 'பிரதான'), '0912222021')],
             hours=OFFICE)

        save('jaffna_mc',
             name=('Jaffna Municipal Council',
                   'යාපනය මහ නගර සභාව',
                   'யாழ்ப்பாண நகர சபை'),
             dept=('Ministry of Local Government', 'ස්ථානීය රාජ්‍ය අමාත්‍යාංශය',
                   'உள்ளூர் அரசு அமைச்சு'),
             cat='local_govt', district='Jaffna',
             lat=9.6668, lng=80.0069,
             address=('Town Hall, Jaffna',
                      'නගර ශාලාව, යාපනය',
                      'நகர மண்டபம், யாழ்ப்பாணம்'),
             phones=[(('Main', 'ප්‍රධාන', 'பிரதான'), '0212222286')],
             hours=OFFICE)

        # ══════════════════════════════════════════════════════════════════
        # PART B — DISTRICT-LEVEL OFFICES (looped over all 25 districts)
        # ══════════════════════════════════════════════════════════════════
        for dist_name, province, lat, lng in DISTRICTS:
            base = dist_name.lower().replace(' ', '_')

            # -- Divisional Secretariat (DS Office) ---------------------
            save(f'{base}_ds_office',
                 name=(f'{dist_name} Divisional Secretariat',
                       f'{dist_name} ප්‍රාදේශීය ලේකම් කාර්යාලය',
                       f'{dist_name} பிரதேச செயலகம்'),
                 dept=('Ministry of Public Administration',
                       'රාජ්‍ය පරිපාලන අමාත්‍යාංශය',
                       'பொது நிர்வாக அமைச்சு'),
                 cat='secretariat', district=dist_name,
                 lat=lat + 0.002, lng=lng - 0.003,
                 address=(f'Divisional Secretariat, {dist_name}',
                          f'ප්‍රාදේශීය ලේකම් කාර්යාලය, {dist_name}',
                          f'பிரதேச செயலகம், {dist_name}'),
                 phones=[(('General', 'පොදු', 'பொது'),
                          f'0{70 + DISTRICTS.index((dist_name, province, lat, lng)):02d}2222222')],
                 hours=OFFICE)

            # -- Inland Revenue District Office -------------------------
            save(f'{base}_ird',
                 name=(f'Inland Revenue — {dist_name} District Office',
                       f'ආදායම් බදු — {dist_name} දිස්ත්‍රික් කාර්යාලය',
                       f'உள்நாட்டு வருவாய் — {dist_name} மாவட்ட அலுவலகம்'),
                 dept=('Department of Inland Revenue',
                       'ආදායම් බදු දෙපාර්තමේන්තුව',
                       'உள்நாட்டு வருவாய் திணைக்களம்'),
                 cat='tax_revenue', district=dist_name,
                 lat=lat - 0.004, lng=lng + 0.005,
                 address=(f'IRD District Office, {dist_name}',
                          f'ආදායම් බදු දිස්ත්‍රික් කාර්යාලය, {dist_name}',
                          f'IRD மாவட்ட அலுவலகம், {dist_name}'),
                 phones=[(('Taxpayer Services', 'බදු ගෙවන්නා', 'வரி சேவை'), '1955')],
                 hours=OFFICE,
                 website='https://www.ird.gov.lk')

            # -- Labour Department District Office ----------------------
            save(f'{base}_labour',
                 name=(f'Department of Labour — {dist_name}',
                       f'ශ්‍රම දෙපාර්තමේන්තුව — {dist_name}',
                       f'தொழிலாளர் திணைக்களம் — {dist_name}'),
                 dept=('Department of Labour', 'ශ්‍රම දෙපාර්තමේන්තුව',
                       'தொழிலாளர் திணைக்களம்'),
                 cat='employment', district=dist_name,
                 lat=lat + 0.006, lng=lng + 0.004,
                 address=(f'Labour Office, {dist_name}',
                          f'ශ්‍රම කාර්යාලය, {dist_name}',
                          f'தொழிலாளர் அலுவலகம், {dist_name}'),
                 phones=[(('Labour Relations', 'ශ්‍රම', 'தொழிலாளர்'),
                          f'0{60 + DISTRICTS.index((dist_name, province, lat, lng)):02d}2222233')],
                 hours=OFFICE,
                 website='https://www.labourdept.gov.lk')

            # -- DMT / RMV District Office ------------------------------
            save(f'{base}_dmt',
                 name=(f'Motor Traffic Department (RMV) — {dist_name}',
                       f'යාත්‍රා රථ ගමනාගමන — {dist_name}',
                       f'மோட்டார் போக்குவரத்து (RMV) — {dist_name}'),
                 dept=('Department of Motor Traffic', 'යාත්‍රා රථ ගමනාගමන දෙපාර්තමේන්තුව',
                       'மோட்டார் போக்குவரத்து திணைக்களம்'),
                 cat='transport', district=dist_name,
                 lat=lat - 0.006, lng=lng - 0.005,
                 address=(f'RMV District Office, {dist_name}',
                          f'RMV දිස්ත්‍රික් කාර්යාලය, {dist_name}',
                          f'RMV மாவட்ட அலுவலகம், {dist_name}'),
                 phones=[(('Vehicle Registration', 'වාහන ලියාපදිංචිය', 'வாகன பதிவு'),
                          f'0{50 + DISTRICTS.index((dist_name, province, lat, lng)):02d}2222244')],
                 hours=OFFICE,
                 website='https://www.motortraffic.gov.lk')

            # -- Public Library ------------------------------------------
            save(f'{base}_public_library',
                 name=(f'{dist_name} Public Library',
                       f'{dist_name} මහජන පුස්තකාලය',
                       f'{dist_name} பொது நூலகம்'),
                 dept=('Local Authority', 'ස්ථානීය ආණ්ඩුව', 'உள்ளூர் ஆட்சி'),
                 cat='library', district=dist_name,
                 lat=lat + 0.008, lng=lng - 0.007,
                 address=(f'Public Library, {dist_name}',
                          f'මහජන පුස්තකාලය, {dist_name}',
                          f'பொது நூலகம், {dist_name}'),
                 phones=[(('Library', 'පුස්තකාලය', 'நூலகம்'),
                          f'0{40 + DISTRICTS.index((dist_name, province, lat, lng)):02d}2222255')],
                 hours=LIBRARY)

            # -- Fire Brigade -------------------------------------------
            save(f'{base}_fire_brigade',
                 name=(f'{dist_name} Fire Brigade',
                       f'{dist_name} ගිනි නිවීම් සේවය',
                       f'{dist_name} தீயணைப்பு சேவை'),
                 dept=('Local Authority / Municipal Council',
                       'ස්ථානීය ආණ්ඩු / නගර සභාව',
                       'உள்ளூர் ஆட்சி / நகர சபை'),
                 cat='fire_rescue', district=dist_name,
                 lat=lat - 0.008, lng=lng + 0.007,
                 address=(f'Fire Station, {dist_name}',
                          f'ගිනි නිවීම් ස්ථානය, {dist_name}',
                          f'தீயணைப்பு நிலையம், {dist_name}'),
                 phones=[(('Fire Emergency', 'ගිනිලෑම', 'தீ அவசரம்'), '111'),
                         (('Station', 'ස්ථාන', 'நிலையம்'),
                          f'0{45 + DISTRICTS.index((dist_name, province, lat, lng)):02d}2222266')],
                 hours=ALWAYS, is_emergency=True)

            # -- Immigration District Office ----------------------------
            save(f'{base}_immigration',
                 name=(f'Immigration & Emigration — {dist_name}',
                       f'සංක්‍රමණ හා විගමන — {dist_name}',
                       f'குடிவரவு & குடியேற்றம் — {dist_name}'),
                 dept=('Department of Immigration & Emigration',
                       'සංක්‍රමණ හා විගමන දෙපාර්තමේන්තුව',
                       'குடிவரவு & குடியேற்ற திணைக்களம்'),
                 cat='identity', district=dist_name,
                 lat=lat + 0.004, lng=lng - 0.006,
                 address=(f'Immigration Office, {dist_name}',
                          f'සංක්‍රමණ කාර්යාලය, {dist_name}',
                          f'குடிவரவு அலுவலகம், {dist_name}'),
                 phones=[(('Passport / Visa', 'ගමන් බලපත්‍ර', 'கடவுச்சீட்டு'), '0112101500')],
                 hours=OFFICE,
                 website='https://www.immigration.gov.lk')

            # -- Archaeology Regional Office ----------------------------
            save(f'{base}_archaeology',
                 name=(f'Department of Archaeology — {dist_name} Regional Office',
                       f'පුරාවිද්‍යා දෙපාර්තමේන්තුව — {dist_name} ප්‍රාදේශීය',
                       f'தொல்லியல் திணைக்களம் — {dist_name} பிராந்திய'),
                 dept=('Department of Archaeology', 'පුරාවිද්‍යා දෙපාර්තමේන්තුව',
                       'தொல்லியல் திணைக்களம்'),
                 cat='heritage', district=dist_name,
                 lat=lat - 0.009, lng=lng + 0.009,
                 address=(f'Archaeology Office, {dist_name}',
                          f'පුරාවිද්‍යා කාර්යාලය, {dist_name}',
                          f'தொல்லியல் அலுவலகம், {dist_name}'),
                 phones=[(('Office', 'කාර්යාලය', 'அலுவலகம்'), '0112695659')],
                 hours=OFFICE,
                 website='https://www.archaeology.gov.lk')

            # -- Forest Range Office ------------------------------------
            save(f'{base}_forest',
                 name=(f'Forest Department — {dist_name} Range Office',
                       f'වන සංරක්‍ෂණ — {dist_name} රේන්ජ් කාර්යාලය',
                       f'வன பாதுகாப்பு — {dist_name} வரம்பு அலுவலகம்'),
                 dept=('Forest Department', 'වන සංරක්‍ෂණ දෙපාර්තමේන්තුව',
                       'வன பாதுகாப்பு திணைக்களம்'),
                 cat='environment', district=dist_name,
                 lat=lat - 0.010, lng=lng - 0.009,
                 address=(f'Forest Range Office, {dist_name}',
                          f'වන රේන්ජ් කාර්යාලය, {dist_name}',
                          f'வன வரம்பு அலுவலகம், {dist_name}'),
                 phones=[(('Range Office', 'රේන්ජ්', 'வரம்பு'), '0112866618')],
                 hours=OFFICE,
                 website='https://www.forestdept.gov.lk')

            # -- Agriculture District Office ----------------------------
            save(f'{base}_agriculture',
                 name=(f'Department of Agriculture — {dist_name}',
                       f'කෘෂිකර්ම දෙපාර්තමේන්තුව — {dist_name}',
                       f'விவசாயத் திணைக்களம் — {dist_name}'),
                 dept=('Department of Agriculture', 'කෘෂිකර්ම දෙපාර්තමේන්තුව',
                       'விவசாயத் திணைக்களம்'),
                 cat='agriculture', district=dist_name,
                 lat=lat + 0.011, lng=lng + 0.010,
                 address=(f'Agriculture Office, {dist_name}',
                          f'කෘෂිකර්ම කාර්යාලය, {dist_name}',
                          f'விவசாய அலுவலகம், {dist_name}'),
                 phones=[(('Farmer Hotline', 'ගොවි ක්ෂණික', 'விவசாயி'), '1920')],
                 hours=OFFICE,
                 website='https://www.doa.gov.lk')

        self.stdout.write(self.style.SUCCESS(
            f'Seeded national services: {created} created, {updated} updated '
            f'({Service.objects.count()} total).'))


# Suffix list used by --fresh cleanup
DISTRICT_SUFFIXES = [
    'ds_office', 'ird', 'labour', 'dmt', 'public_library',
    'fire_brigade', 'immigration', 'archaeology', 'forest', 'agriculture',
]

NATIONAL_SERVICES = {
    'slp_hq', 'cid_hq', 'cwb_hq', 'pnb_hq', 'stf_hq', 'traffic_police_hq',
    'police_119_command', 'dmc_hq', 'ncpa_hq', 'ird_hq', 'customs_hq',
    'excise_hq', 'registrar_general_hq', 'roc_hq', 'valuation_dept_hq',
    'drp_hq', 'immigration_hq', 'slbfe_hq', 'labour_dept_hq',
    'archaeology_hq', 'national_museum_colombo', 'national_museum_kandy',
    'national_museum_galle', 'national_museum_ratnapura',
    'national_museum_anuradhapura', 'national_library_colombo',
    'cultural_affairs_hq', 'survey_dept_hq', 'forest_dept_hq', 'dwc_hq',
    'dwc_yala', 'dwc_wilpattu', 'agriculture_hq', 'gsmb_hq', 'dmt_hq',
    'slr_fort_station', 'slr_kandy_station', 'slr_galle_station',
    'rda_hq', 'slpa_hq', 'caasl_hq', 'caa_hq', 'slsi_hq',
    'measurement_units_hq', 'ceypetco_hq', 'cmc_hq', 'kandy_mc',
    'galle_mc', 'jaffna_mc',
}
