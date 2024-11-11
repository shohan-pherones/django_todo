from django.test import TestCase
from django.contrib.auth.models import User
from .models import Task
from django.urls import reverse


class TaskModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser')
        self.task = Task.objects.create(
            user=self.user,
            title='Test Task',
            description='This is a test task.',
            complete=False
        )

    def test_task_creation(self):
        self.assertEqual(self.task.title, 'Test Task')
        self.assertEqual(self.task.description, 'This is a test task.')
        self.assertFalse(self.task.complete)
        self.assertEqual(str(self.task), 'Test Task')

    def test_task_ordering(self):
        Task.objects.create(user=self.user, title='Incomplete Task')
        Task.objects.create(
            user=self.user, title='Complete Task', complete=True)
        tasks = Task.objects.all()
        self.assertEqual(tasks[0].complete, False)


class TaskListViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser')
        Task.objects.create(user=self.user, title='Task 1')
        Task.objects.create(user=self.user, title='Task 2')

    def test_task_list_view_status_code(self):
        response = self.client.get(reverse('tasks'))
        self.assertEqual(response.status_code, 200)

    def test_task_list_view_template(self):
        response = self.client.get(reverse('tasks'))
        self.assertTemplateUsed(response, 'base/task_list.html')

    def test_task_list_view_context(self):
        response = self.client.get(reverse('tasks'))
        self.assertTrue('tasks' in response.context)
        self.assertEqual(len(response.context['tasks']), 2)


class TaskDetailViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser')
        self.task = Task.objects.create(
            user=self.user, title='Task Detail Test')

    def test_task_detail_view_status_code(self):
        response = self.client.get(reverse('task', args=[self.task.id]))
        self.assertEqual(response.status_code, 200)

    def test_task_detail_view_template(self):
        response = self.client.get(reverse('task', args=[self.task.id]))
        self.assertTemplateUsed(response, 'base/task.html')

    def test_task_detail_view_context(self):
        response = self.client.get(reverse('task', args=[self.task.id]))
        self.assertTrue('task' in response.context)
        self.assertEqual(response.context['task'].title, 'Task Detail Test')
