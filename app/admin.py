from django.contrib import admin
from app import models

# Register your models here.

admin.site.register(models.Language)
admin.site.register(models.Country)
admin.site.register(models.Tour)
admin.site.register(models.TourEvent)
admin.site.register(models.Menu)
admin.site.register(models.Blog)
admin.site.register(models.Gallery)
admin.site.register(models.PeopleSay)
admin.site.register(models.Destination)
admin.site.register(models.TourType)
admin.site.register(models.About)
admin.site.register(models.BlogTag)

