from decimal import Decimal

from django.db.models import Count, Max
from django.db.models.aggregates import Avg, Min
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from src import pagination

from src.mysalary import models, serializers

# Create your views here.


class CompanyViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = models.Company.objects
    serializer_class = serializers.CompanySerializer

    @action(methods=["GET"], detail=False, url_path="popular")
    def get_by_popularity(self, request):
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


class LevelViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = models.Level.objects
    serializer_class = serializers.LevelSerializer

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


class CompensationViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = models.Compensation.objects
    serializer_class = serializers.CompensationSerializer

    def get_queryset(self):
        serializer = serializers.CompensationQuerySerializer(
            data=self.request.query_params
        )

        queryset = self.queryset
        if not serializer.is_valid():
            return queryset.all()

        if company_id := serializer.validated_data.get("company"):
            queryset = queryset.filter(company_id=company_id)

        return queryset.all()


class ContributionViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
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

    @action(methods=["GET"], detail=False, url_path="salaryinfo")
    def salary_info(self, request):
        queryset = self.get_queryset()

        serializer = serializers.ContributionQuerySerializer(
            data=self.request.query_params
        )

        if not serializer.is_valid(raise_exception=True):
            return Response("Query param is invalid")

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
    def contribution_detail(self, request):
        queryset = self.get_queryset()

        serializer = serializers.ContributionQuerySerializer(
            data=self.request.query_params
        )

        if not serializer.is_valid(raise_exception=True):
            return Response("Query param is invalid")

        return Response(
            {
                "level": serializer.validated_data.get("level"),
                "company": models.Company.objects.get(
                    id=serializer.validated_data.get("company")
                ).short_name,
                "salary": queryset.aggregate(Avg("salary"))["salary__avg"] or 0.00,
                "bonus": queryset.aggregate(Avg("bonus"))["bonus__avg"] or 0.00,
            },
            status=status.HTTP_200_OK,
        )

    @action(methods=["GET"], detail=False, url_path="company")
    def company_contribution(self, request):
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


class CeritificateViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = models.Certificate.objects
    serializer_class = serializers.CertificateSerializer


@api_view(http_method_names=["GET"])
def jobs(request):
    return Response(get_job_titles(), status=status.HTTP_200_OK)


def get_job_titles():
    return set(models.Contribution.objects.all().values_list("job_title", flat=True))
