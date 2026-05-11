from data_quality.models import Dataset, DataRecord, AnomalyReport
from data_quality.ml.anomaly_detector import AnomalyDetector


def run_quality_check(dataset_id: int) -> AnomalyReport:
    """
    Main entry point for running a data quality check on a dataset.

    1. Fetches all DataRecords for the given dataset
    2. Runs ML anomaly detection
    3. Saves and returns an AnomalyReport
    """

    # Fetch dataset
    try:
        dataset = Dataset.objects.get(id=dataset_id)
    except Dataset.DoesNotExist:
        raise ValueError(f"Dataset with id {dataset_id} does not exist.")

    # Create a report in 'running' state
    report = AnomalyReport.objects.create(
        dataset=dataset,
        status='running'
    )

    try:
        # Fetch all records
        records_qs = DataRecord.objects.filter(dataset=dataset)

        if not records_qs.exists():
            report.status = 'failed'
            report.report_data = {"error": "No records found in dataset."}
            report.save()
            return report

        # Extract payload list
        records = [r.payload for r in records_qs]

        # Run detection
        detector = AnomalyDetector(contamination=0.1)
        result = detector.detect(records)

        # Save results to report
        report.status = 'completed'
        report.total_records = result['total_records']
        report.anomalies_found = result['anomalies_found']
        report.report_data = result
        report.save()

    except Exception as e:
        report.status = 'failed'
        report.report_data = {"error": str(e)}
        report.save()

    return report