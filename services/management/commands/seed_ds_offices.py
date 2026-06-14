"""
Seed Divisional Secretariat offices for all 14 DS divisions in Jaffna district
(the main Jaffna DS was already seeded by seed_national.py).
"""
from django.core.management.base import BaseCommand
from django.db import transaction
from services.models import Service, Category, ServicePhone, OpeningHours, OpeningHourSlot


def ensure_category():
    cat, _ = Category.objects.update_or_create(
        code='secretariat',
        defaults={
            'name_en': 'Government Secretariats',
            'name_si': 'රාජ්‍ය ලේකම් කාර්යාල',
            'name_ta': 'அரசு செயலகங்கள்',
            'icon': 'account_balance_outlined',
            'color': '0xFF1565C0',
        }
    )
    return cat


def ph(number, label_en='Main Line', label_si='ප්‍රධාන රේඛාව', label_ta='முதன்மை இணைப்பு'):
    return {'number': number, 'label_en': label_en, 'label_si': label_si, 'label_ta': label_ta}


def add_hours(service):
    oh = OpeningHours.objects.create(service=service)
    for day in range(1, 6):  # Mon-Fri
        OpeningHourSlot.objects.create(hours=oh, weekday=day, open_time='08:30', close_time='16:30')
    return oh


# Jaffna district DS divisions (excluding the main Jaffna DS already seeded)
DS_OFFICES = [
    {
        'code': 'nallur_ds',
        'name_en': 'Divisional Secretariat – Nallur',
        'name_si': 'කොට්ඨාශ ලේකම් කාර්යාලය – නල්ලූර්',
        'name_ta': 'பிரிவு செயலகம் – நல்லூர்',
        'address_en': 'Nallur, Jaffna District, Northern Province',
        'lat': 9.6656, 'lng': 80.0108,
        'phone': '0212222105',
    },
    {
        'code': 'kopay_ds',
        'name_en': 'Divisional Secretariat – Kopay',
        'name_si': 'කොට්ඨාශ ලේකම් කාර්යාලය – කොපායි',
        'name_ta': 'பிரிவு செயலகம் – கோப்பாய்',
        'address_en': 'Kopay, Jaffna District, Northern Province',
        'lat': 9.6833, 'lng': 80.0500,
        'phone': '0212274017',
    },
    {
        'code': 'chavakachcheri_ds',
        'name_en': 'Divisional Secretariat – Chavakachcheri',
        'name_si': 'කොට්ඨාශ ලේකම් කාර්යාලය – චාවකච්චේරි',
        'name_ta': 'பிரிவு செயலகம் – சாவகச்சேரி',
        'address_en': 'Chavakachcheri, Jaffna District, Northern Province',
        'lat': 9.6581, 'lng': 80.1783,
        'phone': '0212270238',
    },
    {
        'code': 'vadamaradchi_ds',
        'name_en': 'Divisional Secretariat – Vadamaradchi (Point Pedro)',
        'name_si': 'කොට්ඨාශ ලේකම් කාර්යාලය – වඩමාරච්චි (පොයින්ට් පේදරෝ)',
        'name_ta': 'பிரிவு செயலகம் – வடமராட்சி (பருத்தித்துறை)',
        'address_en': 'Point Pedro, Jaffna District, Northern Province',
        'lat': 9.8150, 'lng': 80.2350,
        'phone': '0212263016',
    },
    {
        'code': 'vadamaradchi_east_ds',
        'name_en': 'Divisional Secretariat – Vadamaradchi East (Karaveddy)',
        'name_si': 'කොට්ඨාශ ලේකම් කාර්යාලය – වඩමාරච්චි නැගෙනහිර',
        'name_ta': 'பிரிவு செயலகம் – வடமராட்சி கிழக்கு (காரைவெட்டி)',
        'address_en': 'Karaveddy, Jaffna District, Northern Province',
        'lat': 9.7650, 'lng': 80.2100,
        'phone': '0212264502',
    },
    {
        'code': 'tellippalai_ds',
        'name_en': 'Divisional Secretariat – Tellippalai',
        'name_si': 'කොට්ඨාශ ලේකම් කාර්යාලය – තෙලිප්පළෙයි',
        'name_ta': 'பிரிவு செயலகம் – தெல்லிப்பழை',
        'address_en': 'Tellippalai, Jaffna District, Northern Province',
        'lat': 9.7500, 'lng': 80.0400,
        'phone': '0213212019',
    },
    {
        'code': 'kayts_ds',
        'name_en': 'Divisional Secretariat – Kayts',
        'name_si': 'කොට්ඨාශ ලේකම් කාර්යාලය – කයිට්ස්',
        'name_ta': 'பிரிவு செயலகம் – காரைநகர் (கைதடி)',
        'address_en': 'Kayts, Jaffna District, Northern Province',
        'lat': 9.6650, 'lng': 79.9700,
        'phone': '0213212505',
    },
    {
        'code': 'karainagar_ds',
        'name_en': 'Divisional Secretariat – Karainagar',
        'name_si': 'කොට්ඨාශ ලේකම් කාර්යාලය – කරෙයිනගර්',
        'name_ta': 'பிரிவு செயலகம் – காரைநகர்',
        'address_en': 'Karainagar, Jaffna District, Northern Province',
        'lat': 9.7333, 'lng': 79.8667,
        'phone': '0213216067',
    },
    {
        'code': 'manipay_ds',
        'name_en': 'Divisional Secretariat – Manipay',
        'name_si': 'කොට්ඨාශ ලේකම් කාර්යාලය – මාණිපාය',
        'name_ta': 'பிரிவு செயலகம் – மாணிப்பாய்',
        'address_en': 'Manipay, Jaffna District, Northern Province',
        'lat': 9.7100, 'lng': 80.0700,
        'phone': '0213213260',
    },
    {
        'code': 'sandilipay_ds',
        'name_en': 'Divisional Secretariat – Sandilipay',
        'name_si': 'කොට්ඨාශ ලේකම් කාර්යාලය – සන්ඩිලිපාය',
        'name_ta': 'பிரிவு செயலகம் – சண்டிலிப்பாய்',
        'address_en': 'Sandilipay, Jaffna District, Northern Province',
        'lat': 9.7250, 'lng': 80.0300,
        'phone': '0213213407',
    },
    {
        'code': 'island_north_ds',
        'name_en': 'Divisional Secretariat – Island North (Velanai)',
        'name_si': 'කොට්ඨාශ ලේකම් කාර්යාලය – ද්වීප උතුර (වේලාණෙයි)',
        'name_ta': 'பிரிவு செயலகம் – தீவு வடக்கு (வேலணை)',
        'address_en': 'Velanai, Jaffna District, Northern Province',
        'lat': 9.6900, 'lng': 79.9200,
        'phone': '0213215044',
    },
    {
        'code': 'island_south_ds',
        'name_en': 'Divisional Secretariat – Island South (Pungudutivu)',
        'name_si': 'කොට්ඨාශ ලේකම් කාර්යාලය – ද්වීප දකුණ (පුංකුඩුතීව්)',
        'name_ta': 'பிரிவு செயலகம் – தீவு தெற்கு (புங்குடுதீவு)',
        'address_en': 'Pungudutivu, Jaffna District, Northern Province',
        'lat': 9.6600, 'lng': 79.8950,
        'phone': '0213215312',
    },
    {
        'code': 'delft_ds',
        'name_en': 'Divisional Secretariat – Delft (Neduntheevu)',
        'name_si': 'කොට්ඨාශ ලේකම් කාර්යාලය – දෙල්ෆ්ට් (නෙදුන්තීව්)',
        'name_ta': 'பிரிவு செயலகம் – நெடுந்தீவு (டெல்ஃப்ட்)',
        'address_en': 'Neduntheevu (Delft Island), Jaffna District, Northern Province',
        'lat': 9.5500, 'lng': 79.6900,
        'phone': '0213215600',
    },
]


