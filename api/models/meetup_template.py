from django.db import models


class MeetupTemplate(models.Model):
    name = models.CharField(max_length=128)
    prereqs = models.ManyToManyField("self", null=True)
    deleted = models.BooleanField(default=False)

    class Meta:
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['deleted'])
        ]

    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        super(MeetupTemplate, self).save(*args, **kwargs)