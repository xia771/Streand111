from django.views.generic.edit import DeleteView, CreateView, UpdateView
from django.views.generic.detail import DetailView
from django.shortcuts import render, reverse, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .models import Schedule, StudentCourse
from .forms import ScoreForm, RateForm
from user.util import get_user


class ScheduleDeleteView(DeleteView):
    model = Schedule


class ScoreUpdateView(UpdateView):
    model = StudentCourse
    form_class = ScoreForm
    template_name = 'course/teacher/score.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        title = "给分"
        if request.GET.get("update"):
            title = "修改成绩"

        info = {}
        return_url = reverse("course", kwargs={"kind": "teacher"})
        if self.object:
            teacher = self.object.course.teacher
            info = {
                "name": teacher.name,
                "kind": "teacher",
            }
            return_url = reverse("view_detail", kwargs={"course_id": self.object.course.id})

        return self.render_to_response(self.get_context_data(info=info, title=title, return_url=return_url))

    def get_success_url(self):
        if self.object:
            return reverse("view_detail", kwargs={"course_id": self.object.course.id})
        else:
            return reverse("course", kwargs={"kind": "teacher"})


class RateUpdateView(UpdateView):
    model = StudentCourse
    fields = ['rating', 'assessment', 'is_anonymous']
    template_name = 'course/student/rating.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student = self.object.student
        context['info'] = {
            "name": student.name,
            "kind": "student",
        }
        context['return_url'] = reverse("view_course", kwargs={"view_kind": "is_end"})
        return context

    def get(self, request, *args, **kwargs):
        user = get_user(request, "student")
        if not user:
            return redirect(reverse("login", kwargs={"kind": "student"}))
        self.object = self.get_object()
        return self.render_to_response(self.get_context_data())

    def get_success_url(self):
        return reverse("view_course", kwargs={"view_kind": "is_end"})

    def form_valid(self, form):
        if form.cleaned_data['rating'] is None:
            form.add_error('rating', '请选择评分')
            return self.form_invalid(form)
        form.instance.evaluation_submitted = True
        return super().form_valid(form)


class StudentCourseDetailView(DetailView):
    model = StudentCourse
    template_name = 'course/student/course.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        if self.object:
            context["info"] = {
                "name": self.object.student.name,
                "kind": "student",
            }
        return self.render_to_response(context)
