from django.contrib import admin
from app.models import Message

class MessageAdmin(admin.ModelAdmin):
    list_display = ('title', 'text', 'author', 'date', )
    search_fields = ('title', )

admin.site.register(Message, MessageAdmin)