from django.urls import include, path
from rest_framework.routers import DefaultRouter

from src.mysalary import views

ROUTER = DefaultRouter()

ROUTER.register("companies", views.CompanyViewSet)
ROUTER.register("levels", views.LevelViewSet)
ROUTER.register("compensations", views.CompensationViewSet)
ROUTER.register("contributions", views.ContributionViewSet)
ROUTER.register("certificates", views.CeritificateViewSet)

urlpatterns = path("", include(ROUTER.urls))
