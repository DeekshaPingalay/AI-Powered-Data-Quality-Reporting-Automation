from django.contrib import admin
from .models import Dataset, DataRecord, AnomalyReport


@admin.register(Dataset)
class DatasetAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'source', 'uploaded_at']
    search_fields = ['name', 'source']


@admin.register(DataRecord)
class DataRecordAdmin(admin.ModelAdmin):
    list_display = ['id', 'dataset', 'created_at']
    list_filter = ['dataset']


@admin.register(AnomalyReport)
class AnomalyReportAdmin(admin.ModelAdmin):
    list_display = ['id', 'dataset', 'status', 'total_records', 'anomalies_found', 'created_at']
    list_filter = ['status']