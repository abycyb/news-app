from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(UserProfile)
admin.site.register(News)
admin.site.register(Comment)
admin.site.register(Subcomment)
admin.site.register(Interacted_News)
admin.site.register(New_Comment)
admin.site.register(New_Subcomment)
