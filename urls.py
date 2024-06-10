from django.urls import path
from .views import StartScrapingView, ScrapingStatusView

urlpatterns = [
    path('taskmanager/start_scraping/', StartScrapingView.as_view()),
    path('taskmanager/scraping_status/<int:job_id>/', ScrapingStatusView.as_view()),
]