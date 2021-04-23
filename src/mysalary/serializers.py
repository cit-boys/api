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
    class Meta:
        model = models.Contribution
        fields = "__all__"


class CertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Contribution
        fields = "__all__"
