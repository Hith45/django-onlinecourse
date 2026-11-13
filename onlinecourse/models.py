from django.db import models
from django.utils.timezone import now
from django.conf import settings




class Instructor(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    full_time = models.BooleanField(default=True)
    total_learners = models.IntegerField()

    def __str__(self):
        return self.user.username


class Learner(models.Model):
    STUDENT = 'student'
    DEVELOPER = 'developer'
    DATA_SCIENTIST = 'data_scientist'
    DATABASE_ADMIN = 'dba'

    OCCUPATION_CHOICES = [
        (STUDENT, 'Student'),
        (DEVELOPER, 'Developer'),
        (DATA_SCIENTIST, 'Data Scientist'),
        (DATABASE_ADMIN, 'Database Admin')
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    occupation = models.CharField(
        max_length=20,
        choices=OCCUPATION_CHOICES,
        default=STUDENT
    )
    social_link = models.URLField(max_length=200)

    def __str__(self):
        return self.user.username + "," + self.occupation

class Course(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    pub_date = models.DateTimeField(default=now)

    def __str__(self):
        return self.name


class Lesson(models.Model):
    title = models.CharField(max_length=200)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    content = models.TextField()

    def __str__(self):
        return self.title


class Enrollment(models.Model):
    AUDIT = 'audit'
    HONOR = 'honor'
    COURSE_MODES = [
        (AUDIT, 'Audit'),
        (HONOR, 'Honor'),
    ]
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    mode = models.CharField(max_length=10, choices=COURSE_MODES, default=AUDIT)

    def __str__(self):
        return f"{self.user.username} - {self.course.name}"


class Question(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    question_text = models.CharField(max_length=200)
    grade = models.IntegerField(default=1)

    def __str__(self):
        return self.question_text

    def is_get_score(self, selected_choices):
        correct_choices = set(
            self.choice_set.filter(is_correct=True).values_list('id', flat=True)
        )
        selected_choices = set(selected_choices)
        return correct_choices == selected_choices


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.choice_text


class Submission(models.Model):
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE)
    choices = models.ManyToManyField(Choice)

    def __str__(self):
        return f"Submission {self.id} for {self.enrollment}"