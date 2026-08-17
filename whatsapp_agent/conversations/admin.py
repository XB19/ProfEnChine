from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Conversation, ProspectProfile


admin.site.register(Conversation)
admin.site.register(ProspectProfile)