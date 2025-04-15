from django.db import models

class TestResult(models.Model):
    user_id = models.CharField(max_length=255)
    test_id = models.IntegerField()
    question_id = models.IntegerField()
    question_type = models.CharField(max_length=10, null=True, blank=True)
    selected_answers = models.JSONField()
    correct_answers = models.JSONField()
    is_correct = models.BooleanField()
    is_partially_correct = models.BooleanField(default=False)
    points_earned = models.IntegerField()
    attempt_number = models.IntegerField()
    submitted = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user_id', 'test_id', 'question_id', 'attempt_number')
        indexes = [
            models.Index(fields=['user_id']),
            models.Index(fields=['test_id']),
            models.Index(fields=['question_id']),
            models.Index(fields=['attempt_number']),
            models.Index(fields=['submitted']),
        ]

    def __str__(self):
        status = 'Correct' if self.is_correct else 'Partially Correct' if self.is_partially_correct else 'Incorrect'
        return f"User {self.user_id} - Test {self.test_id} - Question {self.question_id} - Attempt {self.attempt_number} - {'Submitted' if self.submitted else 'Not Submitted'} - {status}"
