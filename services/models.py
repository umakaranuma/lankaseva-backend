from django.db import models

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
    id = models.CharField(max_length=100, primary_key=True)
    
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

    # Simplified representation. Format: "HH:MM-HH:MM" e.g., "08:30-16:15". Null means closed.
    mon = models.CharField(max_length=20, null=True, blank=True)
    tue = models.CharField(max_length=20, null=True, blank=True)
    wed = models.CharField(max_length=20, null=True, blank=True)
    thu = models.CharField(max_length=20, null=True, blank=True)
    fri = models.CharField(max_length=20, null=True, blank=True)
    sat = models.CharField(max_length=20, null=True, blank=True)
    sun = models.CharField(max_length=20, null=True, blank=True)

    class Meta:
        db_table = 'opening_hours'

    def __str__(self):
        return f"Hours for {self.service.name_en}"
