from django.db.models import (
    Model,
    CharField,
    TextField,
    BooleanField,
    DateTimeField,
    PositiveSmallIntegerField,
    ForeignKey,
    CASCADE,
    DecimalField
)
 
from django.core.validators import MaxValueValidator


from authorization.models import CustomUser


class Course(Model):
    title = CharField(max_length=255)
    description = TextField(blank=True, null=True)
    is_active = BooleanField(default=True)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    owner = ForeignKey(to=CustomUser, on_delete=CASCADE, related_name="owned_courses")
    deleted_at = DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "courses"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title
    
class Lesson(Model):
    title = CharField(max_length=255)
    content = TextField(blank=True, null=True)
    course = ForeignKey(to=Course, on_delete=CASCADE, related_name="lessons")
    is_published = BooleanField(default=False)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    deleted_at = DateTimeField(null=True, blank=True)
    order = DecimalField(max_digits=10, decimal_places=2, default=0)
    indentation = PositiveSmallIntegerField(default=0, validators=[MaxValueValidator(5)])

    class Meta:
        db_table = "lessons"
        ordering = ["order"]

    def __str__(self):
        return self.title

