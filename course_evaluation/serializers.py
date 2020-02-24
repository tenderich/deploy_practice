from rest_framework import serializers
from .models import Course, Evaluation


class CourseSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True, format="%Y-%m-%d %H:%M")
    updated_at = serializers.DateTimeField(read_only=True, format="%Y-%m-%d %H:%M")

    class Meta:
        model = Course
        fields = (
            "id",
            "course_code",
            "course_name",
            "course_professor",
            "course_semester",
            "created_at",
            "updated_at",
        )


class EvluationSerializer(serializers.ModelSerializer):
    course = CourseSerializer(read_only=True)
    created_at = serializers.DateTimeField(read_only=True, format="%Y-%m-%d %H:%M")
    updated_at = serializers.DateTimeField(read_only=True, format="%Y-%m-%d %H:%M")

    class Meta:
        model = Evaluation
        fields = (
            "id",
            "course",
            "grade",
            "review",
            "password",
            "created_at",
            "updated_at",
        )
