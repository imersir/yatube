from django.test import Client, TestCase
from django.urls import reverse


class StaticViewsTests(TestCase):
    def setUp(self):
        self.guest_client = Client()

    # для страницы /about/author/ применяются ожидаемые view-функции и шаблоны.
    def test_about_author_page_uses_correct_template(self):
        response = self.guest_client.get(reverse('about:author'))
        self.assertTemplateUsed(response, 'about/author.html')

    # для страницы /about/tech/ применяются ожидаемые view-функции и шаблоны.
    def test_about_tech_page_uses_correct_template(self):
        response = self.guest_client.get(reverse('about:tech'))
        self.assertTemplateUsed(response, 'about/tech.html')
