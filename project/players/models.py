from typing import Any
from django.db import models
from abstract.models import AbstractBaseModel

class Player(AbstractBaseModel):
    name = models.CharField(max_length=100)
    score = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    def save(self, *args: tuple[Any, ...], **kwargs: dict[Any, Any]) -> None:
        """Override save method to set default values."""
        if not self.id:
            # Set default values for new players
            self.score = 0
        super().save(*args, **kwargs)

    def delete(self, *args: tuple[Any, ...], **kwargs: dict[Any, Any]) -> None:
        """Override delete method to perform soft delete."""
        super().delete(*args, **kwargs)

# Create your models here.
