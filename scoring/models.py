from django.db import models
from accounts.models import User
from submissions.models import Submission


# the model for judges to give scores and feedback to participants
class Score(models.Model):
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE, related_name='scores')
    judge = models.ForeignKey(User, on_delete=models.CASCADE, related_name='scores_given')
    score = models.FloatField()
    feedback = models.TextField(blank=True, null=True)
    scored_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # standard rule: one judge can only score a submission once
        unique_together = ('submission', 'judge')
        ordering = ['-scored_at']

    # validation to keep the score in a reasonable range (0-100)
    def clean(self):
        from django.core.exceptions import ValidationError
        if self.score < 0 or self.score > 100:
            raise ValidationError('Score must be between 0 and 100.')

    def __str__(self):
        # looks good in the admin panel: "judge_1 -> participant_a = 95.0"
        return f"{self.judge.username} -> {self.submission} = {self.score}"
