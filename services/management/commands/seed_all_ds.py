"""
Seed all Divisional Secretariat offices across all 25 Sri Lanka districts.
Uses update_or_create — safe to run multiple times.
"""
from django.core.management.base import BaseCommand
from django.db import transaction
from services.models import Service, Category, ServicePhone, OpeningHours, OpeningHourSlot

HOURS = [(1, '08:30', '16:30'), (2, '08:30', '16:30'), (3, '08:30', '16:30'),
         (4, '08:30', '16:30'), (5, '08:30', '16:30')]

DEPT_EN = 'Divisional Secretariat'
DEPT_SI = 'කොට්ඨාශ ලේකම් කාර්යාලය'
DEPT_TA = 'பிரிவு செயலகம்'


def ensure_cat():
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


def add_hours(svc):
    oh = OpeningHours.objects.create(service=svc)
    for day, open_t, close_t in HOURS:
        OpeningHourSlot.objects.create(hours=oh, weekday=day, open_time=open_t, close_time=close_t)


def ds(code, name_en, name_si, name_ta, address_en, lat, lng, district, province, phone=None):
    return dict(code=code, name_en=name_en, name_si=name_si, name_ta=name_ta,
                address_en=address_en, lat=lat, lng=lng, district=district,
                province=province, phone=phone)


