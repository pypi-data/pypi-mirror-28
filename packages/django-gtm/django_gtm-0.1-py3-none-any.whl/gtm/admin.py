from django.contrib import admin

from . models import GTMDefault, GTMSettings


admin.site.register(GTMDefault)
admin.site.register(GTMSettings)
