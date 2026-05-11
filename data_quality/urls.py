from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    DatasetViewSet,
    DataRecordViewSet,
    AnomalyReportViewSet,
    CSVUploadView          # ADD THIS
)

router = DefaultRouter()
router.register(r'datasets', DatasetViewSet)
router.register(r'records', DataRecordViewSet)
router.register(r'reports', AnomalyReportViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('upload-csv/', CSVUploadView.as_view(), name='upload-csv'),  # ADD THIS
]