ALL_DS = [
    # ── WESTERN PROVINCE ──────────────────────────────────────────────────────
    # Colombo district
    ds('colombo_ds', 'Divisional Secretariat – Colombo', 'කොළඹ කොට්ඨාශ ලේකම් කාර්යාලය', 'கொழும்பு பிரிவு செயலகம்', 'Colombo 07, Western Province', 6.9147, 79.8737, 'Colombo', 'western', '0112691311'),
    ds('thimbirigasyaya_ds', 'Divisional Secretariat – Thimbirigasyaya', 'තිඹිරිගස්යාය කොට්ඨාශ ලේකම්', 'திம்பிரிகஸ்யாய பிரிவு செயலகம்', 'Thimbirigasyaya, Colombo', 6.8900, 79.8700, 'Colombo', 'western', '0112513060'),
    ds('kotte_ds', 'Divisional Secretariat – Sri Jayawardenepura Kotte', 'කෝට්ටේ කොට්ඨාශ ලේකම් කාර්යාලය', 'கோட்டே பிரிவு செயலகம்', 'Sri Jayawardenepura Kotte, Western Province', 6.8878, 79.8993, 'Colombo', 'western', '0112885290'),
    ds('maharagama_ds', 'Divisional Secretariat – Maharagama', 'මහරගම කොට්ඨාශ ලේකම් කාර්යාලය', 'மகரகம பிரிவு செயலகம்', 'Maharagama, Colombo District', 6.8475, 79.9258, 'Colombo', 'western', '0112851021'),
    ds('kolonnawa_ds', 'Divisional Secretariat – Kolonnawa', 'කොලොන්නාව කොට්ඨාශ ලේකම් කාර්යාලය', 'கொலொன்னாவ பிரிவு செயலகம்', 'Kolonnawa, Colombo District', 6.9200, 79.9300, 'Colombo', 'western', '0112534059'),
    ds('kaduwela_ds', 'Divisional Secretariat – Kaduwela', 'කඩුවෙල කොට්ඨාශ ලේකම් කාර්යාලය', 'கடுவெல பிரிவு செயலகம்', 'Kaduwela, Colombo District', 6.9300, 79.9700, 'Colombo', 'western', '0112539050'),
    ds('homagama_ds', 'Divisional Secretariat – Homagama', 'හෝමාගම කොට්ඨාශ ලේකම් කාර්යාලය', 'ஹோமாகம பிரிவு செயலகம்', 'Homagama, Colombo District', 6.8446, 80.0010, 'Colombo', 'western', '0112855071'),
    ds('seethawaka_ds', 'Divisional Secretariat – Seethawaka', 'සීතාවක කොට්ඨාශ ලේකම් කාර්යාලය', 'சீதாவக பிரிவு செயலகம்', 'Avissawella, Colombo District', 6.9549, 80.2127, 'Colombo', 'western', '0362222148'),
    ds('padukka_ds', 'Divisional Secretariat – Padukka', 'පාදුක්ක කොට්ඨාශ ලේකම් කාර්යාලය', 'படுக்க பிரிவு செயலகம்', 'Padukka, Colombo District', 6.8450, 80.1000, 'Colombo', 'western', '0112406163'),
    ds('moratuwa_ds', 'Divisional Secretariat – Moratuwa', 'මොරටුව කොට්ඨාශ ලේකම් කාර්යාලය', 'மொரட்டுவ பிரிவு செயலகம்', 'Moratuwa, Colombo District', 6.7731, 79.8826, 'Colombo', 'western', '0112648002'),
    ds('kesbewa_ds', 'Divisional Secretariat – Kesbewa', 'කේස්බෑව කොට්ඨාශ ලේකම් කාර්යාලය', 'கேஸ்பேவ பிரிவு செயலகம்', 'Kesbewa, Colombo District', 6.8200, 79.9500, 'Colombo', 'western', '0112615060'),
    ds('dehiwala_ds', 'Divisional Secretariat – Dehiwala-Mount Lavinia', 'දෙහිවල-ගල්කිස්ස කොට්ඨාශ ලේකම්', 'தெஹிவல-மவுன்ட் லவீனியா பிரிவு செயலகம்', 'Dehiwala, Colombo District', 6.8500, 79.8700, 'Colombo', 'western', '0112717062'),
    # Gampaha district
    ds('gampaha_ds', 'Divisional Secretariat – Gampaha', 'ගම්පහ කොට්ඨාශ ලේකම් කාර්යාලය', 'கம்பஹா பிரிவு செயலகம்', 'Gampaha, Western Province', 7.0873, 80.0091, 'Gampaha', 'western', '0332222291'),
    ds('negombo_ds', 'Divisional Secretariat – Negombo', 'මීගමුව කොට්ඨාශ ලේකම් කාර්යාලය', 'நீர்கொழும்பு பிரிவு செயலகம்', 'Negombo, Gampaha District', 7.2089, 79.8383, 'Gampaha', 'western', '0312222237'),
    ds('minuwangoda_ds', 'Divisional Secretariat – Minuwangoda', 'මිනුවන්ගොඩ කොට්ඨාශ ලේකම් කාර්යාලය', 'மினுவன்கொட பிரிவு செயலகம்', 'Minuwangoda, Gampaha District', 7.1667, 79.9500, 'Gampaha', 'western', '0112295071'),
    ds('ja_ela_ds', 'Divisional Secretariat – Ja-Ela', 'ජා-ඇල කොට්ඨාශ ලේකම් කාර්යාලය', 'ஜா-ஏல பிரிவு செயலகம்', 'Ja-Ela, Gampaha District', 7.0736, 79.8919, 'Gampaha', 'western', '0112234017'),
    ds('katana_ds', 'Divisional Secretariat – Katana', 'කටාන කොට්ඨාශ ලේකම් කාර්යාලය', 'கட்டான பிரிவு செயலகம்', 'Katana, Gampaha District', 7.1600, 79.8700, 'Gampaha', 'western', '0312253040'),
    ds('kelaniya_ds', 'Divisional Secretariat – Kelaniya', 'කෙළණිය කොට්ඨාශ ලේකම් කාර්යාලය', 'கேலனிய பிரிவு செயலகம்', 'Kelaniya, Gampaha District', 6.9600, 79.9200, 'Gampaha', 'western', '0112913093'),
    ds('wattala_ds', 'Divisional Secretariat – Wattala', 'වත්තල කොට්ඨාශ ලේකම් කාර්යාලය', 'வட்டளை பிரிவு செயலகம்', 'Wattala, Gampaha District', 6.9900, 79.8900, 'Gampaha', 'western', '0112939074'),
    ds('mahara_ds', 'Divisional Secretariat – Mahara', 'මහර කොට්ඨාශ ලේකම් කාර්යාලය', 'மஹர பிரிவு செயலகம்', 'Mahara, Gampaha District', 7.0500, 80.0200, 'Gampaha', 'western', '0332290061'),
    ds('divulapitiya_ds', 'Divisional Secretariat – Divulapitiya', 'දිවුලපිටිය කොට්ඨාශ ලේකම් කාර්යාලය', 'திவுலபிட்டிய பிரிவு செயலகம்', 'Divulapitiya, Gampaha District', 7.2200, 80.0700, 'Gampaha', 'western', '0332265035'),
    ds('mirigama_ds', 'Divisional Secretariat – Mirigama', 'මිරිගම කොට්ඨාශ ලේකම් කාර්යාලය', 'மிரிகம பிரிவு செயலகம்', 'Mirigama, Gampaha District', 7.2400, 80.1200, 'Gampaha', 'western', '0332274035'),
    ds('attanagalla_ds', 'Divisional Secretariat – Attanagalla', 'අත්තනගල්ල කොට්ඨාශ ලේකම් කාර්යාලය', 'அட்டனகல்ல பிரிவு செயலகம்', 'Attanagalla, Gampaha District', 7.1100, 80.0700, 'Gampaha', 'western', '0332290064'),
    ds('biyagama_ds', 'Divisional Secretariat – Biyagama', 'බියගම කොට්ඨාශ ලේකම් කාර්යාලය', 'பியகம பிரிவு செயலகம்', 'Biyagama, Gampaha District', 6.9700, 80.0000, 'Gampaha', 'western', '0112403040'),
    # Kalutara district
    ds('kalutara_ds', 'Divisional Secretariat – Kalutara', 'කළුතර කොට්ඨාශ ලේකම් කාර්යාලය', 'களுத்துறை பிரிவு செயலகம்', 'Kalutara, Western Province', 6.5860, 79.9607, 'Kalutara', 'western', '0342222381'),
    ds('beruwala_ds', 'Divisional Secretariat – Beruwala', 'බේරුවල කොට්ඨාශ ලේකම් කාර්යාලය', 'பெருவல பிரிவு செயலகம்', 'Beruwala, Kalutara District', 6.4750, 79.9850, 'Kalutara', 'western', '0342275047'),
    ds('agalawatta_ds', 'Divisional Secretariat – Agalawatta', 'අගලවත්ත කොට්ඨාශ ලේකම් කාර්යාලය', 'அகலவட்ட பிரிவு செயலகம்', 'Agalawatta, Kalutara District', 6.5400, 80.1100, 'Kalutara', 'western', '0342264031'),
    ds('matugama_ds', 'Divisional Secretariat – Matugama', 'මාතුගම කොට්ඨාශ ලේකම් කාර්යාලය', 'மாட்டுகம பிரிவு செயலகம்', 'Matugama, Kalutara District', 6.5450, 80.1250, 'Kalutara', 'western', '0342247035'),
    ds('horana_ds', 'Divisional Secretariat – Horana', 'හොරණ කොට්ඨාශ ලේකම් කාර්යාලය', 'ஹொரண பிரிவு செயலகம்', 'Horana, Kalutara District', 6.7166, 80.0607, 'Kalutara', 'western', '0342261041'),
    ds('bandaragama_ds', 'Divisional Secretariat – Bandaragama', 'බන්ඩාරගම කොට්ඨාශ ලේකම් කාර்யாලය', 'பண்டாரகம பிரிவு செயலகம்', 'Bandaragama, Kalutara District', 6.7100, 79.9900, 'Kalutara', 'western', '0382292034'),
    ds('bulathsinhala_ds', 'Divisional Secretariat – Bulathsinhala', 'බුලත්සිංහල කොට්ඨාශ ලේකම් කාර්යාලය', 'புலத்சிங்கள பிரிவு செயலகம்', 'Bulathsinhala, Kalutara District', 6.5800, 80.1700, 'Kalutara', 'western', '0342265041'),
    ds('millaniya_ds', 'Divisional Secretariat – Millaniya', 'මිල්ලනිය කොට්ඨාශ ලේකම් කාර්යාලය', 'மில்லனிய பிரிவு செயலகம்', 'Millaniya, Kalutara District', 6.6400, 80.0400, 'Kalutara', 'western', '0342261033'),
    ds('ingiriya_ds', 'Divisional Secretariat – Ingiriya', 'ඉංගිරිය කොට්ඨාශ ලේකම් කාර්යාලය', 'இங்கிரிய பிரிவு செயலகம்', 'Ingiriya, Kalutara District', 6.7400, 80.1000, 'Kalutara', 'western', '0342262041'),
    ds('dodangoda_ds', 'Divisional Secretariat – Dodangoda', 'දොඩංගොඩ කොට්ඨාශ ලේකම් කාර්යාලය', 'தொடன்கொட பிரிவு செயலகம்', 'Dodangoda, Kalutara District', 6.5600, 79.9900, 'Kalutara', 'western', '0342276034'),

    # ── CENTRAL PROVINCE ─────────────────────────────────────────────────────
    # Kandy district
    ds('kandy_ds', 'Divisional Secretariat – Kandy', 'මහනුවර කොට්ඨාශ ලේකම් කාර්යාලය', 'கண்டி பிரிவு செயலகம்', 'Kandy, Central Province', 7.2906, 80.6337, 'Kandy', 'central', '0812232040'),
    ds('harispattuwa_ds', 'Divisional Secretariat – Harispattuwa', 'හරිස්පත්තුව කොට්ඨාශ ලේකම් කාර்யාலය', 'ஹரிஸ்பத்துவ பிரிவு செயலகம்', 'Harispattuwa, Kandy District', 7.2700, 80.5800, 'Kandy', 'central', '0812232062'),
    ds('gangawata_korale_ds', 'Divisional Secretariat – Gangawata Korale', 'ගංගාවාට කෝරළේ කොට්ඨාශ ලේකම් කාර්යාලය', 'கங்காவட கோரலே பிரிவு செயலகம்', 'Gangawata Korale, Kandy District', 7.3100, 80.6500, 'Kandy', 'central', '0812232065'),
    ds('udunuwara_ds', 'Divisional Secretariat – Udunuwara', 'උඩනුවර කොට්ඨාශ ලේකම් කාර්යාලය', 'உடநுவர பிரிவு செயலகம்', 'Udunuwara, Kandy District', 7.1800, 80.6200, 'Kandy', 'central', '0812232070'),
    ds('yatinuwara_ds', 'Divisional Secretariat – Yatinuwara', 'යටිනුවර කොට්ඨාශ ලේකම් කාර்யාலய', 'யட்டினுவர பிரிவு செயலகம்', 'Yatinuwara, Kandy District', 7.2000, 80.5900, 'Kandy', 'central', '0812232073'),
    ds('akurana_ds', 'Divisional Secretariat – Akurana', 'අකුරණ කොට්ඨාශ ලේකම් කාර්යාලය', 'அக்குரண பிரிவு செயலகம்', 'Akurana, Kandy District', 7.3500, 80.6200, 'Kandy', 'central', '0812237029'),
    ds('kundasale_ds', 'Divisional Secretariat – Kundasale', 'කුණ්ඩසාලේ කොට්ඨාශ ලේකම් කාර්යාලය', 'குண்டசாலே பிரிவு செயலகம்', 'Kundasale, Kandy District', 7.2800, 80.6800, 'Kandy', 'central', '0812232081'),
    ds('tumpane_ds', 'Divisional Secretariat – Tumpane', 'තුම්පනේ කොට්ඨාශ ලේකම් කාර්යාලය', 'தும்பன் பிரிவு செயலகம்', 'Tumpane, Kandy District', 7.3200, 80.7000, 'Kandy', 'central', '0812389022'),
    ds('poojapitiya_ds', 'Divisional Secretariat – Poojapitiya', 'පූජාපිටිය කොට්ඨාශ ලේකම් කාර්යාලය', 'பூஜாபிட்டிய பிரிவு செயலகம்', 'Poojapitiya, Kandy District', 7.3600, 80.7000, 'Kandy', 'central', '0812382039'),
    ds('minipe_ds', 'Divisional Secretariat – Minipe', 'මිනිපේ කොට්ඨාශ ලේකම් කාර்யාලය', 'மினிபே பிரிவு செயலகம்', 'Minipe, Kandy District', 7.2300, 80.8600, 'Kandy', 'central', '0552263058'),
    ds('hewaheta_ds', 'Divisional Secretariat – Hewaheta', 'හේවාහේට කොට්ඨාශ ලේකම් කාර්යාලය', 'ஹேவாஹேட பிரிவு செயலகம்', 'Hewaheta, Kandy District', 7.1300, 80.7500, 'Kandy', 'central', '0812384041'),
    ds('nawalapitiya_ds', 'Divisional Secretariat – Nawalapitiya', 'නාවලපිටිය කොට්ඨාශ ලේකම් කාර්යාලය', 'நவலபிட்டிய பிரிவு செயலகம்', 'Nawalapitiya, Kandy District', 7.0547, 80.5299, 'Kandy', 'central', '0542222270'),
    ds('hatharaliyadda_ds', 'Divisional Secretariat – Hatharaliyadda', 'හතරළියද්ද කොට්ඨාශ ලේකම් කාර්යාලය', 'ஹட்டரலியட்ட பிரிவு செயலகம்', 'Hatharaliyadda, Kandy District', 7.1000, 80.6800, 'Kandy', 'central', '0812386052'),
    ds('medadumbara_ds', 'Divisional Secretariat – Medadumbara', 'මැදදුඹර කොට්ඨාශ ලේකම් කාර්යාලය', 'மேடதும்பர பிரிவு செயலகம்', 'Medadumbara, Kandy District', 7.2700, 80.7700, 'Kandy', 'central', '0812232090'),
    ds('delthota_ds', 'Divisional Secretariat – Delthota', 'දෙල්තොට කොට්ඨාශ ලේකම් කාර්යාලය', 'டெல்தொட பிரிவு செயலகம்', 'Delthota, Kandy District', 7.1600, 80.6000, 'Kandy', 'central', '0542262053'),
    ds('pathahewaheta_ds', 'Divisional Secretariat – Pathahewaheta', 'පාතහේවාහේට කොට්ඨාශ ලේකම් කාර்யාலය', 'பாதஹேவாஹேட பிரிவு செயலகம்', 'Pathahewaheta, Kandy District', 7.0800, 80.6700, 'Kandy', 'central', '0542264043'),
    # Matale district
    ds('matale_ds', 'Divisional Secretariat – Matale', 'මාතලේ කොට්ඨාශ ලේකම් කාර்யාலය', 'மாத்தளை பிரிவு செயலகம்', 'Matale, Central Province', 7.4675, 80.6234, 'Matale', 'central', '0662222250'),
    ds('dambulla_ds', 'Divisional Secretariat – Dambulla', 'දඹුල්ල කොට්ඨාශ ලේකම් කාර්යාලය', 'டம்புள்ள பிரிவு செயலகம்', 'Dambulla, Matale District', 7.8675, 80.6514, 'Matale', 'central', '0662284038'),
    ds('galewela_ds', 'Divisional Secretariat – Galewela', 'ගලේවෙල කොට්ඨාශ ලේකම් කාර්யාලය', 'கலேவெல பிரிவு செயலகம்', 'Galewela, Matale District', 7.7400, 80.5900, 'Matale', 'central', '0662263035'),
    ds('rattota_ds', 'Divisional Secretariat – Rattota', 'රත්ටොට කොට්ඨාශ ලේකම් කාර්යාලය', 'ரட்டோட்ட பிரிவு செயலகம்', 'Rattota, Matale District', 7.4900, 80.7200, 'Matale', 'central', '0662255038'),
    ds('ukuwela_ds', 'Divisional Secretariat – Ukuwela', 'උකුවෙල කොට්ඨාශ ලේකම් කාර්යාලය', 'உகுவெல பிரிவு செயலகம்', 'Ukuwela, Matale District', 7.5300, 80.6500, 'Matale', 'central', '0662222265'),
    ds('naula_ds', 'Divisional Secretariat – Naula', 'නාඋල කොට්ඨාශ ලේකම් කාර්යාලය', 'நவுல பிரிவு செயலகம்', 'Naula, Matale District', 7.6700, 80.6300, 'Matale', 'central', '0662279039'),
    ds('pallepola_ds', 'Divisional Secretariat – Pallepola', 'පල්ලේපොල කොට්ඨාශ ලේකම් කාර්යාලය', 'பல்லேபொல பிரிவு செயலகம்', 'Pallepola, Matale District', 7.6000, 80.6200, 'Matale', 'central', '0662272037'),
    ds('yatawatta_ds', 'Divisional Secretariat – Yatawatta', 'යටවත්ත කොට්ඨාශ ලේකම් කාර்யාலய', 'யட்டவட்ட பிரிவு செயலகம்', 'Yatawatta, Matale District', 7.5800, 80.7600, 'Matale', 'central', '0662258041'),
    ds('laggala_ds', 'Divisional Secretariat – Laggala-Pallegama', 'ලග්ගල-පල්ලේගම කොට්ඨාශ ලේකම් කාර්යාලය', 'லக்கல-பல்லேகம பிரிவு செயலகம்', 'Laggala, Matale District', 7.6500, 80.7500, 'Matale', 'central', '0662258045'),
    ds('wilgamuwa_ds', 'Divisional Secretariat – Wilgamuwa', 'විල්ගමුව කොට්ඨාශ ලේකම් කාර්යාලය', 'வில்கமுவ பிரிவு செயலகம்', 'Wilgamuwa, Matale District', 7.8100, 80.7000, 'Matale', 'central', '0662295030'),
    ds('ambanganga_ds', 'Divisional Secretariat – Ambanganga Korale', 'අඹගංග කෝරළේ කොට්ඨාශ ලේකම් කාර්යාලය', 'அம்பங்கங்க கோரலே பிரிவு செயலகம்', 'Ambanganga, Matale District', 7.5600, 80.6800, 'Matale', 'central', '0662222270'),
    # Nuwara Eliya district
    ds('nuwaraeliya_ds', 'Divisional Secretariat – Nuwara Eliya', 'නුවරඑළිය කොට්ඨාශ ලේකම් කාර්යාලය', 'நுவரெலியா பிரிவு செயலகம்', 'Nuwara Eliya, Central Province', 6.9697, 80.7833, 'Nuwara Eliya', 'central', '0522222278'),
    ds('ambagamuwa_ds', 'Divisional Secretariat – Ambagamuwa', 'අඹගමුව කොට්ඨාශ ලේකම් කාර්යාලය', 'அம்பகமுவ பிரிவு செயலகம்', 'Ambagamuwa, Nuwara Eliya District', 6.9000, 80.6700, 'Nuwara Eliya', 'central', '0522230052'),
    ds('kotmale_ds', 'Divisional Secretariat – Kotmale', 'කෝතලේ කොට්ඨාශ ලේකම් කාර්යාලය', 'கொத்மலே பிரிவு செயலகம்', 'Kotmale, Nuwara Eliya District', 7.0400, 80.6300, 'Nuwara Eliya', 'central', '0522236043'),
    ds('walapane_ds', 'Divisional Secretariat – Walapane', 'වලපනේ කොට්ඨාශ ලේකම් කාර්යාලය', 'வலப்பனை பிரிவு செயலகம்', 'Walapane, Nuwara Eliya District', 7.0000, 80.8200, 'Nuwara Eliya', 'central', '0552261049'),
    ds('hanguranketha_ds', 'Divisional Secretariat – Hanguranketha', 'හංගුරන්කෙත කොට්ඨාශ ලේකම් කාර්යාලය', 'ஹங்குரன்கேத பிரிவு செயலகம்', 'Hanguranketha, Nuwara Eliya District', 7.1200, 80.7200, 'Nuwara Eliya', 'central', '0812355043'),

    # ── SOUTHERN PROVINCE ────────────────────────────────────────────────────
    # Galle district
    ds('galle_ds', 'Divisional Secretariat – Galle', 'ගාල්ල කොට්ඨාශ ලේකම් කාර්යාලය', 'காலி பிரிவு செயலகம்', 'Galle, Southern Province', 6.0535, 80.2210, 'Galle', 'southern', '0912222341'),
    ds('baddegama_ds', 'Divisional Secretariat – Baddegama', 'බද්දේගම කොට්ඨාශ ලේකම් කාර்யාலය', 'பட்டேகம பிரிவு செயலகம்', 'Baddegama, Galle District', 6.1800, 80.2100, 'Galle', 'southern', '0912295038'),
    ds('ambalangoda_ds', 'Divisional Secretariat – Ambalangoda', 'අඹලන්ගොඩ කොට්ඨාශ ලේකම් කාර්යාලය', 'அம்பலங்கொட பிரிவு செயலகம்', 'Ambalangoda, Galle District', 6.2349, 80.0558, 'Galle', 'southern', '0912258040'),
    ds('hikkaduwa_ds', 'Divisional Secretariat – Hikkaduwa', 'හික්කඩුව කොට්ඨාශ ලේකම් කාර්යාලය', 'ஹிக்கடுவ பிரிவு செயலகம்', 'Hikkaduwa, Galle District', 6.1394, 80.1063, 'Galle', 'southern', '0912277040'),
    ds('habaraduwa_ds', 'Divisional Secretariat – Habaraduwa', 'හබරාදූව කොට්ඨාශ ලේකම් කාར्यාලය', 'ஹபரதுவ பிரிவு செயலகம்', 'Habaraduwa, Galle District', 6.0600, 80.1800, 'Galle', 'southern', '0912222355'),
    ds('akmeemana_ds', 'Divisional Secretariat – Akmeemana', 'අකමීමාන කොට්ඨාශ ලේකම් කාර்யாලය', 'அக்மீமன பிரிவு செயலகம்', 'Akmeemana, Galle District', 6.0900, 80.2600, 'Galle', 'southern', '0912222350'),
    ds('elpitiya_ds', 'Divisional Secretariat – Elpitiya', 'ඇල්පිටිය කොට්ඨාශ ලේකම් කාර்யාலය', 'எல்பிட்டிய பிரிவு செயலகம்', 'Elpitiya, Galle District', 6.2900, 80.1700, 'Galle', 'southern', '0912293040'),
    ds('imaduwa_ds', 'Divisional Secretariat – Imaduwa', 'ඉමදුව කොට්ඨාශ ලේකම් කාර්යාලය', 'இமதுவ பிரிவு செயலகம்', 'Imaduwa, Galle District', 6.1000, 80.3000, 'Galle', 'southern', '0912299040'),
    ds('nagoda_ds', 'Divisional Secretariat – Nagoda', 'නාගොඩ කොට්ඨාශ ලේකම් කාර་யාලය', 'நாகொட பிரிவு செயலகம்', 'Nagoda, Galle District', 6.1200, 80.2400, 'Galle', 'southern', '0912222360'),
    ds('neluwa_ds', 'Divisional Secretariat – Neluwa', 'නේළුව කොට්ඨාශ ලේකම් කාර᷈யාலය', 'நேலுவ பிரிவு செயலகம்', 'Neluwa, Galle District', 6.2100, 80.3300, 'Galle', 'southern', '0912299048'),
    ds('yakkalamulla_ds', 'Divisional Secretariat – Yakkalamulla', 'යක්කල මුල්ල කොට්ඨාශ ලේකම් කාར்யாலய', 'யக்கலமுல்ல பிரிவு செயலகம்', 'Yakkalamulla, Galle District', 6.1600, 80.2800, 'Galle', 'southern', '0912296042'),
    ds('karandeniya_ds', 'Divisional Secretariat – Karandeniya', 'කරන්දෙනිය කොට්ඨාශ ලේකම් කාර்யாலය', 'கரந்தெனிய பிரிவு செயலகம்', 'Karandeniya, Galle District', 6.2600, 80.2000, 'Galle', 'southern', '0912292039'),
    # Matara district
    ds('matara_ds', 'Divisional Secretariat – Matara', 'මාතර කොට්ඨාශ ලේකම් කාර்யாலய', 'மாத்தறை பிரிவு செயலகம்', 'Matara, Southern Province', 5.9549, 80.5550, 'Matara', 'southern', '0412222356'),
    ds('weligama_ds', 'Divisional Secretariat – Weligama', 'වේලිගම කොට්ඨාශ ලේකම් කාර்யாலய', 'வேலிகம பிரிவு செயலகம்', 'Weligama, Matara District', 5.9744, 80.4296, 'Matara', 'southern', '0412250040'),
    ds('hakmana_ds', 'Divisional Secretariat – Hakmana', 'හකමාන කොට්ඨාශ ලේකම් කාර்யாலய', 'ஹக்மன பிரிவு செயலகம்', 'Hakmana, Matara District', 6.0700, 80.6500, 'Matara', 'southern', '0412267040'),
    ds('devinuwara_ds', 'Divisional Secretariat – Devinuwara', 'දෙවිනුවර කොට්ඨාශ ලේකම් කාර்யாலய', 'தேவிநுவர பிரிவு செயலகம்', 'Devinuwara, Matara District', 5.9300, 80.5800, 'Matara', 'southern', '0412225040'),
    ds('dickwella_ds', 'Divisional Secretariat – Dickwella', 'දික්වෙල්ල කොට්ඨාශ ලේකම් කාර្யාලය', 'திக்வெல்ல பிரிவு செயலகம்', 'Dickwella, Matara District', 5.9700, 80.6900, 'Matara', 'southern', '0412292039'),
    ds('akuressa_ds', 'Divisional Secretariat – Akuressa', 'අකුරැස්ස කොට්ඨාශ ලේකම් කාර்யாலய', 'அக்கரேசா பிரிவு செயலகம்', 'Akuressa, Matara District', 6.1100, 80.4800, 'Matara', 'southern', '0412283040'),
    ds('kamburupitiya_ds', 'Divisional Secretariat – Kamburupitiya', 'කඹුරුපිටිය කොட්ඨාශ ලේකම් කාර்யாலய', 'கம்புருபிட்டிய பிரிவு செயலகம்', 'Kamburupitiya, Matara District', 6.0300, 80.4300, 'Matara', 'southern', '0412285039'),
    ds('mulatiyana_ds', 'Divisional Secretariat – Mulatiyana', 'මූලතිව් කොට්ඨාශ ලේකම් – මූලතිකෙ', 'முலதியன பிரிவு செயலகம்', 'Mulatiyana, Matara District', 6.1600, 80.5400, 'Matara', 'southern', '0412268040'),
    ds('pitabeddara_ds', 'Divisional Secretariat – Pitabeddara', 'පිටාබැද්දර කොට්ඨාශ ලේකම් කාර்யாலய', 'பிடாபெட்டர பிரிவு செயலகம்', 'Pitabeddara, Matara District', 6.1400, 80.5700, 'Matara', 'southern', '0412268045'),
    # Hambantota district
    ds('hambantota_ds', 'Divisional Secretariat – Hambantota', 'හම්බන්තොට කොට්ඨාශ ලේකම් කාර்யாலய', 'அம்பாந்தோட்டை பிரிவு செயலகம்', 'Hambantota, Southern Province', 6.1228, 81.1218, 'Hambantota', 'southern', '0472222227'),
    ds('tissamaharama_ds', 'Divisional Secretariat – Tissamaharama', 'තිස්සමහාරාම කොට්ඨාශ ලේකම් කාර்யාலය', 'திஸ்ஸமஹாராம பிரிவு செயலகம்', 'Tissamaharama, Hambantota District', 6.2862, 81.2858, 'Hambantota', 'southern', '0472237040'),
    ds('tangalle_ds', 'Divisional Secretariat – Tangalle', 'තංගල්ල කොට්ඨාශ ලේකம් කාර்யாலய', 'தங்கல்லை பிரிவு செயலகம்', 'Tangalle, Hambantota District', 6.0256, 80.7984, 'Hambantota', 'southern', '0472240040'),
    ds('ambalantota_ds', 'Divisional Secretariat – Ambalantota', 'අඹලන්තොට කොට්ඨාශ ලේකම් කාර்யாலய', 'அம்பலன்தோட்டை பிரிவு செயலகம்', 'Ambalantota, Hambantota District', 6.1100, 81.0200, 'Hambantota', 'southern', '0472223040'),
    ds('beliatta_ds', 'Divisional Secretariat – Beliatta', 'බෙලිඅත්ත කොට්ඨාශ ලේකම් කාර்யாலய', 'பேலியட்ட பிரிவு செயலகம்', 'Beliatta, Hambantota District', 6.0600, 80.9700, 'Hambantota', 'southern', '0472242039'),
    ds('weeraketiya_ds', 'Divisional Secretariat – Weeraketiya', 'වීරකේතිය කොට්ඨාශ ලේකම් කාර்யாலය', 'வீரகேதிய பிரிவு செயலகம்', 'Weeraketiya, Hambantota District', 6.1700, 80.9200, 'Hambantota', 'southern', '0472245040'),
    ds('lunugamvehera_ds', 'Divisional Secretariat – Lunugamvehera', 'ලුණුගම්වෙහෙර කොට්ඨාශ ලේකම් කාර்யාலය', 'லுனுகம்வேஹெர பிரிவு செயலகம்', 'Lunugamvehera, Hambantota District', 6.2200, 81.1700, 'Hambantota', 'southern', '0472238040'),
    ds('katuwana_ds', 'Divisional Secretariat – Katuwana', 'කටුවාන කොට්ඨාශ ලේකම් කාර்யாலய', 'கட்டுவான பிரிவு செயலகம்', 'Katuwana, Hambantota District', 6.1400, 80.9000, 'Hambantota', 'southern', '0472247040'),
    ds('angunakolapelessa_ds', 'Divisional Secretariat – Angunakolapelessa', 'අඟුනකොළපෑලැස්ස කොට්ඨාශ ලේකම්', 'அங்குணகொலபெலஸ்ஸ பிரிவு செயலகம்', 'Angunakolapelessa, Hambantota District', 6.1800, 81.0700, 'Hambantota', 'southern', '0472246040'),
    ds('sooriyawewa_ds', 'Divisional Secretariat – Sooriyawewa', 'සූරියවැව කොට්ඨාශ ලේකම் කාර்யாலய', 'சூரியவேவ பிரிவு செயலகம்', 'Sooriyawewa, Hambantota District', 6.1600, 81.1100, 'Hambantota', 'southern', '0472225040'),

    # ── NORTHERN PROVINCE ────────────────────────────────────────────────────
    # Jaffna district (main Jaffna DS already in seed_national; sub-divisions in seed_ds_offices)
    # Kilinochchi district
    ds('kilinochchi_ds', 'Divisional Secretariat – Kilinochchi', 'කිලිනොච්චිය කොට්ඨාශ ලේකම් කාර་யාලය', 'கிளிநொச்சி பிரிவு செயலகம்', 'Kilinochchi, Northern Province', 9.3803, 80.4036, 'Kilinochchi', 'northern', '0212285015'),
    ds('pachchilaipalli_ds', 'Divisional Secretariat – Pachchilaipalli', 'පච්චිලෙයිපල්ලි කොට්ඨාශ ලේකම් කාර་யාලය', 'பச்சிலைப்பள்ளி பிரிவு செயலகம்', 'Pachchilaipalli, Kilinochchi District', 9.3200, 80.3400, 'Kilinochchi', 'northern', '0212285020'),
    ds('karachchi_ds', 'Divisional Secretariat – Karachchi', 'කාරච්චිය කොට්ඨාශ ලේකම් කාර་யාලය', 'காரச்சி பிரிவு செயலகம்', 'Karachchi, Kilinochchi District', 9.4000, 80.3800, 'Kilinochchi', 'northern', '0212285025'),
    ds('poonakary_ds', 'Divisional Secretariat – Poonakary', 'පූනෑකරිය කොට්ඨාශ ලේකම් කාර་යාලය', 'பூநகரி பிரிவு செயලகம்', 'Poonakary, Kilinochchi District', 9.2100, 80.2500, 'Kilinochchi', 'northern', '0212285030'),
    # Mannar district
    ds('mannar_ds', 'Divisional Secretariat – Mannar', 'මන්නාරම කොට්ඨාශ ලේකම් කාර་යාලය', 'மன்னார் பிரிவு செயலகம்', 'Mannar, Northern Province', 8.9810, 79.9044, 'Mannar', 'northern', '0232222235'),
    ds('manthai_west_ds', 'Divisional Secretariat – Manthai West', 'මන්ඩෙයි බටහිර කොට්ඨාශ ලේකම් කාර་යාලය', 'மந்தை மேற்கு பிரிவு செயலகம்', 'Manthai West, Mannar District', 8.8500, 79.8600, 'Mannar', 'northern', '0232222240'),
    ds('musalai_ds', 'Divisional Secretariat – Musalai', 'මුසලෙයි කොට්ඨාශ ලේකම් කාර་யාலය', 'முசலை பிரிவு செயலகம்', 'Musalai, Mannar District', 8.9200, 80.0200, 'Mannar', 'northern', '0232222245'),
    ds('nanattan_ds', 'Divisional Secretariat – Nanattan', 'නනාත්තන් කොට්ඨාශ ලේකම් කාර་යාලය', 'நாணாட்டன் பிரிவு செயலகம்', 'Nanattan, Mannar District', 8.8300, 80.0500, 'Mannar', 'northern', '0232222250'),
    ds('madhu_ds', 'Divisional Secretariat – Madhu', 'මාදු කොට්ඨාශ ලේකම් කාර་යාලය', 'மடு பிரிவு செயலகம்', 'Madhu, Mannar District', 8.9600, 80.1200, 'Mannar', 'northern', '0232222255'),
    # Mullaitivu district
    ds('mullaitivu_ds', 'Divisional Secretariat – Mullaitivu', 'මුලතිව් කොට්ඨාශ ලේකම් කාර་យාලය', 'முல்லைத்தீவு பிரிவு செயலகம்', 'Mullaitivu, Northern Province', 9.2668, 80.8127, 'Mullaitivu', 'northern', '0212290015'),
    ds('puthukudiyiruppu_ds', 'Divisional Secretariat – Puthukudiyiruppu', 'පුතුකුඩිඉරිප්පු කොට්ඨාශ ලේකම්', 'புதுக்குடியிருப்பு பிரிவு செயலகம்', 'Puthukudiyiruppu, Mullaitivu District', 9.3400, 80.7400, 'Mullaitivu', 'northern', '0212290020'),
    ds('maritimepattu_ds', 'Divisional Secretariat – Maritimepattu', 'මරිටෙයිම්පෑට්ටු කොට්ඨාශ ලේකම්', 'மரிட்டைம்பட்டு பிரிவு செயலகம்', 'Maritimepattu, Mullaitivu District', 9.2000, 80.8500, 'Mullaitivu', 'northern', '0212290025'),
    ds('oddusuddan_ds', 'Divisional Secretariat – Oddusuddan', 'ඔඩ්ඩුසුඩාන් කොට්ඨාශ ලේකම් කාර་යාලය', 'ஒட்டுசுட்டான் பிரிவு செயலகம்', 'Oddusuddan, Mullaitivu District', 9.4000, 80.6500, 'Mullaitivu', 'northern', '0212290030'),
    ds('thunukkai_ds', 'Divisional Secretariat – Thunukkai', 'ථුනුක්කෙයි කොට්ඨාශ ලේකම් කාර་யාලය', 'துணுக்காய் பிரிவு செயலகம்', 'Thunukkai, Mullaitivu District', 9.4700, 80.5300, 'Mullaitivu', 'northern', '0212290035'),
    ds('mankulam_ds', 'Divisional Secretariat – Mankulam', 'මන්කුළාම් කොට්ඨාශ ලේකම් කාර་යාලය', 'மன்குளம் பிரிவு செயலகம்', 'Mankulam, Mullaitivu District', 9.1400, 80.4700, 'Mullaitivu', 'northern', '0212290040'),
    ds('welioya_ds', 'Divisional Secretariat – Welioya', 'වේලිඔය කොට්ඨාශ ලේකම් කාර་යාලය', 'வேலியொய பிரிவு செயலகம்', 'Welioya, Mullaitivu District', 8.8900, 80.6500, 'Mullaitivu', 'northern', '0212290045'),
    # Vavuniya district
    ds('vavuniya_ds', 'Divisional Secretariat – Vavuniya', 'වව්නියාව කොට්ඨාශ ලේකම් කාර་යාලය', 'வவுனியா பிரிவு செயலகம்', 'Vavuniya, Northern Province', 8.7514, 80.4971, 'Vavuniya', 'northern', '0242222224'),
    ds('vavuniya_north_ds', 'Divisional Secretariat – Vavuniya North', 'වව්නියාව උතුර කොට්ඨාශ ලේකම් කාර་යාලය', 'வவுனியா வடக்கு பிரிவு செயலகம்', 'Vavuniya North, Northern Province', 8.8200, 80.4600, 'Vavuniya', 'northern', '0242222228'),
    ds('vengalacheddikulam_ds', 'Divisional Secretariat – Vengalacheddikulam', 'වෙංගලේච්චේඩිකුළාම් කොට්ඨාශ ලේකම', 'வெங்கலச்சேட்டிகுளம் பிரிவு செயலகம்', 'Vengalacheddikulam, Vavuniya District', 8.7000, 80.5500, 'Vavuniya', 'northern', '0242222232'),
    ds('cheddikulam_ds', 'Divisional Secretariat – Cheddikulam', 'ශේඩිකුළාම් කොට්ඨාශ ලේකම් කාර་யාலය', 'செட்டிகுளம் பிரிவு செயலகம்', 'Cheddikulam, Vavuniya District', 8.7800, 80.4300, 'Vavuniya', 'northern', '0242222236'),

    # ── EASTERN PROVINCE ─────────────────────────────────────────────────────
    # Trincomalee district
    ds('trincomalee_ds', 'Divisional Secretariat – Trincomalee', 'ත්‍රිකුණාමලය කොට්ඨාශ ලේකම් කාර་යාලය', 'திருகோணமலை பிரிவு செயலகம்', 'Trincomalee, Eastern Province', 8.5874, 81.2152, 'Trincomalee', 'eastern', '0262222235'),
    ds('kinniya_ds', 'Divisional Secretariat – Kinniya', 'කින්නියා කොට්ඨාශ ලේකම් කාර་යාලය', 'கின்னியா பிரிவு செயலகம்', 'Kinniya, Trincomalee District', 8.5700, 81.2100, 'Trincomalee', 'eastern', '0262226040'),
    ds('muttur_ds', 'Divisional Secretariat – Muttur', 'මූතූර් කොට්ඨාශ ලේකම් කාර་யාලය', 'முத்தூர் பிரிவு செயலகம்', 'Muttur, Trincomalee District', 8.4700, 81.2700, 'Trincomalee', 'eastern', '0262270040'),
    ds('thambalagamuwa_ds', 'Divisional Secretariat – Thambalagamuwa', 'ගාල්ල කොට්ඨාශ ලේකම් – තඹලකාමුව', 'தம்பலகாமுவ பிரிவு செயலகம்', 'Thambalagamuwa, Trincomalee District', 8.3700, 81.0200, 'Trincomalee', 'eastern', '0262272040'),
    ds('kuchchaveli_ds', 'Divisional Secretariat – Kuchchaveli', 'කුච්චවේලිය කොට்ඨාශ ලේකම් කාར་யාலය', 'குச்சவேலி பிரிவு செயலகம்', 'Kuchchaveli, Trincomalee District', 8.8100, 81.0400, 'Trincomalee', 'eastern', '0262276040'),
    ds('seruwila_ds', 'Divisional Secretariat – Seruwila', 'සේරු විල කොට්ඨාශ ලේකම් කාར་யාලය', 'சேருவில பிரிவு செயலகம்', 'Seruwila, Trincomalee District', 8.3200, 81.0800, 'Trincomalee', 'eastern', '0262274040'),
    ds('kantale_ds', 'Divisional Secretariat – Kantale', 'කන්තලේ කොට්ඨාශ ලේකම් කාර་யාලය', 'கந்தளாய் பிரிவு செயலகம்', 'Kantale, Trincomalee District', 8.3900, 80.9900, 'Trincomalee', 'eastern', '0262234040'),
    ds('morawewa_ds', 'Divisional Secretariat – Morawewa', 'මොරවෙව කොට්ඨාශ ලේකම් කාර་யාලය', 'மொரவேவ பிரிவு செயலகம்', 'Morawewa, Trincomalee District', 8.5200, 80.9000, 'Trincomalee', 'eastern', '0262235040'),
    # Batticaloa district
    ds('batticaloa_ds', 'Divisional Secretariat – Batticaloa', 'මඩකළපු කොට්ඨාශ ලේකම් කාර་යාලය', 'மட்டக்களப்பு பிரிவு செயலகம்', 'Batticaloa, Eastern Province', 7.7170, 81.6924, 'Batticaloa', 'eastern', '0652222252'),
    ds('eravur_pattu_ds', 'Divisional Secretariat – Eravur Pattu', 'ඊරාවූර් පැටෝ කොට්ඨාශ ලේකම්', 'ஏரவூர் பட்டு பிரிவு செயலகம்', 'Eravur, Batticaloa District', 7.7900, 81.6000, 'Batticaloa', 'eastern', '0652260040'),
    ds('kattankudy_ds', 'Divisional Secretariat – Kattankudy', 'කට්ටන්කුඩිය කොට්ඨාශ ලේකම් කාར்யாலය', 'கட்டான்குடி பிரிவு செயலகம்', 'Kattankudy, Batticaloa District', 7.6700, 81.6900, 'Batticaloa', 'eastern', '0652234040'),
    ds('koralai_pattu_ds', 'Divisional Secretariat – Koralai Pattu', 'කොරළෙයි පෑටෝ කොට්ඨාශ ලේකම් කාර்யාලය', 'கோரளைப் பட்டு பிரிவு செயலகம்', 'Koralai Pattu, Batticaloa District', 7.6400, 81.7100, 'Batticaloa', 'eastern', '0652235040'),
    ds('manmunai_north_ds', 'Divisional Secretariat – Manmunai North', 'මන්මුනෙයි උතුර කොට්ඨාශ ලේකම් කාར்யාலය', 'மன்முனை வட பிரிவு செயலகம்', 'Manmunai North, Batticaloa District', 7.8200, 81.5800, 'Batticaloa', 'eastern', '0652263040'),
    ds('manmunai_west_ds', 'Divisional Secretariat – Manmunai West', 'මන්මුනෙයි බටහිර කොට්ඨාශ ලේකම් කාර்யாලය', 'மன்முனை மேற்கு பிரிவு செயலகம்', 'Manmunai West, Batticaloa District', 7.7100, 81.5600, 'Batticaloa', 'eastern', '0652264040'),
    ds('paddippalai_ds', 'Divisional Secretariat – Paddippalai', 'පෑඩ්ඩිපලෙයි කොට්ඨාශ ලේකම් කාර்யාலය', 'படிப்பழை பிரிவு செயலகம்', 'Paddippalai, Batticaloa District', 7.8600, 81.5200, 'Batticaloa', 'eastern', '0652268040'),
    # Ampara district
    ds('ampara_ds', 'Divisional Secretariat – Ampara', 'අම්පාර කොට්ඨාශ ලේකම් කාර்யාலය', 'அம்பாறை பிரிவு செயலகம்', 'Ampara, Eastern Province', 7.2992, 81.6736, 'Ampara', 'eastern', '0632222220'),
    ds('kalmunai_ds', 'Divisional Secretariat – Kalmunai', 'කල්මුණේ කොට්ඨාශ ලේකම් கார்யாலய', 'கல்முனை பிரிவு செயலகம்', 'Kalmunai, Ampara District', 7.4117, 81.8256, 'Ampara', 'eastern', '0672220038'),
    ds('sammanthurai_ds', 'Divisional Secretariat – Sammanthurai', 'සම්මාන්තුරෙයි කොට්ඨාශ ලේකම்', 'சம்மாந்துறை பிரிவு செயலகம்', 'Sammanthurai, Ampara District', 7.3800, 81.8000, 'Ampara', 'eastern', '0672255040'),
    ds('pothuvil_ds', 'Divisional Secretariat – Pothuvil', 'පොත්විල් කොට්ඨාශ ලේකම් கார்யாலய', 'பொத்துவில் பிரிவு செயலகம்', 'Pothuvil, Ampara District', 6.8700, 81.8300, 'Ampara', 'eastern', '0632249038'),
    ds('lahugala_ds', 'Divisional Secretariat – Lahugala', 'ලාහුගල කොට்ඨාශ ලේකம் கார்யாலய', 'லஹுகல பிரிவு செயலகம்', 'Lahugala, Ampara District', 7.0800, 81.7000, 'Ampara', 'eastern', '0632265038'),
    ds('mahaoya_ds', 'Divisional Secretariat – Mahaoya', 'මහඅෝය කොට්ඨාශ ලේකම் கார்யாலய', 'மகாஓய பிரிவு செயலகம்', 'Mahaoya, Ampara District', 7.4400, 81.5200, 'Ampara', 'eastern', '0632275038'),
    ds('uhana_ds', 'Divisional Secretariat – Uhana', 'උහාන කොට‍ිඨාශ ලේකම් கார்யாலய', 'உஹான பிரிவு செயலகம்', 'Uhana, Ampara District', 7.3300, 81.6000, 'Ampara', 'eastern', '0632276038'),
    ds('addalaichenai_ds', 'Divisional Secretariat – Addalaichenai', 'අඩ්ඩලෙයිච්චේනෙයි කොට්ඨාශ ලේකම්', 'அட்டாளைச்சேனை பிரிவு செயலகம்', 'Addalaichenai, Ampara District', 7.3500, 81.7900, 'Ampara', 'eastern', '0672257040'),
    ds('thirukkovil_ds', 'Divisional Secretariat – Thirukkovil', 'ත්‍රිකෝවිල් කොට්ඨාශ ලේකම் கார்யாலய', 'திருக்கோவில் பிரிவு செயலகம்', 'Thirukkovil, Ampara District', 6.9600, 81.7700, 'Ampara', 'eastern', '0632249042'),

    # ── NORTH WESTERN PROVINCE ───────────────────────────────────────────────
    # Kurunegala district
    ds('kurunegala_ds', 'Divisional Secretariat – Kurunegala', 'කුරුණෑගල කොට්ඨාශ ලේකම් කාර்யාலय', 'குருநாகல் பிரிவு செயலகம்', 'Kurunegala, North Western Province', 7.4818, 80.3609, 'Kurunegala', 'northwestern', '0372222339'),
    ds('alawwa_ds', 'Divisional Secretariat – Alawwa', 'ආලාව කොට්ඨාශ ලේකம் கார்யாலய', 'அலாவ்வ பிரிவு செயலகம்', 'Alawwa, Kurunegala District', 7.2900, 80.2300, 'Kurunegala', 'northwestern', '0372260040'),
    ds('galgamuwa_ds', 'Divisional Secretariat – Galgamuwa', 'ගල්ගමුව කොට්ඨාශ ලේකම් கார்யாலய', 'கல்கமுவ பிரிவு செயலகம்', 'Galgamuwa, Kurunegala District', 7.9600, 80.1700, 'Kurunegala', 'northwestern', '0372266040'),
    ds('giribawa_ds', 'Divisional Secretariat – Giribawa', 'ගිරිබාව කොට්ඨාශ ලේකම් கார்யாலய', 'கிரிபாவ பிரிவு செயலகம்', 'Giribawa, Kurunegala District', 7.5800, 80.2000, 'Kurunegala', 'northwestern', '0372268040'),
    ds('ibbagamuwa_ds', 'Divisional Secretariat – Ibbagamuwa', 'ඉබ්බාගමුව කොට්ඨාශ ලේකම् கார்யாலய', 'இப்பகமுவ பிரிவு செயலகம்', 'Ibbagamuwa, Kurunegala District', 7.6900, 80.4100, 'Kurunegala', 'northwestern', '0372270040'),
    ds('kotavehera_ds', 'Divisional Secretariat – Kotavehera', 'කොතවෙහෙර කොට්ඨාශ ලේකම் கார்யாலய', 'கொத்தவேஹெர பிரிவு செயலகம்', 'Kotavehera, Kurunegala District', 7.5300, 80.4000, 'Kurunegala', 'northwestern', '0372272040'),
    ds('kuliyapitiya_east_ds', 'Divisional Secretariat – Kuliyapitiya East', 'කුලියාපිටිය නැගෙනහිර කොට්ඨාශ ලේකම්', 'குலியாபிட்டிய கிழக்கு பிரிவு செயலகம்', 'Kuliyapitiya, Kurunegala District', 7.4600, 80.0400, 'Kurunegala', 'northwestern', '0372295040'),
    ds('mawathagama_ds', 'Divisional Secretariat – Mawathagama', 'මාවතගම කොට්ඨාශ ලේකම் கார்யாலய', 'மாவதகம பிரிவு செயலகம்', 'Mawathagama, Kurunegala District', 7.5500, 80.5200, 'Kurunegala', 'northwestern', '0372278040'),
    ds('narammala_ds', 'Divisional Secretariat – Narammala', 'නාරම්මල කොට්ඨාශ ලේකම் கார்யாலய', 'நாரம்மல பிரிவு செயலகம்', 'Narammala, Kurunegala District', 7.3400, 80.3200, 'Kurunegala', 'northwestern', '0372282040'),
    ds('nikaweratiya_ds', 'Divisional Secretariat – Nikaweratiya', 'නිකවැරටිය කොට්ඨාශ ලේකම்', 'நிகவேரட்டிய பிரிவு செயலகம்', 'Nikaweratiya, Kurunegala District', 7.7300, 80.1200, 'Kurunegala', 'northwestern', '0372263040'),
    ds('pannala_ds', 'Divisional Secretariat – Pannala', 'පන්නල කොට්ඨාශ ලේකම் கார்யாலய', 'பன்னல பிரிவு செயலகம்', 'Pannala, Kurunegala District', 7.3700, 80.1200, 'Kurunegala', 'northwestern', '0372285040'),
    ds('polpithigama_ds', 'Divisional Secretariat – Polpithigama', 'පොල්පිතිගම කොட්ඨාශ ලේකම் కார్యాలయ', 'பொல்பிதிகம பிரிவு செயலகம்', 'Polpithigama, Kurunegala District', 7.9000, 80.3200, 'Kurunegala', 'northwestern', '0372288040'),
    ds('polgahawela_ds', 'Divisional Secretariat – Polgahawela', 'පොල්ගහවෙල කොට්ඨාශ ලේකம் கார்யாலய', 'பொல்கஹவெல பிரிவு செயலகம்', 'Polgahawela, Kurunegala District', 7.3300, 80.3000, 'Kurunegala', 'northwestern', '0372286040'),
    ds('rideegama_ds', 'Divisional Secretariat – Rideegama', 'රිදීගම කොට்ඨාශ ලේකම் кар்யாலய', 'ரிடீகம பிரிவு செயலகம்', 'Rideegama, Kurunegala District', 7.6200, 80.2600, 'Kurunegala', 'northwestern', '0372290040'),
    ds('wariyapola_ds', 'Divisional Secretariat – Wariyapola', 'වාරියපොල කොට්ඨාශ ලේකම் கார்யாலय', 'வாரியபொல பிரிவு செயலகம்', 'Wariyapola, Kurunegala District', 7.5700, 80.1200, 'Kurunegala', 'northwestern', '0372293040'),
    ds('bingiriya_ds', 'Divisional Secretariat – Bingiriya', 'බිංගිරිය කොට්ඨාශ ලේකම் கார்யாலය', 'பிங்கிரிய பிரிவு செயலகம்', 'Bingiriya, Kurunegala District', 7.4100, 80.0800, 'Kurunegala', 'northwestern', '0372258040'),
    # Puttalam district
    ds('puttalam_ds', 'Divisional Secretariat – Puttalam', 'පුත්තලම කොට්ඨාශ ලේකම් கார்யாலய', 'புத்தளம் பிரிவு செயலகம்', 'Puttalam, North Western Province', 8.0296, 79.8394, 'Puttalam', 'northwestern', '0322265339'),
    ds('chilaw_ds', 'Divisional Secretariat – Chilaw', 'හලාවත කොට්ඨාශ ලේකම் கார்யாலய', 'சிலாபம் பிரிவு செயலகம்', 'Chilaw, Puttalam District', 7.5757, 79.7957, 'Puttalam', 'northwestern', '0322222230'),
    ds('arachchikattuwa_ds', 'Divisional Secretariat – Arachchikattuwa', 'අරච්චිකට්ටුව කොට්ඨාශ ලේකම' , 'அரச்சிகட்டுவ பிரிவு செயலகம்', 'Arachchikattuwa, Puttalam District', 7.7100, 79.9200, 'Puttalam', 'northwestern', '0322268040'),
    ds('kalpitiya_ds', 'Divisional Secretariat – Kalpitiya', 'කල්පිටිය කොට්ඨාශ ලේකම் கார்யாலय', 'கல்பிட்டி பிரிவு செயலகம்', 'Kalpitiya, Puttalam District', 8.2300, 79.7700, 'Puttalam', 'northwestern', '0322265040'),
    ds('wennappuwa_ds', 'Divisional Secretariat – Wennappuwa', 'වේනප්පුව කොට්ඨාශ ලේකම் கார்யாலய', 'வென்னப்புவ பிரிவு செயலகம்', 'Wennappuwa, Puttalam District', 7.3600, 79.8700, 'Puttalam', 'northwestern', '0312257040'),
    ds('nattandiya_ds', 'Divisional Secretariat – Nattandiya', 'නාත්ත ඩිය කොට්ඨාශ ලේකම் கார்யாலய', 'நட்டண்டிய பிரிவு செயலகம்', 'Nattandiya, Puttalam District', 7.4500, 79.9100, 'Puttalam', 'northwestern', '0322275040'),
    ds('nawagattegama_ds', 'Divisional Secretariat – Nawagattegama', 'නාවගට්ටේගම කොට්ඨාශ ලේකම்', 'நவகட்டேகம பிரிவு செயலகம்', 'Nawagattegama, Puttalam District', 8.1200, 80.0600, 'Puttalam', 'northwestern', '0252270040'),
    ds('pallama_ds', 'Divisional Secretariat – Pallama', 'පල්ලම කොට්ඨාශ ලේකම் கார்யாலய', 'பல்லம பிரிவு செயலகம்', 'Pallama, Puttalam District', 7.9400, 79.9600, 'Puttalam', 'northwestern', '0322260040'),
    ds('vanathavilluwa_ds', 'Divisional Secretariat – Vanathavilluwa', 'වනත්විලූ කොට්ඨාශ ලේකම' , 'வனாதவில்லுவ பிரிவு செயலகம்', 'Vanathavilluwa, Puttalam District', 8.4200, 79.9000, 'Puttalam', 'northwestern', '0322267040'),

    # ── NORTH CENTRAL PROVINCE ───────────────────────────────────────────────
    # Anuradhapura district
    ds('anuradhapura_ds', 'Divisional Secretariat – Anuradhapura', 'අනුරාධපුර කොට්ඨාශ ලේකම් கார்யாலய', 'அனுராதபுரம் பிரிவு செயலகம்', 'Anuradhapura, North Central Province', 8.3114, 80.4037, 'Anuradhapura', 'northcentral', '0252222228'),
    ds('medawachchiya_ds', 'Divisional Secretariat – Medawachchiya', 'මේදවච්චිය කොට்ඨාශ ලේකම் கார்யாலय', 'மேடவச்சிய பிரிவு செயலகம்', 'Medawachchiya, Anuradhapura District', 8.5100, 80.5100, 'Anuradhapura', 'northcentral', '0252265040'),
    ds('kekirawa_ds', 'Divisional Secretariat – Kekirawa', 'කෙකිරාව කොට්ඨාශ ලේකම் கார்யாலய', 'கேக்கிரவ பிரிவு செயலகம்', 'Kekirawa, Anuradhapura District', 8.0300, 80.6000, 'Anuradhapura', 'northcentral', '0252264040'),
    ds('horowpathana_ds', 'Divisional Secretariat – Horowpathana', 'හොරොව්පතාන කොட්ඨාශ ලේකම' , 'ஹொரொவ்பதன பிரிவு செயலகம்', 'Horowpathana, Anuradhapura District', 9.0700, 80.5900, 'Anuradhapura', 'northcentral', '0252278040'),
    ds('galenbindunuwewa_ds', 'Divisional Secretariat – Galenbindunuwewa', 'ගලෙන්බිඳු නුවෙව කොට்ඨාශ ලේකම', 'கலேன்பிந்துநுவேவ பிரிவு செயலகம்', 'Galenbindunuwewa, Anuradhapura District', 8.4100, 80.5300, 'Anuradhapura', 'northcentral', '0252268040'),
    ds('thalawa_ds', 'Divisional Secretariat – Thalawa', 'තලාව කොට்ட ාශ ලේකම் கார்யாலய', 'தலாவ பிரிவு செயலகம்', 'Thalawa, Anuradhapura District', 8.2800, 80.5800, 'Anuradhapura', 'northcentral', '0252279040'),
    ds('thambuttegama_ds', 'Divisional Secretariat – Thambuttegama', 'තඹුත්තේගම කොට்஠ாஷ லேகம் கார்யாலய', 'தம்புட்டேகம பிரிவு செயலகம்', 'Thambuttegama, Anuradhapura District', 8.1300, 80.5200, 'Anuradhapura', 'northcentral', '0252280040'),
    ds('padaviya_ds', 'Divisional Secretariat – Padaviya', 'පදවිය කොට்ட ාශ ලේකම் கார்யாலய', 'படவிய பிரிவு செயலகம்', 'Padaviya, Anuradhapura District', 8.8400, 80.7300, 'Anuradhapura', 'northcentral', '0252282040'),
    ds('rajanganaya_ds', 'Divisional Secretariat – Rajanganaya', 'රාජාංගනය කොට்ட ாශ ලේකම' , 'ராஜாங்கனய பிரிவு செயலகம்', 'Rajanganaya, Anuradhapura District', 8.1800, 80.3400, 'Anuradhapura', 'northcentral', '0252262040'),
    ds('ipalogama_ds', 'Divisional Secretariat – Ipalogama', 'ඉපලෝගම කොට්ඨාශ ලේකම் கார்யாலय', 'இபலோகம பிரிவு செயலகம்', 'Ipalogama, Anuradhapura District', 8.0600, 80.4500, 'Anuradhapura', 'northcentral', '0252283040'),
    ds('kahatagasdigiliya_ds', 'Divisional Secretariat – Kahatagasdigiliya', 'කහතගස් දිගිලිය කොට්ඨාශ ලේකම', 'கஹாதகஸ்திகிலிய பிரிவு செயலகம்', 'Kahatagasdigiliya, Anuradhapura District', 8.5700, 80.7500, 'Anuradhapura', 'northcentral', '0252284040'),
    ds('mihintale_ds', 'Divisional Secretariat – Mihintale', 'මිහිඳු සෑය කොට්ඨාශ ලේකම் கார்யாலय', 'மிஹிந்தலே பிரிவு செயலகம்', 'Mihintale, Anuradhapura District', 8.3500, 80.5100, 'Anuradhapura', 'northcentral', '0252265048'),
    ds('eppawala_ds', 'Divisional Secretariat – Eppawala', 'එප්පාවල කොට்ட ාශ ලේකම' , 'எப்பாவல பிரிவு செயலகம்', 'Eppawala, Anuradhapura District', 8.1800, 80.4300, 'Anuradhapura', 'northcentral', '0252286040'),
    ds('palagala_ds', 'Divisional Secretariat – Palagala', 'පාළගල කොට်ඨාශ ලේකම் கார்யாலय', 'பாலகல பிரிவு செயலகம்', 'Palagala, Anuradhapura District', 8.2200, 80.4800, 'Anuradhapura', 'northcentral', '0252287040'),
    # Polonnaruwa district
    ds('polonnaruwa_ds', 'Divisional Secretariat – Polonnaruwa', 'පොළොන්නරුව කොට්ඨාශ ලේකම් கார்யாலय', 'பொலொன்னறுவை பிரிவு செயலகம்', 'Polonnaruwa, North Central Province', 7.9403, 81.0188, 'Polonnaruwa', 'northcentral', '0272222245'),
    ds('medirigiriya_ds', 'Divisional Secretariat – Medirigiriya', 'මේදිරිගිරිය කොට ්ඨාශ ලේකම' , 'மேதிரிகிரிய பிரிவு செயலகம்', 'Medirigiriya, Polonnaruwa District', 8.0500, 81.1300, 'Polonnaruwa', 'northcentral', '0272247040'),
    ds('dimbulagala_ds', 'Divisional Secretariat – Dimbulagala', 'ඩිම්බුලාගල කොට්ඨාශ ලේකම' , 'டிம்புலகல பிரிவு செயலகம்', 'Dimbulagala, Polonnaruwa District', 7.8800, 81.2300, 'Polonnaruwa', 'northcentral', '0272249040'),
    ds('hingurakgoda_ds', 'Divisional Secretariat – Hingurakgoda', 'හිඟුරක්ගොඩ කොට්ඨාශ ලේකම' , 'ஹிங்குரக்கொட பிரிவு செயலகம்', 'Hingurakgoda, Polonnaruwa District', 8.0200, 80.9800, 'Polonnaruwa', 'northcentral', '0272246040'),
    ds('thamankaduwa_ds', 'Divisional Secretariat – Thamankaduwa', 'තමන්කඩුව කොට ්ඨාශ ලේකම' , 'தமன்கடுவ பிரிவு செயலகம்', 'Thamankaduwa, Polonnaruwa District', 7.9200, 81.0400, 'Polonnaruwa', 'northcentral', '0272222250'),
    ds('welikanda_ds', 'Divisional Secretariat – Welikanda', 'වේලිකන්ද කොට ්ඨාශ ලේකම' , 'வேலிகந்த பிரிவு செயலகம்', 'Welikanda, Polonnaruwa District', 7.7800, 81.1800, 'Polonnaruwa', 'northcentral', '0272255040'),
    ds('lankapura_ds', 'Divisional Secretariat – Lankapura', 'ලංකාපුර කොට ්ඨාශ ලේකම' , 'லங்காபுர பிரிவு செயலகம்', 'Lankapura, Polonnaruwa District', 8.0900, 80.9200, 'Polonnaruwa', 'northcentral', '0272256040'),

    # ── UVA PROVINCE ─────────────────────────────────────────────────────────
    # Badulla district
    ds('badulla_ds', 'Divisional Secretariat – Badulla', 'බදුල්ල කොට ්ඨාශ ලේකම් கார்யாலय', 'பதுளை பிரிவு செயலகம்', 'Badulla, Uva Province', 6.9934, 81.0550, 'Badulla', 'uva', '0552222294'),
    ds('bandarawela_ds', 'Divisional Secretariat – Bandarawela', 'බණ්ඩාරවෙල කොට ்஠ாஷ லேகம் கார்யாலय', 'பண்டாரவேல பிரிவு செயலகம்', 'Bandarawela, Badulla District', 6.8300, 80.9900, 'Badulla', 'uva', '0572222217'),
    ds('haputale_ds', 'Divisional Secretariat – Haputale', 'හාපුතලේ කොට ්ඨාශ ලේකම் கார்யாலय', 'ஹப்புத்தளை பிரிவு செயலகம்', 'Haputale, Badulla District', 6.7667, 80.9500, 'Badulla', 'uva', '0572268040'),
    ds('ella_ds', 'Divisional Secretariat – Ella', 'එල්ල කොට ්ඨාශ ලේකம் கார்யாலय', 'எல்ல பிரிவு செயலகம்', 'Ella, Badulla District', 6.8700, 81.0500, 'Badulla', 'uva', '0572228040'),
    ds('welimada_ds', 'Divisional Secretariat – Welimada', 'වෙලිමඩ කොට ்஠ாஷ லேகம் கார்யாலय', 'வேலிமட பிரிவு செயலகம்', 'Welimada, Badulla District', 6.9100, 80.9200, 'Badulla', 'uva', '0572245040'),
    ds('hali_ela_ds', 'Divisional Secretariat – Hali-Ela', 'හාලිඑල කොට ்஠ாஷ லேகம் கார்யாலय', 'ஹாலி-எல பிரிவு செயலகம்', 'Hali-Ela, Badulla District', 6.9600, 81.0400, 'Badulla', 'uva', '0552222302'),
    ds('passara_ds', 'Divisional Secretariat – Passara', 'පාස්සර කොට ்஠ாஷ லேகம் கார்யாலय', 'பசரை பிரிவு செயலகம்', 'Passara, Badulla District', 7.0500, 81.2000, 'Badulla', 'uva', '0552264040'),
    ds('uva_paranagama_ds', 'Divisional Secretariat – Uva-Paranagama', 'උව-පාරනගම කොට ®஠ாஷ லேகம' , 'உவ-பரணகம பிரிவு செயலகம்', 'Uva-Paranagama, Badulla District', 6.9700, 80.8800, 'Badulla', 'uva', '0572246040'),
    ds('lunugala_ds', 'Divisional Secretariat – Lunugala', 'ලුනුගල කොට ்஠ாஷ லேகம் கார்யாலय', 'லுனுகல பிரிவு செயலகம்', 'Lunugala, Badulla District', 7.0900, 81.1200, 'Badulla', 'uva', '0552267040'),
    ds('kandaketiya_ds', 'Divisional Secretariat – Kandaketiya', 'කදාකේටිය කොட ®஠ாஷ லேகம' , 'கந்தகேட்டிய பிரிவு செயலகம்', 'Kandaketiya, Badulla District', 7.1500, 81.1900, 'Badulla', 'uva', '0552268040'),
    ds('mahiyanganaya_ds', 'Divisional Secretariat – Mahiyanganaya', 'මහියංගන කොට ®஠ாஷ லேகம' , 'மஹியங்கன பிரிவு செயலகம்', 'Mahiyanganaya, Badulla District', 7.3300, 81.0000, 'Badulla', 'uva', '0552257040'),
    ds('soranathota_ds', 'Divisional Secretariat – Soranathota', 'සොරනාතොට කොට ®஠ாஷ லேகம' , 'சொரனதொட பிரிவு செயலகம்', 'Soranathota, Badulla District', 7.1200, 81.0400, 'Badulla', 'uva', '0552269040'),
    ds('rideemaliyadda_ds', 'Divisional Secretariat – Rideemaliyadda', 'රිදී මාලියද්ද கොட ®஠ாஷ லேகம' , 'ரிடீமாலியட்ட பிரிவு செயலகம்', 'Rideemaliyadda, Badulla District', 7.0300, 81.2400, 'Badulla', 'uva', '0552270040'),
    ds('meegahakivula_ds', 'Divisional Secretariat – Meegahakivula', 'මීගහකිවුල கොட ®஠ாஷ லேகம' , 'மீகஹகிவுல பிரிவு செயலகம்', 'Meegahakivula, Badulla District', 6.8900, 81.1400, 'Badulla', 'uva', '0572271040'),
    # Monaragala district
    ds('monaragala_ds', 'Divisional Secretariat – Monaragala', 'මොනරාගල කොට ்஠ாஷ லேகம் கார்யாலय', 'மொனராகல பிரிவு செயலகம்', 'Monaragala, Uva Province', 6.8727, 81.3497, 'Monaragala', 'uva', '0552276291'),
    ds('wellawaya_ds', 'Divisional Secretariat – Wellawaya', 'වෙල්ලවාය கொட ்஠ாஷ லேகம் கார்யாலय', 'வெல்லவாய பிரிவு செயலகம்', 'Wellawaya, Monaragala District', 6.7300, 81.1000, 'Monaragala', 'uva', '0552274040'),
    ds('buttala_ds', 'Divisional Secretariat – Buttala', 'බුත්තල கொட ்஠ாஷ லேகம் கார்யாலय', 'புட்டல பிரிவு செயலகம்', 'Buttala, Monaragala District', 6.7400, 81.2400, 'Monaragala', 'uva', '0552277040'),
    ds('bibile_ds', 'Divisional Secretariat – Bibile', 'බිබිල கொட ்஠ாஷ லேகம் கார்யாலय', 'பிபில பிரிவு செயலகம்', 'Bibile, Monaragala District', 7.1800, 81.2100, 'Monaragala', 'uva', '0552278040'),
    ds('siyabalanduwa_ds', 'Divisional Secretariat – Siyabalanduwa', 'සියඹලන්දුව கொட ்஠ாஷ லேகம' , 'சியபலந்துவ பிரிவு செயலகம்', 'Siyabalanduwa, Monaragala District', 7.0000, 81.5400, 'Monaragala', 'uva', '0552279040'),
    ds('medagama_ds', 'Divisional Secretariat – Medagama', 'මේදගම கொட ்஠ாஷ லேகம் கார்யாலय', 'மேடகம பிரிவு செயலகம்', 'Medagama, Monaragala District', 6.9200, 81.2000, 'Monaragala', 'uva', '0552276295'),
    ds('badalkumbura_ds', 'Divisional Secretariat – Badalkumbura', 'බදල්කුම්බුර கொட ்஠ாஷ லேகம' , 'படல்கும்பர பிரிவு செயலகம்', 'Badalkumbura, Monaragala District', 6.8200, 81.4600, 'Monaragala', 'uva', '0552280040'),
    ds('katharagama_ds', 'Divisional Secretariat – Katharagama', 'කතරගම கொட ்஠ாஷ லேகம் கார்யாலय', 'கதிர்காமம் பிரிவு செயலகம்', 'Katharagama, Monaragala District', 6.4100, 81.3300, 'Monaragala', 'uva', '0472235040'),
    ds('sevanagala_ds', 'Divisional Secretariat – Sevanagala', 'සේවනගල கொட ்஠ாஷ லேகம் கார்யாலय', 'சேவனகல பிரிவு செயலகம்', 'Sevanagala, Monaragala District', 6.5200, 81.0000, 'Monaragala', 'uva', '0472237048'),

    # ── SABARAGAMUWA PROVINCE ─────────────────────────────────────────────────
    # Ratnapura district
    ds('ratnapura_ds', 'Divisional Secretariat – Ratnapura', 'රත්නපුර කොට ්ඨාශ ලේකම் கார்யாலय', 'இரத்தினபுரி பிரிவு செயலகம்', 'Ratnapura, Sabaragamuwa Province', 6.6800, 80.3992, 'Ratnapura', 'sabaragamuwa', '0452222330'),
    ds('eheliyagoda_ds', 'Divisional Secretariat – Eheliyagoda', 'ඇහැලියගොඩ கொட ்஠ாஷ லேகம் கார்யாலய', 'எஹெலியகொட பிரிவு செயலகம்', 'Eheliyagoda, Ratnapura District', 6.8500, 80.2500, 'Ratnapura', 'sabaragamuwa', '0362261040'),
    ds('balangoda_ds', 'Divisional Secretariat – Balangoda', 'බලන්ගොඩ கொட ்஠ாஷ லேகம் கார்யாலय', 'பலன்கொட பிரிவு செயலகம்', 'Balangoda, Ratnapura District', 6.6500, 80.6900, 'Ratnapura', 'sabaragamuwa', '0452288040'),
    ds('rakwana_ds', 'Divisional Secretariat – Rakwana', 'රක්වාන கொட ்஠ாஷ லேகம் கார்யாலய', 'ரக்வான பிரிவு செயலகம்', 'Rakwana, Ratnapura District', 6.5200, 80.5700, 'Ratnapura', 'sabaragamuwa', '0452262040'),
    ds('pelmadulla_ds', 'Divisional Secretariat – Pelmadulla', 'පෙල්මඩුල்ல கொட ்஠ாஷ லேகம் கார்யாலய', 'பெல்மதுல்ல பிரிவு செயலகம்', 'Pelmadulla, Ratnapura District', 6.5900, 80.4500, 'Ratnapura', 'sabaragamuwa', '0452265040'),
    ds('embilipitiya_ds', 'Divisional Secretariat – Embilipitiya', 'ඇඹිලිපිටිය கொட ்஠ாஷ லேகம்', 'எம்பிலிபிட்டிய பிரிவு செயலகம்', 'Embilipitiya, Ratnapura District', 6.3400, 80.8400, 'Ratnapura', 'sabaragamuwa', '0472261040'),
    ds('nivithigala_ds', 'Divisional Secretariat – Nivithigala', 'නිවිතිගල கொட ்஠ாஷ லேகம் கார்யாலย', 'நிவித்திகல பிரிவு செயலகம்', 'Nivithigala, Ratnapura District', 6.5500, 80.3400, 'Ratnapura', 'sabaragamuwa', '0452266040'),
    ds('ayagama_ds', 'Divisional Secretariat – Ayagama', 'ඇයගම கொட ்஠ாஷ லேகம் கார்யாலय', 'அயகம பிரிவு செயலகம்', 'Ayagama, Ratnapura District', 6.5100, 80.4300, 'Ratnapura', 'sabaragamuwa', '0452267040'),
    ds('kiriella_ds', 'Divisional Secretariat – Kiriella', 'කිරිඑල்ල கொட ்஠ாஷ லேகம் கார்யாலय', 'கிரிஎல்ல பிரிவு செயலகம்', 'Kiriella, Ratnapura District', 6.6300, 80.3000, 'Ratnapura', 'sabaragamuwa', '0452268040'),
    ds('opanayake_ds', 'Divisional Secretariat – Opanayake', 'ඔපනායක கொட ்஠ாஷ லேகம் கார்யாலय', 'ஒபனாயக பிரிவு செயலகம்', 'Opanayake, Ratnapura District', 6.6500, 80.6200, 'Ratnapura', 'sabaragamuwa', '0452269040'),
    ds('kalawana_ds', 'Divisional Secretariat – Kalawana', 'කළවාන கொட ்஠ாஷ லேகம் கார்யாலय', 'கலவான பிரிவு செயலகம்', 'Kalawana, Ratnapura District', 6.5400, 80.5100, 'Ratnapura', 'sabaragamuwa', '0452270040'),
    ds('kuruwita_ds', 'Divisional Secretariat – Kuruwita', 'කුරුවිට கொட ்஠ாஷ லேகம் கார்யாலय', 'குருவிட்ட பிரிவு செயலகம்', 'Kuruwita, Ratnapura District', 6.7800, 80.3500, 'Ratnapura', 'sabaragamuwa', '0452271040'),
    ds('imbulpe_ds', 'Divisional Secretariat – Imbulpe', 'ඉඹුල්පේ கொட ்஠ாஷ லேகம் கார்யாலय', 'இம்புல்பே பிரிவு செயலகம்', 'Imbulpe, Ratnapura District', 6.7200, 80.6000, 'Ratnapura', 'sabaragamuwa', '0452272040'),
    # Kegalle district
    ds('kegalle_ds', 'Divisional Secretariat – Kegalle', 'කேගල்ල கொட ்஠ாஷ லேகம் கார்யாலय', 'கேகாலை பிரிவு செயலகம்', 'Kegalle, Sabaragamuwa Province', 7.2513, 80.3464, 'Kegalle', 'sabaragamuwa', '0352222291'),
    ds('mawanella_ds', 'Divisional Secretariat – Mawanella', 'මාවනැල்ල கொட ்஠ாஷ லேகம் கார்யாலय', 'மாவனெல்ல பிரிவு செயலகம்', 'Mawanella, Kegalle District', 7.2500, 80.4500, 'Kegalle', 'sabaragamuwa', '0352261040'),
    ds('warakapola_ds', 'Divisional Secretariat – Warakapola', 'වරකාපොල கொட ்஠ாஷ லேகம் கார்யாலय', 'வரகாபொல பிரிவு செயலகம்', 'Warakapola, Kegalle District', 7.2500, 80.2700, 'Kegalle', 'sabaragamuwa', '0352263040'),
    ds('rambukkana_ds', 'Divisional Secretariat – Rambukkana', 'රඹුක්කාන கொட ்஠ாஷ லேகம் கார்யாலय', 'ரம்புக்கான பிரிவு செயலகம்', 'Rambukkana, Kegalle District', 7.3300, 80.4100, 'Kegalle', 'sabaragamuwa', '0352265040'),
    ds('aranayaka_ds', 'Divisional Secretariat – Aranayaka', 'ඇරණායක கொட ்஠ாஷ லேகம் கார்யாலय', 'அரணாயக பிரிவு செயலகம்', 'Aranayaka, Kegalle District', 7.2100, 80.3700, 'Kegalle', 'sabaragamuwa', '0352267040'),
    ds('dehiovita_ds', 'Divisional Secretariat – Dehiovita', 'දෙහිඕවිට கொட ்஠ாஷ லேகம் கார்யாலय', 'டேஹியோவிட பிரிவு செயலகம்', 'Dehiovita, Kegalle District', 7.0700, 80.4000, 'Kegalle', 'sabaragamuwa', '0352268040'),
    ds('yatiyanthota_ds', 'Divisional Secretariat – Yatiyanthota', 'යටියන්තොට கொட ்஠ாஷ லேகம் கார்யாலय', 'யட்டியந்தொட பிரிவு செயலகம்', 'Yatiyanthota, Kegalle District', 7.1100, 80.4700, 'Kegalle', 'sabaragamuwa', '0352270040'),
    ds('bulathkohupitiya_ds', 'Divisional Secretariat – Bulathkohupitiya', 'බුලත්කොහුපිටිය கொட ்஠ாஷ லேகம', 'புலத்கொஹுபிட்டிய பிரிவு செயலகம்', 'Bulathkohupitiya, Kegalle District', 7.1800, 80.3500, 'Kegalle', 'sabaragamuwa', '0352272040'),
    ds('ruwanwella_ds', 'Divisional Secretariat – Ruwanwella', 'රුවන්වෙල கொட ்஠ாஷ லேகம் கார்யாலய', 'ருவன்வெல்ல பிரிவு செயலகம்', 'Ruwanwella, Kegalle District', 7.0400, 80.2600, 'Kegalle', 'sabaragamuwa', '0352273040'),
    ds('deraniyagala_ds', 'Divisional Secretariat – Deraniyagala', 'දෙරණියගල கொட ்஠ாஷ லேகம் கார்யாலய', 'டேரனியகல பிரிவு செயலகம்', 'Deraniyagala, Kegalle District', 6.9200, 80.3400, 'Kegalle', 'sabaragamuwa', '0352274040'),
    ds('galigamuwa_ds', 'Divisional Secretariat – Galigamuwa', 'ගලිගමුව கொட ்஠ாஷ லேகம் கார்யாலய', 'கலிகமுவ பிரிவு செயலகம்', 'Galigamuwa, Kegalle District', 7.3200, 80.2000, 'Kegalle', 'sabaragamuwa', '0352275040'),
]


