from django.db import models
from django.db.models import Avg

class Student(models.Model):
    student_id = models.CharField(max_length=20)
    full_name = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.student_id} - {self.full_name}'

    def average_score(self):
        avg = self.grade_set.aggregate(Avg('value'))['value__avg']
        return avg if avg else 0

class Subject(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Grade(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    value = models.FloatField()

    def __str__(self):
        return f'{self.student.full_name} - {self.subject.name}: {self.value}'