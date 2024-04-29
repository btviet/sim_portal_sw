from django.contrib import admin
from django.db import models
from .models import CME, Flare, Magnetogram, Spectrogram
from django.forms import TextInput, Textarea


class FlareAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.CharField: {'widget': Textarea(attrs={'rows':6, 'cols':40})},
    }
class CMEAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.CharField: {'widget': Textarea(attrs={'rows':6, 'cols':40})},
    }

class MagnetogramAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.CharField: {'widget': Textarea(attrs={'rows':6, 'cols':40})},
    }

class SpectrogramAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.CharField: {'widget': Textarea(attrs={'rows':6, 'cols':40})},
    }

admin.site.register(CME, CMEAdmin)
admin.site.register(Flare, FlareAdmin)
admin.site.register(Magnetogram, MagnetogramAdmin)
admin.site.register(Spectrogram, SpectrogramAdmin)