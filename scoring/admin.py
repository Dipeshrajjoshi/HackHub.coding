from django.contrib import admin
from .models import Score


@admin.register(Score)
class ScoreAdmin(admin.ModelAdmin):
    list_display = ['judge', 'submission', 'score', 'scored_at']
    list_filter = ['submission__contest']
    search_fields = ['judge__username', 'submission__participant__username']
    readonly_fields = ['scored_at']
