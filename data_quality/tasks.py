from celery import shared_task
from django.utils import timezone


@shared_task(bind=True)
def run_quality_check_task(self, dataset_id: int):
    """
    Celery task to run anomaly detection on a single dataset.
    Can be triggered manually or on a schedule.
    """
    from data_quality.scripts.quality_checker import run_quality_check

    try:
        report = run_quality_check(dataset_id=dataset_id)
        return {
            "status": report.status,
            "dataset_id": dataset_id,
            "report_id": report.id,
            "anomalies_found": report.anomalies_found,
            "total_records": report.total_records
        }
    except Exception as e:
        # Retry up to 3 times on failure
        raise self.retry(exc=e, countdown=60, max_retries=3)


@shared_task
def run_all_quality_checks():
    """
    Scheduled task — runs quality checks on ALL datasets.
    Triggered automatically by Celery Beat on a schedule.
    """
    from data_quality.models import Dataset

    datasets = Dataset.objects.all()

    if not datasets.exists():
        return {"message": "No datasets found."}

    results = []
    for dataset in datasets:
        try:
            from data_quality.scripts.quality_checker import run_quality_check
            report = run_quality_check(dataset_id=dataset.id)
            results.append({
                "dataset_id": dataset.id,
                "dataset_name": dataset.name,
                "report_id": report.id,
                "status": report.status,
                "anomalies_found": report.anomalies_found
            })
        except Exception as e:
            results.append({
                "dataset_id": dataset.id,
                "dataset_name": dataset.name,
                "error": str(e)
            })

    return {
        "ran_at": timezone.now().isoformat(),
        "total_datasets": len(results),
        "results": results
    }