from django.db import models
from django.utils import timezone
from accounts.models import User

# the main model for our contests
class Contest(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    rules = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    # linking each contest to the user who created it (mostly organizers)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contests')
    is_published = models.BooleanField(default=False)
    # timestamps for when we created/modified the contest
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at'] # show newest contests first on the list

    # checking if the contest is running right now
    def is_active(self):
        now = timezone.now()
        return self.is_published and self.start_time <= now <= self.end_time

    # simple check to see if we missed the deadline
    def is_expired(self):
        return timezone.now() > self.end_time

    # check if the contest hasn't started yet
    def is_upcoming(self):
        return timezone.now() < self.start_time

    # helper to show a pretty status string in the UI
    def status(self):
        if not self.is_published:
            return 'Draft'
        if self.is_upcoming():
            return 'Upcoming'
        if self.is_active():
            return 'Active'
        return 'Ended'

    def __str__(self):
        return self.title


# links to leetcode/hackerrank for the actual coding problems
class ProblemLink(models.Model):
    PLATFORM_CHOICES = [
        ('leetcode', 'LeetCode'),
        ('hackerrank', 'HackerRank'),
        ('codeforces', 'Codeforces'),
        ('other', 'Other'),
    ]
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE, related_name='problem_links')
    title = models.CharField(max_length=200)
    url = models.URLField()
    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES, default='other')

    def __str__(self):
        return f"{self.title} ({self.get_platform_display()})"


# storing messages from the contact us form
class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name} ({self.email})"
