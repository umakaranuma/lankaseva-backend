import django
from django.db import models

# Django renamed CheckConstraint's keyword from `check` to `condition` in 5.1.
# Support both so the project runs under either version installed here.
CHECK_KW = 'condition' if django.VERSION >= (5, 1) else 'check'


class ServiceCategory(models.TextChoices):
    """Mirrors the mobile app's ServiceCategory enum (app_constants.dart)."""

    ELECTRICITY = 'electricity', 'Electricity'
    WATER = 'water', 'Water'
    HOSPITAL = 'hospital', 'Hospitals'
    POLICE = 'police', 'Police'
    COURT = 'court', 'Courts'
    SCHOOL = 'school', 'Schools'
    GOVERNMENT = 'government', 'Government'
    TRANSPORT = 'transport', 'Transport'
    POST = 'post', 'Post Office'

class Service(models.Model):
    # Integer auto-PK (id). The old slug ('colombo_nhsl') is kept as a stable
    # unique `code` so seeds stay idempotent and human-readable.
    code = models.CharField(max_length=100, unique=True)

    name_en = models.CharField(max_length=255)
    name_si = models.CharField(max_length=255)
    name_ta = models.CharField(max_length=255)
    
    department_en = models.CharField(max_length=255)
    department_si = models.CharField(max_length=255)
    department_ta = models.CharField(max_length=255)
    
    category = models.CharField(max_length=50, choices=ServiceCategory.choices)
    district = models.CharField(max_length=100)
    
    address_en = models.TextField()
    address_si = models.TextField()
    address_ta = models.TextField()
    
    lat = models.FloatField()
    lng = models.FloatField()
    
    website = models.URLField(max_length=1024, null=True, blank=True)
    whatsapp = models.CharField(max_length=20, null=True, blank=True)
    
    is_emergency = models.BooleanField(default=False)

    class Meta:
        db_table = 'services'

    def __str__(self):
        return f"{self.name_en} ({self.district})"


class ServicePhone(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='phones')
    label_en = models.CharField(max_length=100)
    label_si = models.CharField(max_length=100)
    label_ta = models.CharField(max_length=100)
    number = models.CharField(max_length=20)
    is_primary = models.BooleanField(default=False)

    class Meta:
        db_table = 'service_phones'

    def __str__(self):
        return f"{self.number} - {self.label_en}"


class OpeningHours(models.Model):
    service = models.OneToOneField(Service, on_delete=models.CASCADE, related_name='hours')
    is_always_open = models.BooleanField(default=False)
    notes = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'opening_hours'

    def __str__(self):
        return f"Hours for {self.service.name_en}"


class OpeningHourSlot(models.Model):
    """Start/end time for one weekday. A weekday without a row is closed."""

    class Weekday(models.IntegerChoices):
        MONDAY = 1
        TUESDAY = 2
        WEDNESDAY = 3
        THURSDAY = 4
        FRIDAY = 5
        SATURDAY = 6
        SUNDAY = 7

    hours = models.ForeignKey(OpeningHours, on_delete=models.CASCADE, related_name='slots')
    weekday = models.PositiveSmallIntegerField(choices=Weekday.choices)
    open_time = models.TimeField()
    close_time = models.TimeField()

    class Meta:
        db_table = 'opening_hour_slots'
        ordering = ['weekday']
        constraints = [
            models.UniqueConstraint(fields=['hours', 'weekday'], name='one_slot_per_weekday'),
            models.CheckConstraint(name='close_after_open',
                                   **{CHECK_KW: models.Q(close_time__gt=models.F('open_time'))}),
        ]

    def __str__(self):
        return f"{self.get_weekday_display()} {self.open_time}-{self.close_time}"
