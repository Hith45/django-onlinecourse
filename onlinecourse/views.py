from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Course, Enrollment, Question, Choice, Submission


def course_details(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    return render(request, 'onlinecourse/course_details_bootstrap.html', {'course': course})


def submit(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    user = request.user
    enrollment = Enrollment.objects.get(user=user, course=course)
    submission = Submission.objects.create(enrollment=enrollment)

    selected_choices = []
    for key, value in request.POST.items():
        if key.startswith('choice_'):
            selected_choices.append(int(value))

    submission.choices.set(Choice.objects.filter(id__in=selected_choices))
    submission_id = submission.id

    return HttpResponseRedirect(
        reverse('onlinecourse:show_exam_result', args=(course_id, submission_id))
    )


def show_exam_result(request, course_id, submission_id):
    course = get_object_or_404(Course, pk=course_id)
    submission = get_object_or_404(Submission, id=submission_id)

    choices = submission.choices.all()
    selected_ids = list(choices.values_list('id', flat=True))

    total_score = 0
    questions = course.question_set.all()
    maximum_score = sum(question.grade for question in questions)

    for question in questions:
        question_selected_ids = choices.filter(
            question=question
        ).values_list('id', flat=True)

        if question.is_get_score(question_selected_ids):
            total_score += question.grade

    percentage = round((total_score / maximum_score) * 100) if maximum_score else 0

    context = {
        'course': course,
        'grade': percentage,
        'choices': choices,
        'selected_ids': selected_ids,
    }

    return render(
        request,
        'onlinecourse/exam_result_bootstrap.html',
        context
    )
