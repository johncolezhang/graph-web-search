from django.db import models
from django.db.models import TextField, CharField, DateTimeField, JSONField, AutoField

class labels(models.Model):
    label_id = AutoField(primary_key=True)
    label_tile = CharField(max_length=128, blank=True, null=True)
    label_sub_title = CharField(max_length=128, blank=True, null=True)
    label_content = CharField(max_length=256, blank=True, null=True)
    updated_time = DateTimeField(auto_now=True)
    add_time = DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.label_tile

    class Meta:
        db_table = "labels"
