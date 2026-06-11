from django.test import TestCase
from django.urls import reverse
from .models import Student, Subject, Grade

class StudentModelTest(TestCase):
    def test_student_creation(self):
        student = Student.objects.create(student_id='001', full_name='Иванов Иван')
        self.assertEqual(student.full_name, 'Иванов Иван')
        self.assertEqual(str(student), '001 - Иванов Иван')

class SubjectModelTest(TestCase):
    def test_subject_creation(self):
        subject = Subject.objects.create(name='Математика')
        self.assertEqual(subject.name, 'Математика')
        self.assertEqual(str(subject), 'Математика')

class GradeModelTest(TestCase):
    def test_grade_creation(self):
        student = Student.objects.create(student_id='001', full_name='Иванов Иван')
        subject = Subject.objects.create(name='Математика')
        grade = Grade.objects.create(student=student, subject=subject, value=5)
        self.assertEqual(grade.value, 5)
        self.assertEqual(str(grade), 'Иванов Иван - Математика: 5')

class IndexViewTest(TestCase):
    def setUp(self):
        self.student = Student.objects.create(student_id='001', full_name='Иванов Иван')
        self.subject = Subject.objects.create(name='Математика')
        Grade.objects.create(student=self.student, subject=self.subject, value=5)

    def test_index_view(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Иванов Иван')
        self.assertContains(response, 'Матем')

    def test_sort_best(self):
        response = self.client.get(reverse('index') + '?sort=best')
        self.assertEqual(response.status_code, 200)

    def test_sort_worst(self):
        response = self.client.get(reverse('index') + '?sort=worst')
        self.assertEqual(response.status_code, 200)

class StudentCreateViewTest(TestCase):
    def test_create_student(self):
        self.client.post(reverse('student_create'), {'full_name': 'Петров Петр'})
        self.assertEqual(Student.objects.count(), 1)

class SubjectCreateViewTest(TestCase):
    def test_create_subject(self):
        self.client.post(reverse('subject_create'), {'name': 'Физика'})
        self.assertEqual(Subject.objects.count(), 1)

class StudentUpdateViewTest(TestCase):
    def setUp(self):
        self.student = Student.objects.create(student_id='001', full_name='Иванов Иван')

    def test_update_student(self):
        self.client.post(reverse('student_update', args=[self.student.pk]), {'full_name': 'Иванов Петр'})
        self.student.refresh_from_db()
        self.assertEqual(self.student.full_name, 'Иванов Петр')

class StudentDeleteViewTest(TestCase):
    def setUp(self):
        self.student = Student.objects.create(student_id='001', full_name='Иванов Иван')

    def test_delete_student(self):
        self.client.post(reverse('student_delete', args=[self.student.pk]))
        self.assertEqual(Student.objects.count(), 0)

class SubjectUpdateViewTest(TestCase):
    def setUp(self):
        self.subject = Subject.objects.create(name='Математика')

    def test_update_subject(self):
        self.client.post(reverse('subject_update', args=[self.subject.pk]), {'name': 'Высшая математика'})
        self.subject.refresh_from_db()
        self.assertEqual(self.subject.name, 'Высшая математика')

class SubjectDeleteViewTest(TestCase):
    def setUp(self):
        self.subject = Subject.objects.create(name='Математика')

    def test_delete_subject(self):
        self.client.post(reverse('subject_delete', args=[self.subject.pk]))
        self.assertEqual(Subject.objects.count(), 0)

class StudentUpdateGradesTest(TestCase):
    def setUp(self):
        self.student = Student.objects.create(student_id='001', full_name='Иванов Иван')
        self.subject = Subject.objects.create(name='Математика')

    def test_update_student_with_grade(self):
        self.client.post(reverse('student_update', args=[self.student.pk]), {
            'full_name': 'Иванов Петр',
            f'subject_{self.subject.id}': '5'
        })
        self.student.refresh_from_db()
        self.assertEqual(self.student.full_name, 'Иванов Петр')
        self.assertTrue(Grade.objects.filter(student=self.student, subject=self.subject).exists())

    def test_update_student_delete_grade(self):
        Grade.objects.create(student=self.student, subject=self.subject, value=4)
        self.client.post(reverse('student_update', args=[self.student.pk]), {
            'full_name': 'Иванов Иван',
            f'subject_{self.subject.id}': ''
        })
        self.assertEqual(Grade.objects.filter(student=self.student).count(), 0)