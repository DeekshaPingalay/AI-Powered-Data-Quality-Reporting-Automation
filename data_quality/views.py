import csv
import io

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from django.shortcuts import render
from .models import Dataset, DataRecord, AnomalyReport
from .serializers import DatasetSerializer, DataRecordSerializer, AnomalyReportSerializer
from .scripts.quality_checker import run_quality_check
from .tasks import run_quality_check_task


class DatasetViewSet(viewsets.ModelViewSet):
    """CRUD API for Datasets."""
    queryset = Dataset.objects.all().order_by('-uploaded_at')
    serializer_class = DatasetSerializer

    @action(detail=True, methods=['post'], url_path='run-check')
    def run_check(self, request, pk=None):
        """
        POST /api/datasets/{id}/run-check/
        Triggers a synchronous ML anomaly detection run on the dataset.
        """
        try:
            report = run_quality_check(dataset_id=int(pk))
            serializer = AnomalyReportSerializer(report)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=True, methods=['post'], url_path='run-check-async')
    def run_check_async(self, request, pk=None):
        """
        POST /api/datasets/{id}/run-check-async/
        Triggers anomaly detection as a background Celery task.
        Returns immediately with a task ID.
        """
        try:
            task = run_quality_check_task.delay(dataset_id=int(pk))
            return Response({
                "message": "Quality check started in background.",
                "task_id": task.id,
                "dataset_id": int(pk)
            }, status=status.HTTP_202_ACCEPTED)
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class DataRecordViewSet(viewsets.ModelViewSet):
    """CRUD API for Data Records."""
    queryset = DataRecord.objects.all().order_by('-created_at')
    serializer_class = DataRecordSerializer


class AnomalyReportViewSet(viewsets.ModelViewSet):
    """CRUD API for Anomaly Reports."""
    queryset = AnomalyReport.objects.all().order_by('-created_at')
    serializer_class = AnomalyReportSerializer


class CSVUploadView(APIView):
    """
    POST /api/upload-csv/
    Upload a CSV file to auto-create a Dataset and its DataRecords.
    """
    parser_classes = [MultiPartParser]

    def post(self, request):
        file = request.FILES.get('file')
        name = request.data.get('name', 'Unnamed Dataset')
        source = request.data.get('source', 'csv_upload')

        if not file:
            return Response(
                {"error": "No file provided."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not file.name.endswith('.csv'):
            return Response(
                {"error": "Only CSV files are supported."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            decoded = file.read().decode('utf-8')
            reader = csv.DictReader(io.StringIO(decoded))
            rows = list(reader)

            if not rows:
                return Response(
                    {"error": "CSV file is empty."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            def convert_row(row):
                converted = {}
                for key, value in row.items():
                    try:
                        converted[key] = float(value)
                    except (ValueError, TypeError):
                        converted[key] = value
                return converted

            dataset = Dataset.objects.create(
                name=name,
                source=source,
                description=f"Uploaded via CSV — {file.name}"
            )

            records = [
                DataRecord(dataset=dataset, payload=convert_row(row))
                for row in rows
            ]
            DataRecord.objects.bulk_create(records)

            return Response({
                "message": "Dataset created successfully.",
                "dataset_id": dataset.id,
                "dataset_name": dataset.name,
                "records_created": len(records)
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
def dashboard(request):
    """Render the main dashboard page."""
    return render(request, 'dashboard.html')