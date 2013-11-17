from django.contrib import admin
from app.models import Message, Person, Relationship

class MessageAdmin(admin.ModelAdmin):
    list_display = ('title', 'text', 'author', 'date', )
    search_fields = ('title', )

admin.site.register(Message, MessageAdmin)

class RelationshipInline(admin.StackedInline):
    model = Relationship
    fk_name = 'from_person'

class PersonAdmin(admin.ModelAdmin):
    inlines = [RelationshipInline]

admin.site.register(Person, PersonAdmin)