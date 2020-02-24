from django.db import models


class TimeStampedModel(models.Model):

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Course(TimeStampedModel):
    course_code = models.CharField(max_length=15)
    course_name = models.CharField(max_length=30)
    course_professor = models.CharField(max_length=30)
    course_semester = models.CharField(max_length=10)

    def __str__(self):
        return "%s - %s : %s" % (self.course_code, self.course_name, self.id)


class Evaluation(TimeStampedModel):
    course = models.ForeignKey(Course, verbose_name="course", on_delete=models.CASCADE)
    grade = models.IntegerField()
    review = models.TextField()
    password = models.IntegerField(default=0000)

    def __str__(self):
        return self.review[:10]
