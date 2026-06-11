# views.py
from collections import defaultdict
from django.views.generic.base import TemplateView
from .models import Grade

class IndexView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        grades = Grade.objects.all()
        student_grades = defaultdict(dict)

        subjects = set()
        for grade in grades:
            subject_name = grade.subject.name
            subjects.add(subject_name)
            student_grades[grade.student][subject_name] = grade.value

        subjects = sorted(subjects)
        student_statistics = [
            {
                'student': student,
                'scores': [f'{grades[subject]:.1f}' for subject in subjects]
            }
            for student, grades in student_grades.items()
        ]
        context.update(
            {
                'subjects': subjects,
                'student_statistics': student_statistics
            }
        )
        return context