from django.db import models
from django.db.models import DO_NOTHING

from api.models.learning_modality import LearningModality
from api.models.person import Person
from api.models.topic import Topic


class PreferredModality(models.Model):
    person = models.ForeignKey(Person, on_delete=DO_NOTHING)
    topic = models.ForeignKey(Topic, on_delete=DO_NOTHING)
    learning_modality = models.ForeignKey(LearningModality, null=True, on_delete=DO_NOTHING)

    class Meta:
        indexes = [
            models.Index(fields=['person_id', 'topic_id', 'learning_modality_id'])
        ]