from django.contrib.auth.models import AbstractUser
from django.db import models


# custom user model which lets us have different roles for organizers, participants, and judges
class User(AbstractUser):
    ROLE_CHOICES = [
        ('organizer', 'Organizer'),
        ('participant', 'Participant'),
        ('judge', 'Judge'),
    ]
    # default to participant if someone just signs up
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='participant')

    # helper methods to check the user's role across the app
    def is_organizer(self):
        return self.role == 'organizer'

    def is_participant(self):
        return self.role == 'participant'

    def is_judge(self):
        return self.role == 'judge'

    def __str__(self):
        # show the username and what their job is in the admin panel
        return f"{self.username} ({self.get_role_display()})"
