from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from data_quality.models import Dataset, DataRecord, AnomalyReport


class DatasetAPITest(TestCase):
    """Tests for Dataset API endpoints."""

    def setUp(self):
        self.client = APIClient()
        self.dataset = Dataset.objects.create(
            name="Test Dataset",
            source="test",
            description="Test dataset for unit tests"
        )

    def test_list_datasets(self):
        """GET /api/datasets/ should return 200."""
        response = self.client.get('/api/datasets/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_dataset(self):
        """POST /api/datasets/ should create a new dataset."""
        data = {
            "name": "New Dataset",
            "source": "test",
            "description": "Created in test"
        }
        response = self.client.post('/api/datasets/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], "New Dataset")

    def test_retrieve_dataset(self):
        """GET /api/datasets/{id}/ should return the dataset."""
        response = self.client.get(f'/api/datasets/{self.dataset.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "Test Dataset")


class DataRecordAPITest(TestCase):
    """Tests for DataRecord API endpoints."""

    def setUp(self):
        self.client = APIClient()
        self.dataset = Dataset.objects.create(
            name="Test Dataset",
            source="test"
        )

    def test_create_record(self):
        """POST /api/records/ should create a new record."""
        data = {
            "dataset": self.dataset.id,
            "payload": {"temperature": 22.0, "pressure": 101.0}
        }
        response = self.client.post('/api/records/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_records(self):
        """GET /api/records/ should return 200."""
        response = self.client.get('/api/records/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class AnomalyDetectionTest(TestCase):
    """Tests for ML anomaly detection logic."""

    def setUp(self):
        self.client = APIClient()
        self.dataset = Dataset.objects.create(
            name="ML Test Dataset",
            source="test"
        )
        # Add normal records
        normal_records = [
            {"temperature": 22.0, "pressure": 101.0, "humidity": 45.0},
            {"temperature": 23.0, "pressure": 102.0, "humidity": 46.0},
            {"temperature": 21.0, "pressure": 100.0, "humidity": 44.0},
            {"temperature": 24.0, "pressure": 103.0, "humidity": 47.0},
            {"temperature": 22.0, "pressure": 101.0, "humidity": 45.0},
            {"temperature": 23.0, "pressure": 102.0, "humidity": 46.0},
            {"temperature": 21.0, "pressure": 100.0, "humidity": 44.0},
            {"temperature": 24.0, "pressure": 103.0, "humidity": 47.0},
            {"temperature": 22.0, "pressure": 101.0, "humidity": 45.0},
        ]
        # Add outlier
        outlier = {"temperature": 999.0, "pressure": 5.0, "humidity": 200.0}

        for payload in normal_records + [outlier]:
            DataRecord.objects.create(
                dataset=self.dataset,
                payload=payload
            )

    def test_anomaly_detector_logic(self):
        """AnomalyDetector should flag the outlier record."""
        from data_quality.ml.anomaly_detector import AnomalyDetector
        records = list(
            DataRecord.objects.filter(
                dataset=self.dataset
            ).values_list('payload', flat=True)
        )
        detector = AnomalyDetector(contamination=0.1)
        result = detector.detect(records)
        self.assertEqual(result['total_records'], 10)
        self.assertGreater(result['anomalies_found'], 0)
        self.assertIn(9, result['anomaly_indices'])

    def test_run_check_endpoint(self):
        """POST /api/datasets/{id}/run-check/ should return a completed report."""
        response = self.client.post(
            f'/api/datasets/{self.dataset.id}/run-check/'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'completed')
        self.assertGreater(response.data['anomalies_found'], 0)