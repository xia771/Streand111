from django.db import models
import datetime
from user.models import Student, Teacher
from constants import COURSE_STATUS, COURSE_OPERATION


def current_year():
    return datetime.date.today().year


class Course(models.Model):
    credits = [
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
    ]
    semesters = [
        ("Autumn", "上"),
        ("Spring", "下")
    ]
    name = models.CharField(max_length=50, verbose_name="课程名")
    introduction = models.CharField(max_length=250, verbose_name="介绍")
    credit = models.IntegerField(verbose_name="学分")
    max_number = models.IntegerField(verbose_name="课程最大人数")

    year = models.IntegerField(verbose_name="年份", default=current_year)
    semester = models.CharField(max_length=20, verbose_name="学期", choices=semesters)

    # 未开始选课， 1
    # 开始选课，未结束选课 2
    # 结束选课， 3
    # 结课 4
    # 已打完分 5
    status = models.IntegerField(verbose_name="课程状态", default=1)

    teacher = models.ForeignKey(Teacher, verbose_name="课程教师", on_delete=models.CASCADE)

    def get_status_text(self):
        return COURSE_STATUS[self.status]

    def get_op_text(self):
        return COURSE_OPERATION[self.status]

    def get_current_count(self):
        courses = StudentCourse.objects.filter(course=self, with_draw=False)
        return len(courses)

    def get_schedules(self):
        schedules = Schedule.objects.filter(course=self)
        return schedules

    def __str__(self):
        return "%s (%s)" % (self.name, self.teacher.name)


def weekday_choices():
    weekday_str = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
    return [(i+1, weekday_str[i]) for i in range(7)]


class Schedule(models.Model):
    weekday = models.IntegerField(choices=weekday_choices(), verbose_name="日期")
    start_time = models.TimeField(verbose_name="上课时间")
    end_time = models.TimeField(verbose_name="下课时间")
    location = models.CharField(max_length=100, verbose_name="上课地点")
    remarks = models.CharField(max_length=100, verbose_name="备注", null=True, blank = True)

    start_week = models.IntegerField(verbose_name="第几周开始")
    end_week = models.IntegerField(verbose_name="第几周结束")

    intervals = [
        (1, "无间隔"),
        (2, "每隔一周上一次")
    ]
    week_interval = models.IntegerField(verbose_name="周间隔", choices=intervals, default=1)

    course = models.ForeignKey(Course, verbose_name="课程名", on_delete=models.CASCADE)

    def __str__(self):
        s = "第%s周-第%s周 " % (self.start_week, self.end_week)
        if self.week_interval == 2:
            s += "隔一周 "
        s += "%s %s-%s " % (self.get_weekday_display(), self.start_time.strftime("%H:%M"),
                            self.end_time.strftime("%H:%M"))
        s += "在%s" % self.location
        if self.remarks:
            s += " %s" % self.remarks
        return s


class StudentCourse(models.Model):
    RATING_CHOICES = [
        (5, '优秀 (5分)'),
        (4, '良好 (4分)'),
        (3, '一般 (3分)'),
        (2, '较差 (2分)'),
        (1, '差 (1分)'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    scores = models.FloatField(null=True)
    comments = models.TextField(null=True)
    rating = models.IntegerField(verbose_name="评分", choices=RATING_CHOICES, null=True)
    assessment = models.TextField(verbose_name="评价内容", null=True)
    is_anonymous = models.BooleanField(verbose_name="是否匿名", default=True)
    with_draw = models.BooleanField(default=False)
    with_draw_time = models.DateTimeField(null=True)
    evaluation_submitted = models.BooleanField(default=False)

    def get_display_rating(self):
        if self.rating is not None:
            return dict(self.RATING_CHOICES)[self.rating]
        return None

    def get_assessment_display(self):
        if not self.assessment:
            return None
        if self.is_anonymous:
            return f"匿名学生评价：{self.assessment}"
        return f"{self.student.name}的评价：{self.assessment}"
