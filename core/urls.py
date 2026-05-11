from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from data_quality.views import dashboard

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('data_quality.urls')),
    path('dashboard/', dashboard, name='dashboard'),
    path('', RedirectView.as_view(url='/dashboard/', permanent=False)),
]