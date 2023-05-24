from django.contrib import admin
from .models.tank import CCT


class CCTAdmin(admin.ModelAdmin):

    """ CCT admin """


admin.site.register(CCT, CCTAdmin)
