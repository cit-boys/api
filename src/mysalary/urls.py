from django.urls import include, path
from rest_framework.routers import DefaultRouter

from src.mysalary import views

ROUTER = DefaultRouter()

ROUTER.register("companies", views.CompanyView)
ROUTER.register("levels", views.LevelView)
ROUTER.register("contributions", views.ContributionView)
ROUTER.register("certificates", views.CeritificateView)

urlpatterns = path("", include(ROUTER.urls))
