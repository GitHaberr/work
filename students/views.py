from collections import defaultdict
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic import CreateView
from .models import Grade, Subject, Student
from django.views.generic import DeleteView
from django.views.generic import UpdateView

from django.shortcuts import redirect


class IndexView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)

        subjects = Subject.objects.all().order_by("name")
        students = Student.objects.all().order_by("full_name")

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
                        scores.append(f"{int(score)}")
                    else:
                        scores.append(f"{score:.1f}")
                else:
                    scores.append("-")

            total_subjects = Subject.objects.count()
            student_scores = [g.value for g in Grade.objects.filter(student=student)]
            if student_scores:
                avg = sum(student_scores) / total_subjects
                avg_display = f"{avg:.2f}"
            else:
                avg_display = "-"

            student_statistics.append(
                {"student": student, "scores": scores, "average": avg_display}
            )

        sort = self.request.GET.get("sort")
        if sort == "best":
            student_statistics.sort(
                key=lambda x: float(x["average"]) if x["average"] != "-" else -1,
                reverse=True,
            )
        elif sort == "worst":
            student_statistics.sort(
                key=lambda x: float(x["average"]) if x["average"] != "-" else 999
            )

        context.update(
            {
                "subjects": subjects,
                "student_statistics": student_statistics,
                "current_sort": self.request.GET.get("sort", "default"),
            }
        )
        return context


class SubjectCreateView(CreateView):
    model = Subject
    fields = ["name"]
    template_name = "subject/subject_form.html"
    success_url = reverse_lazy("index")


class SubjectUpdateView(UpdateView):
    model = Subject
    fields = ["name"]
    template_name = "subject/subject_form.html"
    success_url = reverse_lazy("index")


class SubjectDeleteView(DeleteView):
    model = Subject
    template_name = "subject/subject_delete.html"
    success_url = reverse_lazy("index")


class StudentCreateView(CreateView):
    model = Student
    fields = ["full_name"]
    template_name = "students/student_form.html"
    success_url = reverse_lazy("index")


class StudentUpdateView(UpdateView):
    model = Student
    fields = ["full_name"]
    template_name = "students/student_update.html"
    success_url = reverse_lazy("index")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_subjects = Subject.objects.all().order_by("name")
        existing_grades = {
            g.subject_id: g for g in Grade.objects.filter(student=self.object)
        }

        grades_data = []
        for subject in all_subjects:
            grade = existing_grades.get(subject.id)
            grades_data.append(
                {"subject": subject, "value": grade.value if grade else ""}
            )

        context["grades_data"] = grades_data
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.full_name = request.POST["full_name"]
        self.object.save()

        for key, value in request.POST.items():
            if key.startswith("subject_"):
                subject_id = key.split("_")[1]
                if value:
                    grade, created = Grade.objects.get_or_create(
                        student=self.object,
                        subject_id=subject_id,
                        defaults={"value": float(value)},
                    )
                    if not created:
                        grade.value = float(value)
                        grade.save()
                else:
                    Grade.objects.filter(
                        student=self.object, subject_id=subject_id
                    ).delete()

        return redirect("index")


class StudentDeleteView(DeleteView):
    model = Student
    template_name = "students/student_delete.html"
    success_url = reverse_lazy("index")