class Command(BaseCommand):
    help = 'Seed Jaffna district DS divisional secretariat offices'

    def add_arguments(self, parser):
        parser.add_argument('--fresh', action='store_true', help='Delete existing entries before seeding')

    @transaction.atomic
    def handle(self, *args, **options):
        cat = ensure_category()

        if options['fresh']:
            codes = [d['code'] for d in DS_OFFICES]
            deleted, _ = Service.objects.filter(code__in=codes).delete()
            self.stdout.write(f'Deleted {deleted} existing entries')

        created = updated = 0
        for ds in DS_OFFICES:
            phones = [ph(ds['phone'])] if ds.get('phone') else []
            svc, was_created = Service.objects.update_or_create(
                code=ds['code'],
                defaults={
                    'name_en': ds['name_en'],
                    'name_si': ds['name_si'],
                    'name_ta': ds['name_ta'],
                    'department_en': 'Divisional Secretariat',
                    'department_si': 'කොට්ඨාශ ලේකම් කාර්යාලය',
                    'department_ta': 'பிரிவு செயலகம்',
                    'category_id': 'government',
                    'address_en': ds['address_en'],
                    'address_si': ds['address_en'],
                    'address_ta': ds['address_en'],
                    'lat': ds['lat'],
                    'lng': ds['lng'],
                    'district': 'Jaffna',
                }
            )
            if was_created:
                created += 1
                if phones:
                    for p in phones:
                        ServicePhone.objects.create(
                            service=svc,
                            number=p['number'],
                            label_en=p['label_en'],
                            label_si=p['label_si'],
                            label_ta=p['label_ta'],
                        )
                add_hours(svc)
            else:
                updated += 1

        total = Service.objects.count()
        self.stdout.write(self.style.SUCCESS(
            f'Done — {created} created, {updated} updated. Total services: {total}'
        ))
