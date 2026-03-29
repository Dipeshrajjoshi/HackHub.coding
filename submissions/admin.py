from django.contrib import admin
from .models import Submission


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ['participant', 'contest', 'submission_type', 'submitted_at']
    list_filter = ['submission_type', 'contest']
    search_fields = ['participant__username', 'contest__title']
    readonly_fields = ['submitted_at']
