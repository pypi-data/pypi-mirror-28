from datetime import timedelta

from django.urls import reverse
from django.utils import timezone
from django.test import TestCase

from .models import Question


class TestQuestionModel(TestCase):

    def test_was_published_recently(self):
        delta = timedelta(hours=23,minutes=59,seconds=59)
        q = Question(pub_date=timezone.now() - delta)
        self.assertIs(q.was_published_recently(), True)

        delta = timedelta(hours=24)
        q = Question(pub_date=timezone.now() - delta)
        self.assertIs(q.was_published_recently(), False)

        q = Question(pub_date=timezone.now() + delta)
        self.assertIs(q.was_published_recently(), False)


class TestQuestionPubdate(TestCase):

    def test_future_question(self):
        time = timedelta(days=4) + timezone.now()
        q = Question.objects.create(question_text="future question", pub_date=time)
        url = reverse('polls:index')
        response = self.client.get(url)
        self.assertQuerysetEqual(response.context['latest_questions'], [])

    def test_past_question(self):
        time =  timezone.now() - timedelta(days=4)
        q = Question.objects.create(question_text="past question", pub_date=time)
        url = reverse('polls:index')
        response = self.client.get(url)
        self.assertQuerysetEqual(response.context['latest_questions'],
                                 ['<Question: past question>'])

    def test_future_question_detail(self):
        time = timedelta(days=4) + timezone.now()
        q = Question.objects.create(question_text="future question", pub_date=time)
        url = reverse('polls:detail', args=(q.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
