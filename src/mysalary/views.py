from django.db.models import Count
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

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
        ).order_by("num_contributions")

        popular_companies_serializer = serializers.CompanyListSerializer(
            companies, many=True
        )

        return Response(popular_companies_serializer.data)


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

    def get_queryset(self):
        serializer = serializers.ContributionQuerySerializer(
            data=self.request.query_params
        )

        queryset = self.queryset
        if not serializer.is_valid(raise_exception=True):
            return queryset.all()

        if job_title := serializer.validated_data.get("job_title"):
            queryset = queryset.filter(job_title=job_title)

        if company_id := serializer.validated_data.get("company_id"):
            queryset = queryset.filter(company_id=company_id)

        return queryset.all()

    @action(methods=["GET"], detail=False, url_path="salaryinfo")
    def salary_info(self, request):

        queryset = self.get_queryset()

        print(queryset.values_list("salary"))

        return Response(
            {
                "min": 0.0,
                "max": 0.0,
                "median": 0,
                "info": [
                    {"level": "asd", "contributions": 2},
                ],
            },
            status=status.HTTP_200_OK,
        )


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
