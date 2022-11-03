from django.contrib import admin
from .models import Config


class ConfigA(admin.ModelAdmin):
    exclude = ('users',)
    list_display = ('name', 'ip', 'udp', 'community')


admin.site.register(Config, ConfigA)
admin.site.site_header = "TrapMessage Admin"
