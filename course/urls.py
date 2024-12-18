from django.contrib import admin
from django.urls import path, include
from course.views import *
from course.cbvs import ScheduleDeleteView, ScoreUpdateView, RateUpdateView, StudentCourseDetailView

urlpatterns = [
    path('', to_home, name="course"),
    path('<slug:kind>/', home, name="course"),
    path('teacher/create_course', create_course, name="create_course"),
    path('teacher/view_detail/<int:course_id>', view_detail, name="view_detail"),
    path('teacher/create_schedule/<int:course_id>', create_schedule, name="create_schedule"),
    path('teacher/delete_schedule/<int:schedule_id>', delete_schedule, name="delete_schedule"),
    path('teacher/score/<int:pk>', ScoreUpdateView.as_view(), name="score"),
    path('teacher/batch_grade/<int:course_id>', batch_grade, name="batch_grade"),
    path('teacher/handle_course/<int:course_id>/<int:handle_kind>', handle_course, name="handle_course"),

    path('student/view/<slug:view_kind>', view_course, name="view_course"),
    path('student/operate/<int:course_id>/<slug:operate_kind>', operate_course, name="operate_course"),

    path('student/evaluate/<int:pk>', RateUpdateView.as_view(), name="evaluate"),
    path('student/view_detail/<int:pk>', StudentCourseDetailView.as_view(), name="sview_detail"),
]
