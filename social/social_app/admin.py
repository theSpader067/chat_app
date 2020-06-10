from django.contrib import admin
from .models import message,profile,friendRequest,groups,groupProfile
# Register your models here.
admin.site.register(message)
admin.site.register(profile)
admin.site.register(friendRequest)
admin.site.register(groups)
admin.site.register(groupProfile)
