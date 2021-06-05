from decimal import Decimal

from django.db.models import Count, Max
from django.db.models.aggregates import Avg, Min
from rest_framework import status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework.settings import api_settings

from src import pagination
from src.mysalary import models, serializers

# Create your views here.
class CompanyView(viewsets.GenericViewSet):
    queryset = models.Company.objects
    serializer_class = serializers.CompanySerializer

    # CRUD functions

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def perform_create(self, serializer):
        serializer.save()

    def get_success_headers(self, data):
        try:
            return {"Location": str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, "_prefetched_objects_cache", None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()

    def partial_update(self, request, *args, **kwargs):
        kwargs["partial"] = True
        return self.update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()

    # other functions

    @action(methods=["GET"], detail=False, url_path="popular")
    def get_popular_companies(self, request):
        companies = models.Company.objects.annotate(
            num_contributions=Count("contribution")
        ).order_by("-num_contributions")

        popular = companies[0:4]
        unpopular = companies[5:]
        popular_companies_serializer = serializers.CompanyListSerializer(
            popular, many=True
        )

        return Response(
            {
                "popular": serializers.CompanyListSerializer(
                    companies[0:4], many=True
                ).data,
                "unpopular": serializers.CompanyListSerializer(
                    companies[5:], many=True
                ).data,
            }
        )


class LevelView(viewsets.GenericViewSet):
    queryset = models.Level.objects
    serializer_class = serializers.LevelSerializer

    # CRUD functions

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def perform_create(self, serializer):
        serializer.save()

    def get_success_headers(self, data):
        try:
            return {"Location": str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, "_prefetched_objects_cache", None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()

    def partial_update(self, request, *args, **kwargs):
        kwargs["partial"] = True
        return self.update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()

    # other functions

    def get_queryset(self):
        serializer = serializers.ContributionQuerySerializer(
            data=self.request.query_params
        )

        queryset = self.queryset
        if not serializer.is_valid():
            return queryset.all()

        if job_title := serializer.validated_data.get("job_title"):
            queryset = queryset.filter(job_title=job_title)

        if company_id := serializer.validated_data.get("company"):
            queryset = queryset.filter(company_id=company_id)

        return queryset.all()


class ContributionView(viewsets.GenericViewSet):
    queryset = models.Contribution.objects
    serializer_class = serializers.ContributionSerializer
    pagination_class = pagination.StandardResultsSetPagination

    def get_queryset(self):
        serializer = serializers.ContributionQuerySerializer(
            data=self.request.query_params
        )

        queryset = self.queryset
        if not serializer.is_valid():
            return queryset.all()

        if job_title := serializer.validated_data.get("job_title"):
            queryset = queryset.filter(job_title=job_title)

        if company_id := serializer.validated_data.get("company"):
            queryset = queryset.filter(company_id=company_id)

        if company_name := serializer.validated_data.get("company_name"):
            queryset = queryset.filter(company__short_name=company_name)

        if level := serializer.validated_data.get("level"):
            queryset = queryset.filter(level__name=level)

        return queryset.all()

    # CRUD functions

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def perform_create(self, serializer):
        serializer.save()

    def get_success_headers(self, data):
        try:
            return {"Location": str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, "_prefetched_objects_cache", None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()

    def partial_update(self, request, *args, **kwargs):
        kwargs["partial"] = True
        return self.update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()

    # other functions

    @action(methods=["GET"], detail=False, url_path="salaryinfo")
    def salary_info(self, request):
        queryset = self.get_queryset()

        serializer = serializers.ContributionQuerySerializer(
            data=self.request.query_params
        )

        if not serializer.is_valid(raise_exception=True):
            return Response("Query param is invalid")

        try:
            queryset[0]
        except IndexError:
            return Response(status=status.HTTP_200_OK)

        values = queryset.values_list("salary", flat=True).order_by("salary")

        min = queryset.aggregate(Min("salary"))["salary__min"] or 0.00
        max = queryset.aggregate(Max("salary"))["salary__max"] or 0.00

        contributions = queryset.count()
        if contributions % 2 == 1:
            median = values[contributions // 2]
        else:
            mid = contributions // 2
            median = values[mid + 1] + values[mid - 1]

        info = []

        queryset = (
            queryset.values("level__name")
            .annotate(count=Count("level"), salary=Avg("salary"), bonus=Avg("bonus"))
            .order_by("level__order")
        )

        for query in queryset:
            info.append(
                {
                    "level": query.get("level__name"),
                    "salary": query.get("salary"),
                    "bonus": query.get("bonus"),
                    "contributions": query.get("count"),
                }
            )

        sample = serializers.SampleSerializer(info, many=True)

        return Response(
            {
                "min": min,
                "max": max,
                "median": median or 0.00,
                "info": sample.data,
            },
            status=status.HTTP_200_OK,
        )

    @action(methods=["GET"], detail=False, url_path="contributiondetail")
    def contribution_job(self, request):
        queryset = self.get_queryset()

        serializer = serializers.ContributionQuerySerializer(
            data=self.request.query_params
        )

        if not serializer.is_valid(raise_exception=True):
            return Response("Query param is invalid")

        company = (
            models.Company.objects.get(
                id=serializer.validated_data.get("company")
            ).short_name,
        )

        return Response(
            {
                "level": serializer.validated_data.get("level"),
                "company": company,
                "salary": queryset.aggregate(Avg("salary"))["salary__avg"] or 0.00,
                "bonus": queryset.aggregate(Avg("bonus"))["bonus__avg"] or 0.00,
            },
            status=status.HTTP_200_OK,
        )

    @action(methods=["GET"], detail=False, url_path="company")
    def contribution_company(self, request):
        queryset = self.get_queryset()

        serializer = serializers.ContributionQuerySerializer(
            data=self.request.query_params
        )

        values = (
            queryset.values_list("job_title", flat=True)
            .order_by("job_title")
            .distinct()
        )

        company_id = queryset[0].company_id

        results = {}

        for value in values:
            temp = models.Contribution.objects.filter(
                company=company_id, job_title=value
            )
            results[value] = temp.values_list("salary", flat=True)

        finals = []

        for result in results:
            finals.append(
                {
                    "job_title": result,
                    "salaries": results[result],
                }
            )

        return Response(finals)

    @action(methods=["GET"], detail=False, url_path="description")
    def description_company(self, request):
        queryset = self.get_queryset()

        return Response(queryset[0].company.description, status=status.HTTP_200_OK)


class CeritificateView(viewsets.GenericViewSet):
    queryset = models.Certificate.objects
    serializer_class = serializers.CertificateSerializer

    # CRUD functions

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def perform_create(self, serializer):
        serializer.save()

    def get_success_headers(self, data):
        try:
            return {"Location": str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, "_prefetched_objects_cache", None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()

    def partial_update(self, request, *args, **kwargs):
        kwargs["partial"] = True
        return self.update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()

    # other functions


class DashboardView(viewsets.GenericViewSet):
    @action(methods=["GET"], detail=False, url_path="salaryinfo")
    def salary_info(self, request):
        # filtered by job_title and company

        queryset = self.get_queryset()

        serializer = serializers.ContributionQuerySerializer(
            data=self.request.query_params
        )

        if not serializer.is_valid(raise_exception=True):
            return Response("Query param is invalid")

        try:
            queryset[0]
        except IndexError:
            return Response(status=status.HTTP_200_OK)

        values = queryset.values_list("salary", flat=True).order_by("salary")

        min = queryset.aggregate(Min("salary"))["salary__min"] or 0.00
        max = queryset.aggregate(Max("salary"))["salary__max"] or 0.00

        contributions = queryset.count()
        if contributions % 2 == 1:
            median = values[contributions // 2]
        else:
            mid = contributions // 2
            median = values[mid + 1] + values[mid - 1]

        info = []

        queryset = (
            queryset.values("level__name")
            .annotate(count=Count("level"), salary=Avg("salary"), bonus=Avg("bonus"))
            .order_by("level__order")
        )

        for query in queryset:
            info.append(
                {
                    "level": query.get("level__name"),
                    "salary": query.get("salary"),
                    "bonus": query.get("bonus"),
                    "contributions": query.get("count"),
                }
            )

        sample = serializers.SampleSerializer(info, many=True)

        return Response(
            {
                "min": min,
                "max": max,
                "median": median or 0.00,
                "info": sample.data,
            },
            status=status.HTTP_200_OK,
        )

    @api_view(http_method_names=["GET"])
    def jobs(request):
        return Response(get_job_titles(), status=status.HTTP_200_OK)

    def get_job_titles():
        return set(
            models.Contribution.objects.all().values_list("job_title", flat=True)
        )

    @action(methods=["GET"], detail=False, url_path="company")
    def contribution_company(self, request):
        queryset = self.get_queryset()

        serializer = serializers.ContributionQuerySerializer(
            data=self.request.query_params
        )

        values = (
            queryset.values_list("job_title", flat=True)
            .order_by("job_title")
            .distinct()
        )

        company_id = queryset[0].company_id

        results = {}

        for value in values:
            temp = models.Contribution.objects.filter(
                company=company_id, job_title=value
            )
            results[value] = temp.values_list("salary", flat=True)

        finals = []

        for result in results:
            finals.append(
                {
                    "job_title": result,
                    "salaries": results[result],
                }
            )

        return Response(finals)


@api_view(http_method_names=["GET"])
def jobs(request):
    return Response(get_job_titles(), status=status.HTTP_200_OK)


def get_job_titles():
    return set(models.Contribution.objects.all().values_list("job_title", flat=True))
