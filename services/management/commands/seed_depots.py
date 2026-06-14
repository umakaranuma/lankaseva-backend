"""Seeds SLTB bus depots and major inter-provincial bus stands across Sri Lanka.

Covers Jaffna sub-depots (Kopay, Kokkuvil, Karainagar, etc.) plus all major
SLTB regional depots for every district.  Run after seed_services:

    python manage.py seed_depots
    python manage.py seed_depots --fresh   # wipe and re-seed only these entries
"""

from django.core.management.base import BaseCommand
from django.db import transaction

from services.models import Category, OpeningHours, OpeningHourSlot, Service, ServicePhone

SLTB_HOURS = [(d, '05:00', '21:00') for d in range(1, 7)] + [(7, '06:00', '20:00')]
ALWAYS = 'always'

MOH    = 'Sri Lanka Transport Board (SLTB)'
MOH_SI = 'ශ්‍රී ලංකා ගමනාගමන මණ්ඩලය (ශ්‍රී ලංගම)'
MOH_TA = 'இலங்கை போக்குவரத்து சபை (இ.போ.ச)'


class Command(BaseCommand):
    help = 'Seed SLTB bus depots and major bus stands for all districts.'

    def add_arguments(self, parser):
        parser.add_argument('--fresh', action='store_true',
                            help='Delete depot entries seeded by this command first.')

    @transaction.atomic
    def handle(self, *args, **options):
        Category.objects.update_or_create(
            code='transport',
            defaults=dict(name_en='Transport', name_si='ප්‍රවාහනය',
                          name_ta='போக்குவரத்து',
                          icon='directions_bus', color='0xFF1A1A2E'),
        )

        if options['fresh']:
            Service.objects.filter(code__in=list(DEPOT_CODES)).delete()
            self.stdout.write('Cleared existing depot entries.')

        created = updated = 0

        def save(code, *, name_en, name_si, name_ta,
                 district, lat, lng,
                 addr_en, addr_si, addr_ta,
                 phones, hours=SLTB_HOURS):
            nonlocal created, updated
            _, was_created = Service.objects.update_or_create(
                code=code,
                defaults=dict(
                    name_en=name_en, name_si=name_si, name_ta=name_ta,
                    department_en=MOH, department_si=MOH_SI, department_ta=MOH_TA,
                    category_id='transport', district=district,
                    address_en=addr_en, address_si=addr_si, address_ta=addr_ta,
                    lat=lat, lng=lng, is_emergency=False,
                ),
            )
            svc = Service.objects.get(code=code)
            svc.phones.all().delete()
            ServicePhone.objects.bulk_create([
                ServicePhone(
                    service=svc,
                    label_en=p['label_en'], label_si=p['label_si'],
                    label_ta=p['label_ta'], number=p['number'],
                    is_primary=(i == 0),
                )
                for i, p in enumerate(phones)
            ])
            oh, _ = OpeningHours.objects.update_or_create(
                service=svc,
                defaults={'is_always_open': hours == ALWAYS, 'notes': None},
            )
            oh.slots.all().delete()
            if hours != ALWAYS:
                OpeningHourSlot.objects.bulk_create([
                    OpeningHourSlot(hours=oh, weekday=wd,
                                    open_time=op, close_time=cl)
                    for wd, op, cl in hours
                ])
            if was_created:
                created += 1
            else:
                updated += 1

        def ph(number, label_en='Inquiries',
               label_si='විමසීම්', label_ta='விசாரணை'):
            return {'number': number, 'label_en': label_en,
                    'label_si': label_si, 'label_ta': label_ta}

        def no_phone():
            return [ph('1989', 'SLTB Hotline', 'ශ්‍රී ලංගම ක්ෂණිකා', 'இ.போ.ச அவசர')]

        HOTLINE = no_phone()

        # ══════════════════════════════════════════════════════════════════
        # JAFFNA DISTRICT — full sub-depot coverage
        # ══════════════════════════════════════════════════════════════════

        save('jaffna_central_bus_stand',
             name_en='Jaffna Central Bus Stand',
             name_si='යාපනය මධ්‍යම බස් නිළය',
             name_ta='யாழ்ப்பாணம் மத்திய பேருந்து நிலையம்',
             district='Jaffna', lat=9.6668, lng=80.0118,
             addr_en='Hospital Road / Palaly Road Junction, Jaffna',
             addr_si='රෝහල් පාර / පලාලි පාර සන්ධිය, යාපනය',
             addr_ta='மருத்துவமனை சாலை / பலாலி சாலை சந்தி, யாழ்ப்பாணம்',
             phones=[ph('0212222207'), ph('1989', 'SLTB Hotline', 'ශ්‍රී ලංගම', 'இ.போ.ச')])

        save('jaffna_kondavil_depot',
             name_en='SLTB Kondavil Depot — Jaffna',
             name_si='කොන්ඩවිල් ශ්‍රී ලංගම ගබඩාව — යාපනය',
             name_ta='கொண்டாவில் இ.போ.ச கொட்டகை — யாழ்ப்பாணம்',
             district='Jaffna', lat=9.7080, lng=80.0400,
             addr_en='Palali Road, Kondavil, Jaffna',
             addr_si='පලාලි පාර, කොන්ඩවිල්, යාපනය',
             addr_ta='பலாலி சாலை, கொண்டாவில், யாழ்ப்பாணம்',
             phones=[ph('0212222207')])

        save('jaffna_kopay_depot',
             name_en='SLTB Kopay Sub-Depot & Bus Stand',
             name_si='කෝපේ ශ්‍රී ලංගම උප-ගබඩාව හා බස් නිළය',
             name_ta='கோப்பாய் இ.போ.ச உப-கொட்டகை & பேருந்து நிலையம்',
             district='Jaffna', lat=9.6833, lng=80.0500,
             addr_en='Kopay Junction, Kopay, Jaffna',
             addr_si='කෝපේ සන්ධිය, කෝපේ, යාපනය',
             addr_ta='கோப்பாய் சந்தி, கோப்பாய், யாழ்ப்பாணம்',
             phones=HOTLINE)

        save('jaffna_kokkuvil_depot',
             name_en='SLTB Kokkuvil Bus Stand',
             name_si='කොක්කුවිල් ශ්‍රී ලංගම බස් නිළය',
             name_ta='கொக்குவில் இ.போ.ச பேருந்து நிலையம்',
             district='Jaffna', lat=9.6917, lng=80.0208,
             addr_en='Kokkuvil, Jaffna',
             addr_si='කොක්කුවිල්, යාපනය',
             addr_ta='கொக்குவில், யாழ்ப்பாணம்',
             phones=HOTLINE)

        save('jaffna_karainagar_depot',
             name_en='SLTB Karainagar Depot (KR)',
             name_si='කරෙයිනාගර් ශ්‍රී ලංගම ගබඩාව (KR)',
             name_ta='காரைநகர் இ.போ.ச கொட்டகை (KR)',
             district='Jaffna', lat=9.7333, lng=79.8667,
             addr_en='Karainagar Island, Jaffna',
             addr_si='කරෙයිනාගර් දූපත, යාපනය',
             addr_ta='காரைநகர் தீவு, யாழ்ப்பாணம்',
             phones=HOTLINE)

        save('jaffna_chavakachcheri_depot',
             name_en='SLTB Chavakachcheri Depot',
             name_si='චාවකච්චේරි ශ්‍රී ලංගම ගබඩාව',
             name_ta='சாவகச்சேரி இ.போ.ச கொட்டகை',
             district='Jaffna', lat=9.6500, lng=80.1500,
             addr_en='Main Street, Chavakachcheri, Jaffna',
             addr_si='ප්‍රධාන වීදිය, චාවකච්චේරි, යාපනය',
             addr_ta='பிரதான தெரு, சாவகச்சேரி, யாழ்ப்பாணம்',
             phones=HOTLINE)

        save('jaffna_point_pedro_depot',
             name_en='SLTB Point Pedro Depot (PP)',
             name_si='පොයින්ට් පේද්‍රෝ ශ්‍රී ලංගම ගබඩාව (PP)',
             name_ta='பருத்தித்துறை இ.போ.ச கொட்டகை (PP)',
             district='Jaffna', lat=9.8170, lng=80.2350,
             addr_en='Vadamaradchi South, Point Pedro, Jaffna',
             addr_si='වඩමරාච්චි දකුණ, පොයින්ට් පේද්‍රෝ, යාපනය',
             addr_ta='வடமராட்சி தெற்கு, பருத்தித்துறை, யாழ்ப்பாணம்',
             phones=HOTLINE)

        save('jaffna_manipay_depot',
             name_en='SLTB Manipay Bus Stand',
             name_si='මනිපේ ශ්‍රී ලංගම බස් නිළය',
             name_ta='மணிப்பாய் இ.போ.ச பேருந்து நிலையம்',
             district='Jaffna', lat=9.7100, lng=80.0700,
             addr_en='Manipay, Jaffna',
             addr_si='මනිපේ, යාපනය',
             addr_ta='மணிப்பாய், யாழ்ப்பாணம்',
             phones=HOTLINE)

        save('jaffna_kayts_depot',
             name_en='SLTB Kayts Bus Stand',
             name_si='කයිට්ස් ශ්‍රී ලංගම බස් නිළය',
             name_ta='காரைதீவு இ.போ.ச பேருந்து நிலையம்',
             district='Jaffna', lat=9.6650, lng=79.9700,
             addr_en='Kayts Island, Jaffna',
             addr_si='කයිට්ස් දූපත, යාපනය',
             addr_ta='காரைதீவு, யாழ்ப்பாணம்',
             phones=HOTLINE)

        save('jaffna_tellippalai_depot',
             name_en='SLTB Tellippalai Bus Stand',
             name_si='තෙල්ලිපළාය ශ්‍රී ලංගම බස් නිළය',
             name_ta='தெல்லிப்பழை இ.போ.ச பேருந்து நிலையம்',
             district='Jaffna', lat=9.7500, lng=80.0400,
             addr_en='Tellippalai, Jaffna',
             addr_si='තෙල්ලිපළාය, යාපනය',
             addr_ta='தெல்லிப்பழை, யாழ்ப்பாணம்',
             phones=HOTLINE)

        # ══════════════════════════════════════════════════════════════════
        # KILINOCHCHI / MULLAITIVU / MANNAR / VAVUNIYA
        # ══════════════════════════════════════════════════════════════════

        save('kilinochchi_bus_stand',
             name_en='Kilinochchi SLTB Bus Stand (KC)',
             name_si='කිලිනොච්චි ශ්‍රී ලංගම බස් නිළය',
             name_ta='கிளிநொச்சி இ.போ.ச பேருந்து நிலையம்',
             district='Kilinochchi', lat=9.3833, lng=80.4067,
             addr_en='A9 Highway, Kilinochchi Town',
             addr_si='A9 මාර්ගය, කිලිනොච්චි නගරය',
             addr_ta='A9 நெடுஞ்சாலை, கிளிநொச்சி நகர்',
             phones=HOTLINE)

        save('mannar_bus_stand',
             name_en='Mannar SLTB Bus Stand (MN)',
             name_si='මන්නාරම ශ්‍රී ලංගම බස් නිළය',
             name_ta='மன்னார் இ.போ.ச பேருந்து நிலையம்',
             district='Mannar', lat=8.9781, lng=79.9137,
             addr_en='Mannar Town, Mannar Island',
             addr_si='මන්නාරම නගරය, මන්නාරම දූපත',
             addr_ta='மன்னார் நகர், மன்னார் தீவு',
             phones=HOTLINE)

        save('vavuniya_bus_stand',
             name_en='Vavuniya SLTB Bus Stand (VV)',
             name_si='වවුනියාව ශ්‍රී ලංගම බස් නිළය',
             name_ta='வவுனியா இ.போ.ச பேருந்து நிலையம்',
             district='Vavuniya', lat=8.7535, lng=80.4976,
             addr_en='A9 Highway, Vavuniya Town',
             addr_si='A9 මාර්ගය, වවුනියාව නගරය',
             addr_ta='A9 நெடுஞ்சாலை, வவுனியா நகர்',
             phones=HOTLINE)

        save('mullaitivu_bus_stand',
             name_en='Mullaitivu SLTB Bus Stand (MV)',
             name_si='මුල්ලයිතිව් ශ්‍රී ලංගම බස් නිළය',
             name_ta='முல்லைத்தீவு இ.போ.ச பேருந்து நிலையம்',
             district='Mullaitivu', lat=9.2700, lng=80.8150,
             addr_en='Mullaitivu Town',
             addr_si='මුල්ලයිතිව් නගරය',
             addr_ta='முல்லைத்தீவு நகர்',
             phones=HOTLINE)

        # ══════════════════════════════════════════════════════════════════
        # WESTERN PROVINCE
        # ══════════════════════════════════════════════════════════════════

        save('colombo_pettah_cbs',
             name_en='Central Bus Stand Pettah (Colombo)',
             name_si='පේට්ටාහ් මධ්‍යම බස් නිළය',
             name_ta='பேட்டாஹ் மத்திய பேருந்து நிலையம்',
             district='Colombo', lat=6.9351, lng=79.8544,
             addr_en='Olcott Mawatha (Saunders Place), Pettah, Colombo 11',
             addr_si='ඔල්කොට් මාවත, පේට්ටාහ්, කොළඹ 11',
             addr_ta='ஒல்கட் மாவத்தை, பேட்டாஹ், கொழும்பு 11',
             phones=[ph('0112328081'), ph('0112328082', 'Inquiries 2', 'විමසීම් 2', 'விசாரணை 2')])

        save('colombo_bastian_mawatha',
             name_en='Bastian Mawatha Bus Station (Colombo)',
             name_si='බස්ටියන් මාවත බස් නිළය',
             name_ta='பஸ்டியன் மாவத்தை பேருந்து நிலையம்',
             district='Colombo', lat=6.9336, lng=79.8553,
             addr_en='Bastian Mawatha / Olcott Mawatha, Colombo 11',
             addr_si='බස්ටියන් මාවත, කොළඹ 11',
             addr_ta='பஸ்டியன் மாவத்தை, கொழும்பு 11',
             phones=[ph('0112328083')])

        save('colombo_borella_depot',
             name_en='SLTB Borella / Meethotamulla Depot',
             name_si='බොරැල්ල / මීතොටමුල්ල ශ්‍රී ලංගම ගබඩාව',
             name_ta='போரெல்ல / மீத்தொத்தமுல்ல இ.போ.ச கொட்டகை',
             district='Colombo', lat=6.9359, lng=79.8885,
             addr_en='Meethotamulla, Colombo 15',
             addr_si='මීතොටමුල්ල, කොළඹ 15',
             addr_ta='மீத்தொத்தமுல்ல, கொழும்பு 15',
             phones=HOTLINE)

        save('colombo_thalangama_depot',
             name_en='SLTB Thalangama Depot',
             name_si='තලංගම ශ්‍රී ලංගම ගබඩාව',
             name_ta='தலங்கம இ.போ.ச கொட்டகை',
             district='Colombo', lat=6.9068, lng=79.9261,
             addr_en='Thalangama, Kolonnawa, Colombo',
             addr_si='තලංගම, කොලොන්නාව',
             addr_ta='தலங்கம, கொலொன்னாவ',
             phones=HOTLINE)

        save('colombo_angoda_depot',
             name_en='SLTB Angoda Depot (AG)',
             name_si='අංගොඩ ශ්‍රී ලංගම ගබඩාව (AG)',
             name_ta='அங்கொட இ.போ.ச கொட்டகை (AG)',
             district='Colombo', lat=6.9228, lng=79.9143,
             addr_en='Angoda, Kolonnawa, Colombo',
             addr_si='අංගොඩ, කොලොන්නාව',
             addr_ta='அங்கொட, கொலொன்னாவ',
             phones=HOTLINE)

        save('gampaha_ja_ela_depot',
             name_en='SLTB Ja-Ela Depot',
             name_si='ජා-ඇල ශ්‍රී ලංගම ගබඩාව',
             name_ta='ஜா-ஏல இ.போ.ச கொட்டகை',
             district='Gampaha', lat=7.0789, lng=79.8896,
             addr_en='Ja-Ela, Gampaha District',
             addr_si='ජා-ඇල, ගම්පහ දිස්ත්‍රික්කය',
             addr_ta='ஜா-ஏல, கம்பஹா மாவட்டம்',
             phones=HOTLINE)

        save('gampaha_negombo_depot',
             name_en='SLTB Negombo Depot (NB)',
             name_si='නේගොඹෝ ශ්‍රී ලංගම ගබඩාව (NB)',
             name_ta='நீர்கொழும்பு இ.போ.ச கொட்டகை (NB)',
             district='Gampaha', lat=7.2216, lng=79.8514,
             addr_en='Negombo Bus Depot, Negombo',
             addr_si='නේගොඹෝ ගබඩාව, නේගොඹෝ',
             addr_ta='நீர்கொழும்பு கொட்டகை, நீர்கொழும்பு',
             phones=HOTLINE)

        save('gampaha_depot',
             name_en='SLTB Gampaha Depot',
             name_si='ගම්පහ ශ්‍රී ලංගම ගබඩාව',
             name_ta='கம்பஹா இ.போ.ச கொட்டகை',
             district='Gampaha', lat=7.0838, lng=80.0231,
             addr_en='Gampaha Town, Gampaha',
             addr_si='ගම්පහ නගරය',
             addr_ta='கம்பஹா நகர்',
             phones=HOTLINE)

        save('kalutara_depot',
             name_en='SLTB Kalutara Bus Station',
             name_si='කළුතර ශ්‍රී ලංගම බස් නිළය',
             name_ta='களுத்துறை இ.போ.ச பேருந்து நிலையம்',
             district='Kalutara', lat=6.5844, lng=79.9604,
             addr_en='Colombo Road, Kalutara',
             addr_si='කොළඹ පාර, කළුතර',
             addr_ta='கொழும்பு சாலை, களுத்துறை',
             phones=HOTLINE)

        save('kalutara_panadura_depot',
             name_en='SLTB Panadura Depot (PN)',
             name_si='පානදුර ශ්‍රී ලංගම ගබඩාව (PN)',
             name_ta='பாணதுறை இ.போ.ச கொட்டகை (PN)',
             district='Kalutara', lat=6.7145, lng=79.9081,
             addr_en='Panadura, Kalutara District',
             addr_si='පානදුර, කළුතර දිස්ත්‍රික්කය',
             addr_ta='பாணதுறை, களுத்துறை மாவட்டம்',
             phones=HOTLINE)

        # ══════════════════════════════════════════════════════════════════
        # CENTRAL PROVINCE
        # ══════════════════════════════════════════════════════════════════

        save('kandy_south_depot',
             name_en='SLTB Kandy South Depot (KS)',
             name_si='මහනුවර දකුණු ශ්‍රී ලංගම ගබඩාව (KS)',
             name_ta='கண்டி தெற்கு இ.போ.ச கொட்டகை (KS)',
             district='Kandy', lat=7.2856, lng=80.6251,
             addr_en='Goods Shed Road, Kandy',
             addr_si='භාණ්ඩ කූඩු පාර, මහනුවර',
             addr_ta='சரக்கு கிடங்கு சாலை, கண்டி',
             phones=HOTLINE)

        save('kandy_bogambara_terminal',
             name_en='Kandy Intercity Bus Terminal (Bogambara)',
             name_si='මහනුවර අන්තර් නගර බස් නිළය (බොගම්බර)',
             name_ta='கண்டி நகரங்களுக்கிடையில் பேருந்து நிலையம்',
             district='Kandy', lat=7.2898, lng=80.6338,
             addr_en='Station Road, Bogambara, Kandy',
             addr_si='ස්ථාන පාර, බොගම්බර, මහනුවර',
             addr_ta='நிலைய சாலை, போகம்பர, கண்டி',
             phones=[ph('0703977830')])

        save('kandy_teldeniya_depot',
             name_en='SLTB Teldeniya Depot (TD)',
             name_si='තෙල්දෙනිය ශ්‍රී ලංගම ගබඩාව (TD)',
             name_ta='தெல்தெனிய இ.போ.ச கொட்டகை (TD)',
             district='Kandy', lat=7.3148, lng=80.7585,
             addr_en='Teldeniya, Kandy District',
             addr_si='තෙල්දෙනිය, මහනුවර දිස්ත්‍රික්කය',
             addr_ta='தெல்தெனிய, கண்டி மாவட்டம்',
             phones=HOTLINE)

        save('matale_depot',
             name_en='SLTB Matale Depot (ML)',
             name_si='මාතලේ ශ්‍රී ලංගම ගබඩාව (ML)',
             name_ta='மாத்தளை இ.போ.ச கொட்டகை (ML)',
             district='Matale', lat=7.4700, lng=80.6230,
             addr_en='Matale Town, Matale',
             addr_si='මාතලේ නගරය',
             addr_ta='மாத்தளை நகர்',
             phones=HOTLINE)

        save('nuwara_eliya_depot',
             name_en='SLTB Nuwara Eliya Depot (NE)',
             name_si='නුවර එළිය ශ්‍රී ලංගම ගබඩාව',
             name_ta='நுவரெலியா இ.போ.ச கொட்டகை',
             district='Nuwara Eliya', lat=6.9700, lng=80.7800,
             addr_en='Nuwara Eliya Town',
             addr_si='නුවර එළිය නගරය',
             addr_ta='நுவரெலியா நகர்',
             phones=HOTLINE)

        save('nuwara_eliya_hatton_depot',
             name_en='SLTB Hatton Depot',
             name_si='හැටන් ශ්‍රී ලංගම ගබඩාව',
             name_ta='ஹட்டன் இ.போ.ச கொட்டகை',
             district='Nuwara Eliya', lat=6.8887, lng=80.5992,
             addr_en='Hatton Town, Nuwara Eliya District',
             addr_si='හැටන් නගරය, නුවර එළිය දිස්ත්‍රික්කය',
             addr_ta='ஹட்டன் நகர், நுவரெலியா மாவட்டம்',
             phones=HOTLINE)

        # ══════════════════════════════════════════════════════════════════
        # SOUTHERN PROVINCE
        # ══════════════════════════════════════════════════════════════════

        save('galle_depot',
             name_en='SLTB Galle Central Bus Station (GL)',
             name_si='ගාල්ල ශ්‍රී ලංගම මධ්‍යම බස් නිළය (GL)',
             name_ta='காலி இ.போ.ச மத்திய பேருந்து நிலையம் (GL)',
             district='Galle', lat=6.0359, lng=80.2170,
             addr_en='Colombo Road, Galle 80000',
             addr_si='කොළඹ පාර, ගාල්ල 80000',
             addr_ta='கொழும்பு சாலை, காலி 80000',
             phones=HOTLINE)

        save('matara_depot',
             name_en='SLTB Matara Bus Stand (MT)',
             name_si='මාතර ශ්‍රී ලංගම බස් නිළය (MT)',
             name_ta='மாத்தறை இ.போ.ச பேருந்து நிலையம் (MT)',
             district='Matara', lat=5.9500, lng=80.5330,
             addr_en='Matara Town, Southern Province',
             addr_si='මාතර නගරය, දකුණු පළාත',
             addr_ta='மாத்தறை நகர், தெற்கு மாகாணம்',
             phones=HOTLINE)

        save('hambantota_depot',
             name_en='SLTB Hambantota Bus Stand',
             name_si='හම්බන්තොට ශ්‍රී ලංගම බස් නිළය',
             name_ta='அம்பாந்தோட்டை இ.போ.ச பேருந்து நிலையம்',
             district='Hambantota', lat=6.1255, lng=81.1258,
             addr_en='Hambantota Town, Southern Province',
             addr_si='හම්බන්තොට නගරය, දකුණු පළාත',
             addr_ta='அம்பாந்தோட்டை நகர், தெற்கு மாகாணம்',
             phones=HOTLINE)

        # ══════════════════════════════════════════════════════════════════
        # NORTH WESTERN PROVINCE
        # ══════════════════════════════════════════════════════════════════

        save('kurunegala_south_depot',
             name_en='SLTB Kurunegala South Depot (KGS)',
             name_si='කුරුණෑගල දකුණු ශ්‍රී ලංගම ගබඩාව (KGS)',
             name_ta='குருணாகல் தெற்கு இ.போ.ச கொட்டகை (KGS)',
             district='Kurunegala', lat=7.4793, lng=80.3708,
             addr_en='Kandy Road, Kurunegala',
             addr_si='මහනුවර පාර, කුරුණෑගල',
             addr_ta='கண்டி சாலை, குருணாகல்',
             phones=HOTLINE)

        save('kurunegala_north_depot',
             name_en='SLTB Kurunegala North Depot (KGN)',
             name_si='කුරුණෑගල උතුරු ශ්‍රී ලංගම ගබඩාව (KGN)',
             name_ta='குருணாகல் வடக்கு இ.போ.ச கொட்டகை (KGN)',
             district='Kurunegala', lat=7.5008, lng=80.3953,
             addr_en='A6 Highway (Ambepussa–Trincomalee Rd), Kurunegala',
             addr_si='A6 ජාතික මාර්ගය, කුරුණෑගල',
             addr_ta='A6 நெடுஞ்சாலை, குருணாகல்',
             phones=[ph('0372222320')])

        save('puttalam_depot',
             name_en='SLTB Puttalam Bus Station (PT)',
             name_si='පුත්තලම ශ්‍රී ලංගම බස් නිළය (PT)',
             name_ta='புத்தளம் இ.போ.ச பேருந்து நிலையம் (PT)',
             district='Puttalam', lat=8.0279, lng=79.8334,
             addr_en='Puttalam Town, North Western Province',
             addr_si='පුත්තලම නගරය',
             addr_ta='புத்தளம் நகர்',
             phones=HOTLINE)

        # ══════════════════════════════════════════════════════════════════
        # NORTH CENTRAL PROVINCE
        # ══════════════════════════════════════════════════════════════════

        save('anuradhapura_depot',
             name_en='SLTB Anuradhapura New Bus Stand (AP)',
             name_si='අනුරාධාපුරය නව ශ්‍රී ලංගම බස් නිළය (AP)',
             name_ta='அனுராதபுரம் புதிய இ.போ.ச பேருந்து நிலையம் (AP)',
             district='Anuradhapura', lat=8.3407, lng=80.4147,
             addr_en='Maithripala Senanayake Mawatha, Anuradhapura',
             addr_si='මෛත්‍රිපාල සේනානායක මාවත, අනුරාධාපුරය',
             addr_ta='மைத்திரிபால சேனாநாயக்க மாவத்தை, அனுராதபுரம்',
             phones=[ph('0252222325'), ph('0252222564', 'Inquiries 2', 'විමසීම් 2', 'விசாரணை 2')])

        save('polonnaruwa_depot',
             name_en='SLTB Polonnaruwa Depot (PL)',
             name_si='පොළොන්නරුව ශ්‍රී ලංගම ගබඩාව (PL)',
             name_ta='பொலன்னறுவை இ.போ.ச கொட்டகை (PL)',
             district='Polonnaruwa', lat=7.9297, lng=81.0329,
             addr_en='Kaduruwela, Polonnaruwa',
             addr_si='කදුරුවෙල, පොළොන්නරුව',
             addr_ta='கடுருவேல, பொலன்னறுவை',
             phones=HOTLINE)

        # ══════════════════════════════════════════════════════════════════
        # EASTERN PROVINCE
        # ══════════════════════════════════════════════════════════════════

        save('trincomalee_depot',
             name_en='SLTB Trincomalee Depot (TM)',
             name_si='තිරිකුණාමලය ශ්‍රී ලංගම ගබඩාව (TM)',
             name_ta='திருகோணமலை இ.போ.ச கொட்டகை (TM)',
             district='Trincomalee', lat=8.5945, lng=81.2183,
             addr_en='Uppuveli Road, Trincomalee',
             addr_si='උප්පුවේලි පාර, තිරිකුණාමලය',
             addr_ta='உப்புவேலி சாலை, திருகோணமலை',
             phones=HOTLINE)

        save('batticaloa_depot',
             name_en='SLTB Batticaloa Depot (BT)',
             name_si='මඩකලපුව ශ්‍රී ලංගම ගබඩාව (BT)',
             name_ta='மட்டக்களப்பு இ.போ.ச கொட்டகை (BT)',
             district='Batticaloa', lat=7.7146, lng=81.6947,
             addr_en='Munai Street, Batticaloa',
             addr_si='මූනේ වීදිය, මඩකලපුව',
             addr_ta='முனை தெரு, மட்டக்களப்பு',
             phones=HOTLINE)

        save('ampara_depot',
             name_en='SLTB Ampara Bus Station (AM)',
             name_si='අම්පාර ශ්‍රී ලංගම බස් නිළය (AM)',
             name_ta='அம்பாறை இ.போ.ச பேருந்து நிலையம் (AM)',
             district='Ampara', lat=7.2904, lng=81.6731,
             addr_en='Ampara Town, Eastern Province',
             addr_si='අම්පාර නගරය, නැගෙනහිර පළාත',
             addr_ta='அம்பாறை நகர், கிழக்கு மாகாணம்',
             phones=HOTLINE)

        # ══════════════════════════════════════════════════════════════════
        # UVA PROVINCE
        # ══════════════════════════════════════════════════════════════════

        save('badulla_depot',
             name_en='SLTB Badulla Depot (BD)',
             name_si='බදුල්ල ශ්‍රී ලංගම ගබඩාව (BD)',
             name_ta='பதுளை இ.போ.ச கொட்டகை (BD)',
             district='Badulla', lat=6.9872, lng=81.0575,
             addr_en='372/5 Mahiyangana Road, Badulla',
             addr_si='Mahiyangana පාර 372/5, බදුල්ල',
             addr_ta='372/5 மஹியங்கன சாலை, பதுளை',
             phones=HOTLINE)

        save('monaragala_depot',
             name_en='SLTB Monaragala Bus Stand (MON)',
             name_si='මොනරාගල ශ්‍රී ලංගම බස් නිළය',
             name_ta='மொணராகல இ.போ.ச பேருந்து நிலையம்',
             district='Monaragala', lat=6.8718, lng=81.3519,
             addr_en='Monaragala Town, Uva Province',
             addr_si='මොනරාගල නගරය, ඌව පළාත',
             addr_ta='மொணராகல நகர், ஊவா மாகாணம்',
             phones=HOTLINE)

        # ══════════════════════════════════════════════════════════════════
        # SABARAGAMUWA PROVINCE
        # ══════════════════════════════════════════════════════════════════

        save('ratnapura_depot',
             name_en='SLTB Ratnapura Depot (RP)',
             name_si='රත්නපුර ශ්‍රී ලංගම ගබඩාව (RP)',
             name_ta='இரத்தினபுரி இ.போ.ச கொட்டகை (RP)',
             district='Ratnapura', lat=6.6849, lng=80.4105,
             addr_en='Ratnapura Town, Sabaragamuwa Province',
             addr_si='රත්නපුර නගරය, සබරගමු පළාත',
             addr_ta='இரத்தினபுரி நகர், சபரகமுவ மாகாணம்',
             phones=HOTLINE)

        save('kegalle_depot',
             name_en='SLTB Kegalle Depot (KL)',
             name_si='කේගල්ල ශ්‍රී ලංගම ගබඩාව (KL)',
             name_ta='கேகாலை இ.போ.ச கொட்டகை (KL)',
             district='Kegalle', lat=7.2517, lng=80.3439,
             addr_en='Kegalle Town, Sabaragamuwa Province',
             addr_si='කේගල්ල නගරය',
             addr_ta='கேகாலை நகர்',
             phones=HOTLINE)

        self.stdout.write(self.style.SUCCESS(
            f'Seeded depots: {created} created, {updated} updated '
            f'(total services in DB: {Service.objects.count()}).'))


