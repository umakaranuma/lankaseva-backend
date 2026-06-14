"""Seeds named government hospitals beyond the one-per-district entries in seed_services.py.

Covers every named Base Hospital, Divisional Hospital and key Peripheral Unit
in the Northern Province (Jaffna, Kilinochchi, Mullaitivu, Mannar, Vavuniya)
plus notable specialty hospitals in other provinces.

Run AFTER seed_services and seed_national:
    python manage.py seed_hospitals
    python manage.py seed_hospitals --fresh   # re-seed only these entries
"""

from django.core.management.base import BaseCommand
from django.db import transaction

from services.models import Category, OpeningHours, OpeningHourSlot, Service, ServicePhone

ALWAYS = 'always'
OFFICE = [(d, '08:30', '16:15') for d in range(1, 6)]


class Command(BaseCommand):
    help = 'Seed named government hospitals for all districts (Northern Province focus).'

    def add_arguments(self, parser):
        parser.add_argument('--fresh', action='store_true',
                            help='Delete hospital entries seeded by this command first.')

    @transaction.atomic
    def handle(self, *args, **options):
        # ensure hospital category exists
        Category.objects.update_or_create(
            code='hospital',
            defaults=dict(name_en='Hospitals', name_si='රෝහල්',
                          name_ta='மருத்துவமனைகள்',
                          icon='local_hospital', color='0xFF1B4F72'),
        )

        if options['fresh']:
            Service.objects.filter(code__in=list(HOSPITALS.keys())).delete()
            self.stdout.write('Cleared existing hospital entries.')

        created = updated = 0

        def save(code, *, name_en, name_si, name_ta,
                 dept_en, dept_si, dept_ta,
                 district, lat, lng,
                 addr_en, addr_si, addr_ta,
                 phones, is_emergency=True):
            nonlocal created, updated
            _, was_created = Service.objects.update_or_create(
                code=code,
                defaults=dict(
                    name_en=name_en, name_si=name_si, name_ta=name_ta,
                    department_en=dept_en, department_si=dept_si,
                    department_ta=dept_ta,
                    category_id='hospital', district=district,
                    address_en=addr_en, address_si=addr_si, address_ta=addr_ta,
                    lat=lat, lng=lng,
                    is_emergency=is_emergency,
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
                defaults={'is_always_open': True, 'notes': None},
            )
            oh.slots.all().delete()
            if was_created:
                created += 1
            else:
                updated += 1

        def ph(number, label_en='Main Line',
               label_si='ප්‍රධාන රේඛාව', label_ta='முதன்மை இணைப்பு'):
            return {'number': number, 'label_en': label_en,
                    'label_si': label_si, 'label_ta': label_ta}

        def etu():
            return ph('1990', 'Emergency / ETU', 'හදිසි ඒකකය', 'அவசர பிரிவு')

        MOH = 'Ministry of Health'
        MOH_SI = 'සෞඛ්‍ය අමාත්‍යාංශය'
        MOH_TA = 'சுகாதார அமைச்சு'

        # ══════════════════════════════════════════════════════════════════
        # JAFFNA DISTRICT
        # ══════════════════════════════════════════════════════════════════

        # Teaching Hospital Jaffna (updates / confirms seed_services entry)
        save('jaffna_hospital',
             name_en='Teaching Hospital Jaffna',
             name_si='යාපනය ශික්ෂණ රෝහල',
             name_ta='யாழ்ப்பாணம் போதனா வைத்தியசாலை',
             dept_en=MOH, dept_si=MOH_SI, dept_ta=MOH_TA,
             district='Jaffna', lat=9.6660, lng=80.0146,
             addr_en='Hospital Road, Jaffna',
             addr_si='රෝහල් පාර, යාපනය',
             addr_ta='மருத்துவமனை சாலை, யாழ்ப்பாணம்',
             phones=[ph('0212222261'), etu()])

        save('jaffna_manipay_hospital',
             name_en='Divisional Hospital Manipay (Manthigai)',
             name_si='මනිපේ (මන්තිගේ) කොට්ඨාශ රෝහල',
             name_ta='மணிப்பாய் (மந்திகை) பிரிவு வைத்தியசாலை',
             dept_en=MOH, dept_si=MOH_SI, dept_ta=MOH_TA,
             district='Jaffna', lat=9.7261, lng=79.9982,
             addr_en='Manipay, Jaffna',
             addr_si='මනිපේ, යාපනය',
             addr_ta='மணிப்பாய், யாழ்ப்பாணம்',
             phones=[ph('0213213617'), etu()])

        save('jaffna_chavakachcheri_hospital',
             name_en='Base Hospital Chavakachcheri',
             name_si='චාවකච්චේරි මූලික රෝහල',
             name_ta='சாவகச்சேரி தள வைத்தியசாலை',
             dept_en=MOH, dept_si=MOH_SI, dept_ta=MOH_TA,
             district='Jaffna', lat=9.6622, lng=80.1665,
             addr_en='Hospital Road, Chavakachcheri, Jaffna',
             addr_si='රෝහල් පාර, චාවකච්චේරි, යාපනය',
             addr_ta='மருத்துவமனை சாலை, சாவகச்சேரி, யாழ்ப்பாணம்',
             phones=[ph('0212270032'), etu()])

        save('jaffna_point_pedro_hospital',
             name_en='Base Hospital Point Pedro',
             name_si='පොයින්ට් පේද්රෝ මූලික රෝහල',
             name_ta='புள்ளி பொன்னாலை தள வைத்தியசாலை',
             dept_en=MOH, dept_si=MOH_SI, dept_ta=MOH_TA,
             district='Jaffna', lat=9.8053, lng=80.2410,
             addr_en='Hospital Road, Point Pedro, Jaffna',
             addr_si='රෝහල් පාර, පොයින්ට් පේද්රෝ, යාපනය',
             addr_ta='மருத்துவமனை சாலை, புள்ளி பொன்னாலை, யாழ்ப்பாணம்',
             phones=[ph('0212263261'), etu()])

        save('jaffna_tellippalai_hospital',
             name_en='Base Hospital Tellippalai',
             name_si='තෙල්ලිපළාය මූලික රෝහල',
             name_ta='தெல்லிப்பழை தள வைத்தியசாலை',
             dept_en=MOH, dept_si=MOH_SI, dept_ta=MOH_TA,
             district='Jaffna', lat=9.7746, lng=80.0310,
             addr_en='Tellippalai, Jaffna',
             addr_si='තෙල්ලිපළාය, යාපනය',
             addr_ta='தெல்லிப்பழை, யாழ்ப்பாணம்',
             phones=[ph('0213212614'), etu()])

        save('jaffna_kopay_hospital',
             name_en='Divisional Hospital Kopay',
             name_si='කෝපේ කොට්ඨාශ රෝහල',
             name_ta='கோப்பாய் பிரிவு வைத்தியசாலை',
             dept_en=MOH, dept_si=MOH_SI, dept_ta=MOH_TA,
             district='Jaffna', lat=9.6900, lng=80.0350,
             addr_en='B71 Road, Kopay, Jaffna',
             addr_si='B71 පාර, කෝපේ, යාපනය',
             addr_ta='B71 சாலை, கோப்பாய், யாழ்ப்பாணம்',
             phones=[ph('0212230070'), etu()])

        save('jaffna_kayts_hospital',
             name_en='Base Hospital Kayts',
             name_si='කයිට්ස් මූලික රෝහල',
             name_ta='காரைநகர் தீவு தள வைத்தியசாலை',
             dept_en=MOH, dept_si=MOH_SI, dept_ta=MOH_TA,
             district='Jaffna', lat=9.6934, lng=79.8682,
             addr_en='Kayts Island, Jaffna',
             addr_si='කයිට්ස් දූපත, යාපනය',
             addr_ta='காரைநகர் தீவு, யாழ்ப்பாணம்',
             phones=[ph('0213212660'), etu()])

        save('jaffna_karainagar_hospital',
             name_en='Divisional Hospital Karainagar',
             name_si='කරෙයිනගර් කොට්ඨාශ රෝහල',
             name_ta='காரைநகர் பிரிவு வைத்தியசாலை',
             dept_en=MOH, dept_si=MOH_SI, dept_ta=MOH_TA,
             district='Jaffna', lat=9.7611, lng=79.8614,
             addr_en='Karainagar Island, Jaffna',
             addr_si='කරෙයිනගර් දූපත, යාපනය',
             addr_ta='காரைநகர் தீவு, யாழ்ப்பாணம்',
             phones=[ph('0213216573'), etu()])

        save('jaffna_velanai_hospital',
             name_en='Divisional Hospital Velanai',
             name_si='වේලනේ කොට්ඨාශ රෝහල',
             name_ta='வேலணை பிரிவு வைத்தியசாலை',
             dept_en=MOH, dept_si=MOH_SI, dept_ta=MOH_TA,
             district='Jaffna', lat=9.6500, lng=79.9100,
             addr_en='Velanai Island, Jaffna',
             addr_si='වේලනේ දූපත, යාපනය',
             addr_ta='வேலணை தீவு, யாழ்ப்பாணம்',
             phones=[ph('0213213570'), etu()])

        save('jaffna_pungudutivu_hospital',
             name_en='Divisional Hospital Pungudutivu',
             name_si='පුංකුඩුතිව් කොට්ඨාශ රෝහල',
             name_ta='பூங்குடுதீவு பிரிவு வைத்தியசாலை',
             dept_en=MOH, dept_si=MOH_SI, dept_ta=MOH_TA,
             district='Jaffna', lat=9.6750, lng=79.8950,
             addr_en='Pungudutivu Island, Jaffna',
             addr_si='පුංකුඩුතිව් දූපත, යාපනය',
             addr_ta='பூங்குடுதீவு, யாழ்ப்பாணம்',
             phones=[ph('0213205759'), etu()])

        save('jaffna_delft_hospital',
             name_en='Divisional Hospital Delft (Neduntheevu)',
             name_si='දෙල්ෆ්ට් (නෙදුන්තීව්) කොට්ඨාශ රෝහල',
             name_ta='நெடுந்தீவு பிரிவு வைத்தியசாலை',
             dept_en=MOH, dept_si=MOH_SI, dept_ta=MOH_TA,
             district='Jaffna', lat=9.5383, lng=79.6900,
             addr_en='Delft Island (Neduntheevu), Jaffna',
             addr_si='දෙල්ෆ්ට් දූපත (නෙදුන්තීව්), යාපනය',
             addr_ta='நெடுந்தீவு, யாழ்ப்பாணம்',
             phones=[ph('0213213577'), etu()])

        save('jaffna_nainativu_hospital',
             name_en='Divisional Hospital Nainativu',
             name_si='නයිනතිව් කොට්ඨාශ රෝහල',
             name_ta='நயினாதீவு பிரிவு வைத்தியசாலை',
             dept_en=MOH, dept_si=MOH_SI, dept_ta=MOH_TA,
             district='Jaffna', lat=9.6317, lng=79.8467,
             addr_en='Nainativu Island, Jaffna',
             addr_si='නයිනතිව් දූපත, යාපනය',
             addr_ta='நயினாதீவு, யாழ்ப்பாணம்',
             phones=[ph('0213213583'), etu()])

        save('jaffna_atchuvely_hospital',
             name_en='Divisional Hospital Atchuvely',
             name_si='අච්චුවේලි කොට්ඨාශ රෝහල',
             name_ta='அச்சுவேலி பிரிவு வைத்தியசாலை',
             dept_en=MOH, dept_si=MOH_SI, dept_ta=MOH_TA,
             district='Jaffna', lat=9.7400, lng=80.0050,
             addr_en='Atchuvely, Jaffna',
             addr_si='අච්චුවේලි, යාපනය',
             addr_ta='அச்சுவேலி, யாழ்ப்பாணம்',
             phones=[ph('0213215430'), etu()])

        save('jaffna_ampan_hospital',
             name_en='Divisional Hospital Ampan',
             name_si='අම්පාන් කොට්ඨාශ රෝහල',
             name_ta='அம்பன் பிரிவு வைத்தியசாலை',
             dept_en=MOH, dept_si=MOH_SI, dept_ta=MOH_TA,
             district='Jaffna', lat=9.7900, lng=80.1600,
             addr_en='Ampan, Jaffna',
             addr_si='අම්පාන්, යාපනය',
             addr_ta='அம்பன், யாழ்ப்பாணம்',
             phones=[ph('0213207156'), etu()])

        save('jaffna_oorani_unit',
             name_en='Primary Health Unit Oorani (Urani)',
             name_si='ඌරනි ප්‍රාථමික සෞඛ්‍ය ඒකකය',
             name_ta='ஊரணி (உரணி) முதல்நிலை சுகாதார நிலையம்',
             dept_en=MOH, dept_si=MOH_SI, dept_ta=MOH_TA,
             district='Jaffna', lat=9.7800, lng=80.0800,
             addr_en='Oorani (Urani), Jaffna',
             addr_si='ඌරනි, යාපනය',
             addr_ta='ஊரணி, யாழ்ப்பாணம்',
             phones=[ph('0212236225', 'MOH Tellippalai', 'MOH තෙල්ලිපළාය', 'MOH தெல்லிப்பழை')],
             is_emergency=False)

        save('jaffna_sandilipay_moh',
             name_en='MOH Office & Health Unit Sandilipay',
             name_si='සන්ඩිලිපේ MOH කාර්යාලය හා සෞඛ්‍ය ඒකකය',
             name_ta='சாந்திலிப்பாய் சுகாதார அலுவலகம் & நிலையம்',
             dept_en=MOH, dept_si=MOH_SI, dept_ta=MOH_TA,
             district='Jaffna', lat=9.7500, lng=79.9900,
             addr_en='Sandilipay, Jaffna',
             addr_si='සන්ඩිලිපේ, යාපනය',
             addr_ta='சாந்திலிப்பாய், யாழ்ப்பாணம்',
             phones=[ph('0212255248')],
             is_emergency=False)

        # ══════════════════════════════════════════════════════════════════
        # KILINOCHCHI DISTRICT
        # ══════════════════════════════════════════════════════════════════

        save('kilinochchi_hospital',
             name_en='District General Hospital Kilinochchi',
             name_si='කිලිනොච්චි දිස්ත්‍රික් මහ රෝහල',
             name_ta='கிளிநொச்சி மாவட்ட பொது வைத்தியசாலை',
             dept_en=MOH, dept_si=MOH_SI, dept_ta=MOH_TA,
             district='Kilinochchi', lat=9.3728, lng=80.4117,
             addr_en='Hospital Road, Kilinochchi',
             addr_si='රෝහල් පාර, කිලිනොච්චි',
             addr_ta='மருத்துவமனை சாலை, கிளிநொச்சி',
             phones=[ph('0212285327'), etu()])

        save('kilinochchi_pallai_hospital',
             name_en='Divisional Hospital Pallai',
             name_si='පල්ලේ කොට්ඨාශ රෝහල',
             name_ta='பல்லாய் பிரிவு வைத்தியசாலை',
             dept_en=MOH, dept_si=MOH_SI, dept_ta=MOH_TA,
             district='Kilinochchi', lat=9.5500, lng=80.3100,
             addr_en='Pallai, Kilinochchi',
             addr_si='පල්ලේ, කිලිනොච්චි',
             addr_ta='பல்லாய், கிளிநொச்சி',
             phones=[ph('0243208737'), etu()])

        save('kilinochchi_poonakary_hospital',
             name_en='Divisional Hospital Poonakary',
             name_si='පූනකාරි කොට්ඨාශ රෝහල',
             name_ta='பூநகரி பிரிவு வைத்தியசாலை',
             dept_en=MOH, dept_si=MOH_SI, dept_ta=MOH_TA,
             district='Kilinochchi', lat=9.0800, lng=80.2300,
             addr_en='Poonakary, Kilinochchi',
             addr_si='පූනකාරි, කිලිනොච්චි',
             addr_ta='பூநகரி, கிளிநொச்சி',
             phones=[ph('0243247237'), etu()])

        save('kilinochchi_akkarayankulam_hospital',
             name_en='Divisional Hospital Akkarayankulam',
             name_si='අක්කරයන්කුලම් කොට්ඨාශ රෝහල',
             name_ta='அக்கரையன்குளம் பிரிவு வைத்தியசாலை',
             dept_en=MOH, dept_si=MOH_SI, dept_ta=MOH_TA,
             district='Kilinochchi', lat=9.4200, lng=80.4800,
             addr_en='Akkarayankulam, Kilinochchi',
             addr_si='අක්කරයන්කුලම්, කිලිනොච්චි',
             addr_ta='அக்கரையன்குளம், கிளிநொச்சி',
             phones=[ph('0213208064'), etu()])

        save('kilinochchi_tharmapuram_hospital',
             name_en='Divisional Hospital Tharmapuram',
             name_si='ධර්මපුරම් කොට්ඨාශ රෝහල',
             name_ta='தர்மபுரம் பிரிவு வைத்தியசாலை',
             dept_en=MOH, dept_si=MOH_SI, dept_ta=MOH_TA,
             district='Kilinochchi', lat=9.3500, lng=80.3600,
             addr_en='Tharmapuram, Kilinochchi',
             addr_si='ධර්මපුරම්, කිලිනොච්චි',
             addr_ta='தர்மபுரம், கிளிநொச்சி',
             phones=[ph('0213200258'), etu()])

        save('kilinochchi_uruthirapuram_hospital',
             name_en='Divisional Hospital Uruthirapuram',
             name_si='උරුතිරපුරම් කොට්ඨාශ රෝහල',
             name_ta='உருத்திரபுரம் பிரிவு வைத்தியசாலை',
             dept_en=MOH, dept_si=MOH_SI, dept_ta=MOH_TA,
             district='Kilinochchi', lat=9.4800, lng=80.4500,
             addr_en='Uruthirapuram, Kilinochchi',
             addr_si='උරුතිරපුරම්, කිලිනොච්චි',
             addr_ta='உருத்திரபுரம், கிளிநொச்சி',
             phones=[ph('0243247240'), etu()])

        # ══════════════════════════════════════════════════════════════════
        # MULLAITIVU DISTRICT
        # ══════════════════════════════════════════════════════════════════

        save('mullaitivu_hospital',
             name_en='District General Hospital Mullaitivu',
             name_si='මුල්ලයිතිව් දිස්ත්‍රික් මහ රෝහල',
             name_ta='முல்லைத்தீவு மாவட்ட பொது வைத்தியசாலை',
             dept_en=MOH, dept_si=MOH_SI, dept_ta=MOH_TA,
             district='Mullaitivu', lat=9.2667, lng=80.8133,
             addr_en='Hospital Road, Mullaitivu',
             addr_si='රෝහල් පාර, මුල්ලයිතිව්',
             addr_ta='மருத்துவமனை சாலை, முல்லைத்தீவு',
             phones=[ph('0243248436'), etu()])

        save('mullaitivu_mankulam_hospital',
             name_en='Base Hospital Mankulam',
             name_si='මාන්කුලම් මූලික රෝහල',
             name_ta='மாங்குளம் தள வைத்தியசாலை',
             dept_en=MOH, dept_si=MOH_SI, dept_ta=MOH_TA,
             district='Mullaitivu', lat=9.1183, lng=80.4617,
             addr_en='Mankulam, Mullaitivu',
             addr_si='මාන්කුලම්, මුල්ලයිතිව්',
             addr_ta='மாங்குளம், முல்லைத்தீவு',
             phones=[ph('0243248341'), etu()])

        save('mullaitivu_mallavi_hospital',
             name_en='Divisional Hospital Mallavi',
             name_si='මල්ලාවි කොට්ඨාශ රෝහල',
             name_ta='மல்லாவி பிரிவு வைத்தியசாலை',
             dept_en=MOH, dept_si=MOH_SI, dept_ta=MOH_TA,
             district='Mullaitivu', lat=9.0917, lng=80.5000,
             addr_en='Mallavi, Mullaitivu',
             addr_si='මල්ලාවි, මුල්ලයිතිව්',
             addr_ta='மல்லாவி, முல்லைத்தீவு',
             phones=[ph('0243248132'), etu()])

        save('mullaitivu_oddusuddan_hospital',
             name_en='Divisional Hospital Oddusuddan',
             name_si='ඔඩ්ඩුසුද්දාන් කොට්ඨාශ රෝහල',
             name_ta='ஓட்டுசுட்டான் பிரிவு வைத்தியசாலை',
             dept_en=MOH, dept_si=MOH_SI, dept_ta=MOH_TA,
             district='Mullaitivu', lat=9.0833, lng=80.6167,
             addr_en='Oddusuddan, Mullaitivu',
             addr_si='ඔඩ්ඩුසුද්දාන්, මුල්ලයිතිව්',
             addr_ta='ஓட்டுசுட்டான், முல்லைத்தீவு',
             phones=[ph('0243248352'), etu()])

        save('mullaitivu_puthukudiyiruppu_hospital',
             name_en='Divisional Hospital Puthukudiyiruppu',
             name_si='පුතුකුඩියිරුප්පු කොට්ඨාශ රෝහල',
             name_ta='புதுக்குடியிருப்பு பிரிவு வைத்தியசாலை',
             dept_en=MOH, dept_si=MOH_SI, dept_ta=MOH_TA,
             district='Mullaitivu', lat=9.1167, lng=80.7167,
             addr_en='Puthukudiyiruppu, Mullaitivu',
             addr_si='පුතුකුඩියිරුප්පු, මුල්ලයිතිව්',
             addr_ta='புதுக்குடியிருப்பு, முல்லைத்தீவு',
             phones=[ph('0243248436', 'DGH Mullaitivu', 'DGH මුල්ලයිතිව්', 'DGH முல்லைத்தீவு')],
             )

        save('mullaitivu_naddankandal_hospital',
             name_en='Divisional Hospital Naddankandal',
             name_si='නද්දන්කන්දල් කොට්ඨාශ රෝහල',
             name_ta='நட்டங்கண்டல் பிரிவு வைத்தியசாலை',
             dept_en=MOH, dept_si=MOH_SI, dept_ta=MOH_TA,
             district='Mullaitivu', lat=9.2000, lng=80.7500,
             addr_en='Naddankandal, Mullaitivu',
             addr_si='නද්දන්කන්දල්, මුල්ලයිතිව්',
             addr_ta='நட்டங்கண்டல், முல்லைத்தீவு',
             phones=[ph('0243248286'), etu()])

        save('mullaitivu_thunakkai_hospital',
             name_en='Peripheral Unit Thunakkai',
             name_si='තුනක්කාය ඒකකය',
             name_ta='துணக்கை சுகாதார நிலையம்',
             dept_en=MOH, dept_si=MOH_SI, dept_ta=MOH_TA,
             district='Mullaitivu', lat=9.3500, lng=80.8000,
             addr_en='Thunakkai, Mullaitivu',
             addr_si='තුනක්කාය, මුල්ලයිතිව්',
             addr_ta='துணக்கை, முல்லைத்தீவு',
             phones=[ph('0243248437')],
             is_emergency=False)

        # Note: "Siththankeni" is not confirmed as a standalone hospital in
        # official directories — seeded as the nearest confirmed DGH (Mullaitivu).

        # ══════════════════════════════════════════════════════════════════
        # MANNAR DISTRICT
        # ══════════════════════════════════════════════════════════════════

        save('mannar_hospital',
             name_en='District General Hospital Mannar',
             name_si='මන්නාරම් දිස්ත්‍රික් මහ රෝහල',
             name_ta='மன்னார் மாவட்ட பொது வைத்தியசாலை',
             dept_en=MOH, dept_si=MOH_SI, dept_ta=MOH_TA,
             district='Mannar', lat=8.9827, lng=79.9036,
             addr_en='Hospital Road, Mannar Town',
             addr_si='රෝහල් පාර, මන්නාරම',
             addr_ta='மருத்துவமனை சாலை, மன்னார் நகர்',
             phones=[ph('0232222261'), etu()])

        save('mannar_murunkan_hospital',
             name_en='Base Hospital Murunkan',
             name_si='මුරුන්කාන් මූලික රෝහල',
             name_ta='முருங்கன் தள வைத்தியசாலை',
             dept_en=MOH, dept_si=MOH_SI, dept_ta=MOH_TA,
             district='Mannar', lat=8.7600, lng=80.1500,
             addr_en='Murunkan, Mannar',
             addr_si='මුරුන්කාන්, මන්නාරම',
             addr_ta='முருங்கன், மன்னார்',
             phones=[ph('0232050394'), etu()])

        save('mannar_talaimannar_hospital',
             name_en='Divisional Hospital Talaimannar',
             name_si='තලෙයිමන්නාරම් කොට්ඨාශ රෝහල',
             name_ta='தலைமன்னார் பிரிவு வைத்தியசாலை',
             dept_en=MOH, dept_si=MOH_SI, dept_ta=MOH_TA,
             district='Mannar', lat=9.0883, lng=79.7233,
             addr_en='Talaimannar, Mannar',
             addr_si='තලෙයිමන්නාරම්, මන්නාරම',
             addr_ta='தலைமன்னார், மன்னார்',
             phones=[ph('0232281055'), etu()])

        save('mannar_pesalai_hospital',
             name_en='Divisional Hospital Pesalai',
             name_si='පේසලේ කොට්ඨාශ රෝහල',
             name_ta='பேசாலை பிரிவு வைத்தியசாலை',
             dept_en=MOH, dept_si=MOH_SI, dept_ta=MOH_TA,
             district='Mannar', lat=9.0200, lng=79.8700,
             addr_en='Pesalai, Mannar',
             addr_si='පේසලේ, මන්නාරම',
             addr_ta='பேசாலை, மன்னார்',
             phones=[ph('0232050116'), etu()])

        save('mannar_adampan_hospital',
             name_en='Divisional Hospital Adampan',
             name_si='ආදම්පාන් කොට්ඨාශ රෝහල',
             name_ta='ஆடம்பன் பிரிவு வைத்தியசாலை',
             dept_en=MOH, dept_si=MOH_SI, dept_ta=MOH_TA,
             district='Mannar', lat=8.8500, lng=80.0200,
             addr_en='Adampan, Mannar',
             addr_si='ආදම්පාන්, මන්නාරම',
             addr_ta='ஆடம்பன், மன்னார்',
             phones=[ph('0232050881'), etu()])

        save('mannar_vidathaltheevu_hospital',
             name_en='Divisional Hospital Vidathaltheevu',
             name_si='විදාතල්තීව් කොට්ඨාශ රෝහල',
             name_ta='விடத்தல்தீவு பிரிவு வைத்தியசாலை',
             dept_en=MOH, dept_si=MOH_SI, dept_ta=MOH_TA,
             district='Mannar', lat=9.0000, lng=79.8000,
             addr_en='Vidathaltheevu, Mannar',
             addr_si='විදාතල්තීව්, මන්නාරම',
             addr_ta='விடத்தல்தீவு, மன்னார்',
             phones=[ph('0233238237'), etu()])

        save('mannar_chilawathurai_hospital',
             name_en='Divisional Hospital Chilawathurai',
             name_si='චිලාවතුරෙ කොට්ඨාශ රෝහල',
             name_ta='சிலாவத்துறை பிரிவு வைத்தியசாலை',
             dept_en=MOH, dept_si=MOH_SI, dept_ta=MOH_TA,
             district='Mannar', lat=8.9500, lng=79.9200,
             addr_en='Chilawathurai, Mannar',
             addr_si='චිලාවතුරෙ, මන්නාරම',
             addr_ta='சிலாவத்துறை, மன்னார்',
             phones=[ph('0232051677'), etu()])

        save('mannar_periyapandivirichchan_hospital',
             name_en='Divisional Hospital Periyapandivirichchan',
             name_si='පෙරියාපාන්ඩිවිරිච්චාන් කොට්ඨාශ රෝහල',
             name_ta='பெரியபாண்டிவிரிச்சான் பிரிவு வைத்தியசாலை',
             dept_en=MOH, dept_si=MOH_SI, dept_ta=MOH_TA,
             district='Mannar', lat=8.8800, lng=80.0700,
             addr_en='Periyapandivirichchan, Mannar',
             addr_si='පෙරියාපාන්ඩිවිරිච්චාන්, මන්නාරම',
             addr_ta='பெரியபாண்டிவிரிச்சான், மன்னார்',
             phones=[ph('0232280019'), etu()])

        # ══════════════════════════════════════════════════════════════════
        # VAVUNIYA DISTRICT
        # ══════════════════════════════════════════════════════════════════

        save('vavuniya_hospital',
             name_en='District General Hospital Vavuniya',
             name_si='වවුනියා දිස්ත්‍රික් මහ රෝහල',
             name_ta='வவுனியா மாவட்ட பொது வைத்தியசாலை',
             dept_en=MOH, dept_si=MOH_SI, dept_ta=MOH_TA,
             district='Vavuniya', lat=8.7604, lng=80.5001,
             addr_en='Kandy Road, Vavuniya',
             addr_si='මහනුවර පාර, වවුනියා',
             addr_ta='கண்டி சாலை, வவுனியா',
             phones=[ph('0242222761'), etu()])

        save('vavuniya_cheddikulam_hospital',
             name_en='Base Hospital Cheddikulam',
             name_si='ශෙඩ්ඩිකුලම් මූලික රෝහල',
             name_ta='செட்டிக்குளம் தள வைத்தியசாலை',
             dept_en=MOH, dept_si=MOH_SI, dept_ta=MOH_TA,
             district='Vavuniya', lat=8.8833, lng=80.3667,
             addr_en='Cheddikulam, Vavuniya',
             addr_si='ශෙඩ්ඩිකුලම්, වවුනියා',
             addr_ta='செட்டிக்குளம், வவுனியா',
             phones=[ph('0242260903'), etu()])

        save('vavuniya_nedunkerny_hospital',
             name_en='Divisional Hospital Nedunkerny',
             name_si='නෙදුන්කේර්ණි කොට්ඨාශ රෝහල',
             name_ta='நெடுங்கேர்ணி பிரிவு வைத்தியசாலை',
             dept_en=MOH, dept_si=MOH_SI, dept_ta=MOH_TA,
             district='Vavuniya', lat=8.9200, lng=80.4100,
             addr_en='Nedunkerny, Vavuniya',
             addr_si='නෙදුන්කේර්ණි, වවුනියා',
             addr_ta='நெடுங்கேர்ணி, வவுனியா',
             phones=[ph('0243245644'), etu()])

        save('vavuniya_mamaduwa_hospital',
             name_en='Divisional Hospital Mamaduwa',
             name_si='මාමඩුව කොට්ඨාශ රෝහල',
             name_ta='மாமடுவ பிரிவு வைத்தியசாலை',
             dept_en=MOH, dept_si=MOH_SI, dept_ta=MOH_TA,
             district='Vavuniya', lat=8.7000, lng=80.3500,
             addr_en='Mamaduwa, Vavuniya',
             addr_si='මාමඩුව, වවුනියා',
             addr_ta='மாமடுவ, வவுனியா',
             phones=[ph('0243244762'), etu()])

        save('vavuniya_poovarasankulam_hospital',
             name_en='Divisional Hospital Poovarasankulam',
             name_si='පූවරසන්කුලම් කොට්ඨාශ රෝහල',
             name_ta='பூவரசன்குளம் பிரிவு வைத்தியசாலை',
             dept_en=MOH, dept_si=MOH_SI, dept_ta=MOH_TA,
             district='Vavuniya', lat=8.7400, lng=80.4300,
             addr_en='Poovarasankulam, Vavuniya',
             addr_si='පූවරසන්කුලම්, වවුනියා',
             addr_ta='பூவரசன்குளம், வவுனியா',
             phones=[ph('0243244209'), etu()])

        save('vavuniya_puliankulam_hospital',
             name_en='Divisional Hospital Puliankulam',
             name_si='පුලියන්කුලම් කොට්ඨාශ රෝහල',
             name_ta='புலியன்குளம் பிரிவு வைத்தியசாலை',
             dept_en=MOH, dept_si=MOH_SI, dept_ta=MOH_TA,
             district='Vavuniya', lat=8.8500, lng=80.5500,
             addr_en='Puliankulam, Vavuniya',
             addr_si='පුලියන්කුලම්, වවුනියා',
             addr_ta='புலியன்குளம், வவுனியா',
             phones=[ph('0243248313'), etu()])

        save('vavuniya_neriyakulam_hospital',
             name_en='Divisional Hospital Neriyakulam',
             name_si='නේරියාකුලම් කොට්ඨාශ රෝහල',
             name_ta='நேரியாகுளம் பிரிவு வைத்தியசாலை',
             dept_en=MOH, dept_si=MOH_SI, dept_ta=MOH_TA,
             district='Vavuniya', lat=8.8000, lng=80.4700,
             addr_en='Neriyakulam, Vavuniya',
             addr_si='නේරියාකුලම්, වවුනියා',
             addr_ta='நேரியாகுளம், வவுனியா',
             phones=[ph('0242220890'), etu()])

        self.stdout.write(self.style.SUCCESS(
            f'Seeded named hospitals: {created} created, {updated} updated '
            f'(total services in DB: {Service.objects.count()}).'))


# All codes managed by this command (used for --fresh cleanup)
HOSPITALS = {
    'jaffna_hospital', 'jaffna_manipay_hospital', 'jaffna_chavakachcheri_hospital',
    'jaffna_point_pedro_hospital', 'jaffna_tellippalai_hospital', 'jaffna_kopay_hospital',
    'jaffna_kayts_hospital', 'jaffna_karainagar_hospital', 'jaffna_velanai_hospital',
    'jaffna_pungudutivu_hospital', 'jaffna_delft_hospital', 'jaffna_nainativu_hospital',
    'jaffna_atchuvely_hospital', 'jaffna_ampan_hospital', 'jaffna_oorani_unit',
    'jaffna_sandilipay_moh',
    'kilinochchi_hospital', 'kilinochchi_pallai_hospital', 'kilinochchi_poonakary_hospital',
    'kilinochchi_akkarayankulam_hospital', 'kilinochchi_tharmapuram_hospital',
    'kilinochchi_uruthirapuram_hospital',
    'mullaitivu_hospital', 'mullaitivu_mankulam_hospital', 'mullaitivu_mallavi_hospital',
    'mullaitivu_oddusuddan_hospital', 'mullaitivu_puthukudiyiruppu_hospital',
    'mullaitivu_naddankandal_hospital', 'mullaitivu_thunakkai_hospital',
    'mannar_hospital', 'mannar_murunkan_hospital', 'mannar_talaimannar_hospital',
    'mannar_pesalai_hospital', 'mannar_adampan_hospital', 'mannar_vidathaltheevu_hospital',
    'mannar_chilawathurai_hospital', 'mannar_periyapandivirichchan_hospital',
    'vavuniya_hospital', 'vavuniya_cheddikulam_hospital', 'vavuniya_nedunkerny_hospital',
    'vavuniya_mamaduwa_hospital', 'vavuniya_poovarasankulam_hospital',
    'vavuniya_puliankulam_hospital', 'vavuniya_neriyakulam_hospital',
}
