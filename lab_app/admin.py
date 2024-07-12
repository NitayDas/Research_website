from django.contrib import admin
from .models import BannerImage, PeopleProfile, Publication, PeopleCategory

# Register your models here.
admin.site.register(BannerImage)
admin.site.register(PeopleProfile)
admin.site.register(Publication)
admin.site.register(PeopleCategory)