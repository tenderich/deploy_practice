import math
from django.shortcuts import render, redirect

# from django.core.paginator import Paginator
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

from .models import Course, Evaluation
from .serializers import CourseSerializer, EvluationSerializer


@api_view(["GET"])
@permission_classes([AllowAny])
def home(request):
    course = Course.objects.all()
    return render(request, "course.html", {"course": course})


@api_view(["POST"])
@permission_classes([AllowAny])
def search_course(request):
    course_code = request.data.get("course_code", "")
    course_name = request.data.get("course_name", "")
    course_professor = request.data.get("course_professor", "")
    course_semester = request.data.get("course_semester", "")

    msg = "search"

    course = Course.objects.all()
    if course_code != "":
        course = course.filter(course_code__contains=course_code)
    if course_name != "":
        course = course.filter(course_name__contains=course_name)
    if course_professor != "":
        course = course.filter(course_professor__contains=course_professor)
    if course_semester != "":
        course = course.filter(course_semester__contains=course_semester)

    course = CourseSerializer(course, many=True).data
    return render(request, "course.html", {"course": course, "search": msg,},)
    # return Response(course, status=200)


# 강의평가 만들기
@api_view(["POST"])
@permission_classes([AllowAny])
def create_course_evaluation(request, course_id):
    try:
        course = Course.objects.get(id=course_id)
    except Course.DoesNotExist:
        return Response({"message": "no such objects"}, status=404)

    review = request.data.get("review", "")
    grade = request.data.get("grade", 3)
    password = int(request.data.get("password", 0000))

    evaluation = Evaluation.objects.create(
        course=course, grade=grade, review=review, password=password
    )
    evaluation = EvluationSerializer(evaluation).data
    return Response(evaluation, status=200)
    # return redirect("/course-evaluation/" + str(course.id))


# 강의평가 불러오기
@api_view(["GET"])
@permission_classes([AllowAny])
def fetch_course_evaluation(request, course_id):
    try:
        course = Course.objects.get(id=course_id)
    except Course.DoesNotExist:
        return Response({"message": "no such objects"}, status=404)

    evaluation = Evaluation.objects.filter(course=course).order_by("id")
    print(course.id)
    course = CourseSerializer(course).data
    evaluation = EvluationSerializer(evaluation, many=True).data
    # return Response(evaluation, status=200)
    return render(request, "detail.html", {"course": course, "evaluation": evaluation},)


# 강의평가 수정하기
@api_view(["PUT"])
@permission_classes([AllowAny])
def update_course_evaluation(request, evaluation_id):
    password = request.data.get("password")
    grade = request.data.get("grade")
    review = request.data.get("review", "")
    if password == "":
        password = -1
    else:
        password = int(password)

    if grade == "":
        grade = -1
    else:
        grade = int(grade)

    try:
        evaluation = Evaluation.objects.get(id=evaluation_id)
    except Evaluation.DoesNotExist:
        return Response({"message": "no such objects"}, status=404)

    if password == evaluation.password:  # 비밀번호 확인후 맞으면 실행
        evaluation.grade = grade
        evaluation.review = review
        evaluation.save()
        evaluation = EvluationSerializer(evaluation).data
        return Response(
            {"message": "evaluation updated", "evaluation": evaluation}, status=200
        )
        # return redirect("/course-evaluation/" + str(evaluation.course.id))

    else:
        return Response({"message": "permission denied"}, status=400)


# 강의평가 삭제하기
@api_view(["DELETE"])
@permission_classes([AllowAny])
def delete_course_evaluation(request, evaluation_id):
    password = request.data.get("password")

    if password == "":
        password = -1
    else:
        password = int(password)

    try:
        evaluation = Evaluation.objects.get(id=evaluation_id)
    except Evaluation.DoesNotExist:
        return Response({"message": "no such objects"}, status=404)

    if password == evaluation.password:
        evaluation.delete()
        # return Response({"message": "evaluation deleted"}, status=200)
        return redirect("/fetch-course-evaluation/" + str(evaluation.course.id))
    else:
        return Response({"message": "permission denide"}, status=400)

