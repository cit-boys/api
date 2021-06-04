from rest_framework import serializers

from src.mysalary import models

DEFAULT_DATETIME_FORMAT = "%m/%d/%Y %H:%M:%S"


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Company
        fields = "__all__"


class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Level
        fields = "__all__"


class ContributionSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source="company.short_name", read_only=True)
    company_id = serializers.PrimaryKeyRelatedField(
        write_only=True,
        source="company",
        queryset=models.Company.objects.all(),
    )

    class Meta:
        model = models.Contribution
        fields = "__all__"
        extra_kwargs = {
            "company": {
                "read_only": True,
            },
            "datetime_of_contribution": {
                "input_formats": (DEFAULT_DATETIME_FORMAT,),
                "format": DEFAULT_DATETIME_FORMAT,
            },
        }


class ContributionQuerySerializer(serializers.Serializer):
    job_title = serializers.CharField(required=False)
    company = serializers.IntegerField(required=False)
    company_name = serializers.CharField(required=False)
    level = serializers.CharField(required=False)


class CertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Contribution
        fields = "__all__"


class CompanyListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Company
        fields = "__all__"


class SampleSerializer(serializers.Serializer):
    level = serializers.CharField()
    salary = serializers.FloatField()
    bonus = serializers.FloatField()
    contributions = serializers.IntegerField()
