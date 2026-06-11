# students/views.py
from collections import defaultdict
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic import CreateView
from .models import Grade, Subject, Student


class IndexView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)

        subjects = Subject.objects.all().order_by('name')
        students = Student.objects.all()

        student_grades = defaultdict(dict)
        for grade in Grade.objects.all():
            student_grades[grade.student][grade.subject] = grade.value

        student_statistics = []
        for student in students:
            scores = []
            for subject in subjects:
                score = student_grades.get(student, {}).get(subject)
                if score is not None:
                    if score.is_integer():
                        scores.append(f'{int(score)}')
                    else:
                        scores.append(f'{score:.1f}')
                else:
                    scores.append('-')
            student_statistics.append({
                'student': student,
                'scores': scores
            })

        context.update({
            'subjects': subjects,
            'student_statistics': student_statistics
        })
        return context


class StudentCreateView(CreateView):
    model = Student
    fields = ['student_id', 'full_name']
    template_name = 'students/student_form.html'
    success_url = reverse_lazy('index')