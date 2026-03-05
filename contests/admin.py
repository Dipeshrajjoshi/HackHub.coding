from django.contrib import admin
from .models import Contest, ProblemLink, ContactMessage


class ProblemLinkInline(admin.TabularInline):
    model = ProblemLink
    extra = 0


@admin.register(Contest)
class ContestAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_by', 'start_time', 'end_time', 'is_published', 'status']
    list_filter = ['is_published']
    search_fields = ['title']
    inlines = [ProblemLinkInline]

    def status(self, obj):
        return obj.status()
    status.short_description = 'Status'


@admin.register(ProblemLink)
class ProblemLinkAdmin(admin.ModelAdmin):
    list_display = ['title', 'contest', 'platform', 'url']
    list_filter = ['platform']


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_at')
    search_fields = ('name', 'email', 'message')
    readonly_fields = ('created_at',)
