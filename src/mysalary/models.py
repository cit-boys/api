from django.db import models

from src.constants import DEFAULT_MAX_LENGTH, MEDIUM_TEXT_MAX_LENGTH
from src.mysalary.choices import AcademicLevel, Gender

# Create your models here.


class Company(models.Model):
    name = models.CharField(max_length=DEFAULT_MAX_LENGTH)
    location = models.CharField(max_length=MEDIUM_TEXT_MAX_LENGTH)

    class Meta:
        verbose_name_plural = "Companies"


class Level(models.Model):
    name = models.CharField(max_length=DEFAULT_MAX_LENGTH)

    # Foreign Keys
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    order = models.PositiveIntegerField()


class Compensation(models.Model):
    salary = models.DecimalField(max_digits=9, decimal_places=2)

    # Foreign Keys
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    salary = models.FloatField()


class Contribution(models.Model):
    job_title = models.CharField(max_length=DEFAULT_MAX_LENGTH)
    years_of_experience = models.PositiveIntegerField()
    years_at_company = models.PositiveIntegerField()
    salary = models.DecimalField(max_digits=9, decimal_places=2)
    bonus = models.DecimalField(max_digits=9, decimal_places=2)
    gender = models.CharField(max_length=1, choices=Gender.choices)
    highest_academic_level_attained = models.CharField(
        max_length=1, choices=AcademicLevel.choices
    )
    datetime_of_contribution = models.DateTimeField(
        null=True, blank=True, auto_now_add=True
    )

    # Foreign Keys
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    level = models.ForeignKey(Level, on_delete=models.CASCADE)


class Certificate(models.Model):
    certificate_name = models.CharField(max_length=MEDIUM_TEXT_MAX_LENGTH)

    # Foreign Keys
    compensation = models.ForeignKey(Compensation, on_delete=models.CASCADE)
