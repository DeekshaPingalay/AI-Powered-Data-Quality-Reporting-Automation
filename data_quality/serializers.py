from rest_framework import serializers
from .models import Dataset, DataRecord, AnomalyReport


class DataRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataRecord
        fields = ['id', 'dataset', 'payload', 'created_at']


class DatasetSerializer(serializers.ModelSerializer):
    records = DataRecordSerializer(many=True, read_only=True)

    class Meta:
        model = Dataset
        fields = ['id', 'name', 'description', 'source', 'uploaded_at', 'records']


class AnomalyReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnomalyReport
        fields = [
            'id', 'dataset', 'created_at', 'status',
            'total_records', 'anomalies_found', 'report_data'
        ]