class Command(BaseCommand):
    help = 'Seed all DS divisional secretariat offices across all 25 Sri Lanka districts'

    def add_arguments(self, parser):
        parser.add_argument('--fresh', action='store_true', help='Delete existing entries before seeding')

    @transaction.atomic
    def handle(self, *args, **options):
        ensure_cat()

        if options['fresh']:
            codes = [d['code'] for d in ALL_DS]
            deleted, _ = Service.objects.filter(code__in=codes).delete()
            self.stdout.write(f'Deleted {deleted} existing entries')

        created = updated = 0
        for entry in ALL_DS:
            svc, was_created = Service.objects.update_or_create(
                code=entry['code'],
                defaults={
                    'name_en': entry['name_en'],
                    'name_si': entry['name_si'],
                    'name_ta': entry['name_ta'],
                    'department_en': DEPT_EN,
                    'department_si': DEPT_SI,
                    'department_ta': DEPT_TA,
                    'category_id': 'government',
                    'address_en': entry['address_en'],
                    'address_si': entry['address_en'],
                    'address_ta': entry['address_en'],
                    'lat': entry['lat'],
                    'lng': entry['lng'],
                    'district': entry['district'],
                }
            )
            if was_created:
                created += 1
                if entry.get('phone'):
                    ServicePhone.objects.create(
                        service=svc,
                        number=entry['phone'],
                        label_en='Main Line',
                        label_si='ප්‍රධාන රේඛාව',
                        label_ta='முதன்மை இணைப்பு',
                    )
                add_hours(svc)
            else:
                updated += 1

        total = Service.objects.count()
        self.stdout.write(self.style.SUCCESS(
            f'Done — {created} created, {updated} updated. Total services: {total}'
        ))
