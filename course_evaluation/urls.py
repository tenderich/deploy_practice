from django.urls import path
from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path("search-course", views.search_course, name="search-course"),
    path(
        "create-course-evaluation/<int:course_id>",
        views.create_course_evaluation,
        name="create-course-evaluation",
    ),
    path(
        "fetch-course-evaluation/<int:course_id>",
        views.fetch_course_evaluation,
        name="fetch-course-evaluation",
    ),
    path(
        "update-course-evaluation/<int:evaluation_id>",
        views.update_course_evaluation,
        name="update-course-evaluation",
    ),
    path(
        "delete-course-evaluation/<int:evaluation_id>",
        views.delete_course_evaluation,
        name="delete-course-evluation",
    ),
]
