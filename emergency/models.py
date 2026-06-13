from django.db import models


class EmergencyHotline(models.Model):
    """A national emergency hotline tile shown on the Emergency hub and the
    home-screen quick-dial row.

    The display name stays a translation key (`name_key`, resolved by the
    app's i18n files) and `icon_key` maps to a Flutter icon client-side —
    everything else (which hotlines exist, their numbers, colours, ordering
    and whether they appear in quick-dial) is owned by the database.
    """

    name_key = models.CharField(max_length=64)
    number = models.CharField(max_length=16)
    icon_key = models.CharField(max_length=32)
    color = models.CharField(max_length=7)  # Hex, e.g. "#A32D2D"
    is_quick_dial = models.BooleanField(default=False)
    sort_order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        db_table = 'emergency_hotlines'
        ordering = ['sort_order']

    def __str__(self):
        return f'{self.name_key} ({self.number})'
