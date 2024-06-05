from django.contrib import admin
from .models.tank import CCT
from .models.event import Event


class CCTAdmin(admin.ModelAdmin):

    """ CCT admin """


class EventAdmin(admin.ModelAdmin):

    """ Event admin """


admin.site.register(CCT, CCTAdmin)
admin.site.register(Event, EventAdmin)
