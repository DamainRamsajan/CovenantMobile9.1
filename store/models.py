from django.db import models

class Document(models.Model):
    id = models.CharField(primary_key=True, max_length=64)
    title = models.CharField(max_length=512, blank=True)
    content = models.TextField(blank=True)
    policy_tags = models.CharField(max_length=512, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "documents"

    def __str__(self):
        return self.title or self.id

class Vector(models.Model):
    id = models.CharField(primary_key=True, max_length=64)
    doc = models.ForeignKey(Document, on_delete=models.CASCADE, related_name="vectors")
    embedding = models.BinaryField()
    dim = models.IntegerField()
    model = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "vectors"

class ProvenanceLog(models.Model):
    run_id = models.CharField(max_length=64)
    step_no = models.IntegerField()
    actor = models.CharField(max_length=128)
    action = models.CharField(max_length=128)
    input_hash = models.CharField(max_length=128, blank=True)
    output_hash = models.CharField(max_length=128, blank=True)
    policy_decision = models.CharField(max_length=128, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    prev_hash = models.CharField(max_length=128, blank=True)

    class Meta:
        db_table = "provenance_log"
        unique_together = (("run_id", "step_no"),)

