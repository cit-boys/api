from django.urls import include, path
from rest_framework.routers import DefaultRouter

from src.mysalary import views

ROUTER = DefaultRouter()

ROUTER.register("companies", views.CompanyViewSet)

urlpatterns = path("", include(ROUTER.urls))
