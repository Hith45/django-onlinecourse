from django.contrib import admin

from .models import (
    Course,
    Lesson,
    Instructor,
    Learner,
    Enrollment,
    Question,
    Choice,
    Submission,
)


class QuestionInline(admin.StackedInline):
    model = Question
    extra = 3


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3


class CourseAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]


class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]
    list_display = ('question_text', 'grade')


class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'course')


admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Instructor)
admin.site.register(Learner)
admin.site.register(Enrollment)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
admin.site.register(Submission)
