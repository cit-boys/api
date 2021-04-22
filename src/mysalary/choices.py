from django.db.models import TextChoices


class Gender(TextChoices):
    MALE = ("M", "Male")
    FEMALE = ("F", "Female")
    OTHERS = ("O", "Others")

class AcademicLevel(TextChoices):
    NONE = ("N", "None")
    GRADE_SCHOOL = ("G", "Grade School")
    HIGH_SCHOOL = ("H", "High School")
    ASSOCIATE_DEGREE = ("A", "Associate Degree")
    BACHELORS_DEGREE = ("B", "Bachelor's Degree")
    MASTERS_DEGREE = ("M", "Master's Degree")
    DOCTORATE = ("D", "Doctorate")