# All codes managed by this command
DEPOT_CODES = {
    'jaffna_central_bus_stand', 'jaffna_kondavil_depot', 'jaffna_kopay_depot',
    'jaffna_kokkuvil_depot', 'jaffna_karainagar_depot', 'jaffna_chavakachcheri_depot',
    'jaffna_point_pedro_depot', 'jaffna_manipay_depot', 'jaffna_kayts_depot',
    'jaffna_tellippalai_depot',
    'kilinochchi_bus_stand', 'mannar_bus_stand', 'vavuniya_bus_stand',
    'mullaitivu_bus_stand',
    'colombo_pettah_cbs', 'colombo_bastian_mawatha', 'colombo_borella_depot',
    'colombo_thalangama_depot', 'colombo_angoda_depot',
    'gampaha_ja_ela_depot', 'gampaha_negombo_depot', 'gampaha_depot',
    'kalutara_depot', 'kalutara_panadura_depot',
    'kandy_south_depot', 'kandy_bogambara_terminal', 'kandy_teldeniya_depot',
    'matale_depot', 'nuwara_eliya_depot', 'nuwara_eliya_hatton_depot',
    'galle_depot', 'matara_depot', 'hambantota_depot',
    'kurunegala_south_depot', 'kurunegala_north_depot', 'puttalam_depot',
    'anuradhapura_depot', 'polonnaruwa_depot',
    'trincomalee_depot', 'batticaloa_depot', 'ampara_depot',
    'badulla_depot', 'monaragala_depot',
    'ratnapura_depot', 'kegalle_depot',
}
