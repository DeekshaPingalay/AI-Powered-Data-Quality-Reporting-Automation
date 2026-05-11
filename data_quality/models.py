from django.db import models


class Dataset(models.Model):
    """Represents an uploaded or registered dataset."""
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    source = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.name


class DataRecord(models.Model):
    """Individual data rows belonging to a dataset."""
    dataset = models.ForeignKey(
        Dataset, on_delete=models.CASCADE, related_name='records'
    )
    payload = models.JSONField()  # Flexible: stores any row as JSON
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Record {self.id} — {self.dataset.name}"


class AnomalyReport(models.Model):
    """Stores anomaly detection results for a dataset."""

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('running', 'Running'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]

    dataset = models.ForeignKey(
        Dataset, on_delete=models.CASCADE, related_name='anomaly_reports'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='pending'
    )
    total_records = models.IntegerField(default=0)
    anomalies_found = models.IntegerField(default=0)
    report_data = models.JSONField(default=dict)  # Full report as JSON

    def __str__(self):
        return f"Report [{self.status}] — {self.dataset.name} @ {self.created_at}"