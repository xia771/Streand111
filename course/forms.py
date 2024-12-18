from django import forms
from .models import Course, Schedule, StudentCourse


class CourseForm(forms.ModelForm):

    class Meta:
        model = Course
        exclude = ['status', 'teacher']


class ScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule
        exclude = ["course"]


class ScoreForm(forms.ModelForm):
    class Meta:
        model = StudentCourse
        fields = ["student", "course", "scores", "comments"]

    student = forms.CharField(label="学生", disabled=True)
    # course = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    course = forms.CharField(label="课程", disabled=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initial['student'] = self.instance.student
        self.initial['course'] = self.instance.course

    def clean_student(self):
        return self.initial['student']

    def clean_course(self):
        return self.initial['course']


class RateForm(forms.ModelForm):
    class Meta:
        model = StudentCourse
        fields = ["course", "scores", "comments", "rating", "assessment"]

    course = forms.CharField(label="课程", disabled=True)
    scores = forms.IntegerField(label="成绩", disabled=True)
    comments = forms.CharField(label="老师评价", disabled=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initial['course'] = self.instance.course
        self.initial['scores'] = self.instance.scores
        self.initial['comments'] = self.instance.comments

    def clean_course(self):
        return self.initial['course']

    def clean_scores(self):
        return self.initial['scores']

    def clean_comments(self):
        return self.initial['comments']



# class BatchGradeForm(forms.Form):
#     scores = forms.DateField(label='学生评分', help_text='学生学号和分数的字典')
#
#     def __init__(self, *args, **kwargs):
#         super(BatchGradeForm, self).__init__(*args, **kwargs)
#         self.fields['scores'].widget.attrs.update({'class': 'form-control'})
#
# course/forms.py


# course/forms.py
from django import forms

class BatchGradeForm(forms.Form):
    student_scores = forms.CharField(
        label='学生成绩',
        widget=forms.Textarea(attrs={'placeholder': '请按照以下格式输入：学号1:分数1,学号2:分数2,...'}),
        help_text='请输入学号和分数，用逗号分隔多个学生'
    )
    comments = forms.CharField(
        label='评语',
        widget=forms.Textarea(attrs={'placeholder': '请输入统一评语（可选）'}),
        required=False
    )

    def clean_student_scores(self):
        data = self.cleaned_data['student_scores']
        scores = {}
        try:
            for item in data.split(','):
                if item.strip():
                    student_id, score = item.strip().split(':')
                    score = float(score)
                    if score < 0 or score > 100:
                        raise forms.ValidationError('分数必须在0-100之间')
                    scores[student_id.strip()] = score
        except ValueError:
            raise forms.ValidationError('格式错误，请使用正确的格式：学号1:分数1,学号2:分数2,...')
        return scores