from django.db import models
from django.contrib.auth.models import User

# PUBLIC_INTERFACE
class Note(models.Model):
    """
    This model represents a note created by a user.
    """
    title = models.CharField(max_length=255, help_text="The title of the note")
    content = models.TextField(help_text="The detailed content of the note")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Timestamp when the note was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="Timestamp when the note was last updated")
    owner = models.ForeignKey(User, related_name='notes', on_delete=models.CASCADE, help_text="User who owns this note")

    def __str__(self):
        return f"{self.title} by {self.owner.username}"
