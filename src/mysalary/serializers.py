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


class CompensationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Compensation
        fields = "__all__"


class ContributionSerializer(serializers.ModelSerializer):
    class CompanyNameSerializer(serializers.ModelSerializer):
        class Meta:
            model = models.Company
            fields = ["name"]

    company = CompanyNameSerializer(read_only=True)

    class Meta:
        model = models.Contribution
        fields = [
            "company",
            "years_of_experience",
            "datetime_of_contribution",
            "salary",
            "job_title",
        ]
        extra_kwargs = {
            "datetime_of_contribution": {
                "input_formats": (DEFAULT_DATETIME_FORMAT,),
                "format": DEFAULT_DATETIME_FORMAT,
            }
        }


class ContributionQuerySerializer(serializers.Serializer):
    job_title = serializers.CharField(required=False)
    company = serializers.IntegerField(required=False)


class CertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Contribution
        fields = "__all__"


class CompanyListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Company
        fields = ["name"]
