from django.db import models
from django.utils import timezone
from accounts.models import User
from contests.models import Contest
from django.core.exceptions import ValidationError
import os


# helper to make sure users don't upload weird files (like .exe)
def validate_file_extension(value):
    ext = os.path.splitext(value.name)[1]
    # we allow common document, image, and source code formats
    valid_extensions = [
        '.zip', '.pdf', '.doc', '.docx', 
        '.png', '.jpg', '.jpeg',
        '.py', '.js', '.java', '.cpp', '.c', '.h', '.html', '.css', '.ts', '.go', '.rs', '.php', '.rb'
    ]
    if not ext.lower() in valid_extensions:
        raise ValidationError(f'Unsupported file extension ({ext}). Please upload ZIP, PDF, or common source code files.')


# checking the file size so we don't crash the server with huge uploads
def validate_file_size(value):
    filesize = value.size
    # 10MB is plenty for code or a single document/image
    if filesize > 10 * 1024 * 1024:
        raise ValidationError("The maximum file size that can be uploaded is 10MB")


# the main model that stores all the user solutions and entries
class Submission(models.Model):
    SUBMISSION_TYPE_CHOICES = [
        ('code', 'Code File'),
        ('document', 'Document'),
        ('image', 'Image'),
        ('zip', 'ZIP File'),
        ('github', 'GitHub Repository'),
    ]
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE, related_name='submissions')
    participant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='submissions')
    title = models.CharField(max_length=200, default="Untitled Submission")
    description = models.TextField(blank=True)
    submission_type = models.CharField(max_length=20, choices=SUBMISSION_TYPE_CHOICES)

    # file field with our custom size and extension validators attached
    file = models.FileField(upload_to='submissions/files/', null=True, blank=True, validators=[validate_file_extension, validate_file_size])
    
    # separate field specifically for images so judges can see them directly in the browser
    image = models.ImageField(upload_to='submissions/images/', null=True, blank=True, validators=[validate_file_size])
    
    # field for a link to a github repo or an external portfolio
    external_link = models.URLField(null=True, blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # standard constraint: one submission per person per contest to keep it fair
        unique_together = ('contest', 'participant')
        ordering = ['-submitted_at']

    def __str__(self):
        # looks good in the django admin panel: "user_a -> Sample Contest"
        return f"{self.participant.username} -> {self.contest.title}"
