from rest_framework import serializers

from src.mysalary import models


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
        ]


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


# class SalaryInformationSerializer(serializers.BaseSerializer):
#     class ContributionsByLevelSerializer(serializers.BaseSerializer):


#     min_salary = serializers.FloatField()
#     max_salary = serializers.FloatField()
#     median_salary = serializers.FloatField()

#     contributions_by_level = ContributionsByLevelSerializer()
