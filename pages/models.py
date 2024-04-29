from django.db import models
from django.utils import timezone
from django.urls import reverse
import datetime
import pytz

class CME(models.Model):
    cme_number = models.CharField(max_length=200, default='none')
 #   author = models.ForeignKey("auth.User",on_delete=models.CASCADE,)
    issue_time = models.DateTimeField(default=timezone.now)
    initial_time = models.DateTimeField(default=datetime.datetime(2023, 1, 1, 0, 0, tzinfo=pytz.utc), help_text='Time at 21.5 Rs')
    longitude = models.FloatField(help_text="-180 degrees <= longitude cone axis <= 180 degrees, with 0 in the Earth direction ")
    latitude = models.FloatField(help_text="-60 degrees <= Co-latitude cone axis <= + 60 degrees")
    half_angle = models.FloatField(help_text=" 0 <= cone radius (half of the full angular width of the cone) <= 60 degrees")
    speed = models.FloatField(help_text="0 <= Radial velocity <= 3000 km/s")
    comment = models.CharField(max_length=1000, default='none', help_text ='Source/reference')
    def __str__(self):
        return self.cme_number
    def get_absolute_url(self):
        return reverse("cactus", kwargs={"pk": self.pk})


class Flare(models.Model):
    flare_number = models.CharField(max_length=200, default='none')
 #   author = models.ForeignKey("auth.User",on_delete=models.CASCADE,)
    issue_time = models.DateTimeField(default=datetime.datetime(2012,7,12,0,0, tzinfo=pytz.utc))
    alert_text = models.CharField(max_length=200, default='none')
    comment = models.CharField(max_length=1000, default='none', help_text='Source/reference')
    def __str__(self):
        return self.flare_number
    def get_absolute_url(self):
        return reverse("flarealert", kwargs={"pk": self.pk})


class Magnetogram(models.Model):
    magnetogram_number =  models.CharField(max_length=200, default='none')
    issue_time = models.DateTimeField(default=datetime.datetime(2023, 1, 1, 0, 0, tzinfo=pytz.utc))
    image = models.ImageField(upload_to='magnetograms/')
    comment = models.CharField(max_length=1000, default='none', help_text='Source/reference')
    def __str__(self):
        return self.magnetogram_number


class Spectrogram(models.Model):
    spectrogram_number = models.CharField(max_length=200, default='none')
    issue_time = models.DateTimeField(default=datetime.datetime(2023, 1, 1, 0, 0, tzinfo=pytz.utc))
    image = models.ImageField(upload_to='spectrograms/', blank=True)
    alert_text = models.CharField(max_length=200, default='none', blank=True)
    comment = models.CharField(max_length=1000, default='none', help_text='Source/reference')
    def __str__(self):
        return self.spectrogram_number