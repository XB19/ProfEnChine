from django.db import models


class Document(models.Model):
    prospect = models.ForeignKey(
        "conversations.ProspectProfile",
        on_delete=models.CASCADE,
        related_name="documents",
        null=True,
        blank=True,
        help_text="Prospect ayant envoyé ce document (passeport, casier, diplôme, photo...)",
    )
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to="documents/")
    content = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title