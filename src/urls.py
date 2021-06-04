from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from .mysalary.urls import urlpatterns as MYSALARY_URLS
from .mysalary.views import jobs

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "api/",
        include([MYSALARY_URLS, path("jobs/", jobs)]),
    ),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
