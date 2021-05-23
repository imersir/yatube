from django.test import Client, TestCase
from django.urls import reverse


# приложение About
class AboutTest(TestCase):
    def setUp(self):
        self.guest_client = Client()

    # страница /about/author/ доступна неавторизованному пользователю
    def test_about_author_page_accessible_by_name(self):
        response = self.guest_client.get(reverse('about:author'))
        self.assertEqual(response.status_code, 200)

    # страница /about/tech/ доступна неавторизованному пользователю
    def test_about_tech_page_accessible_by_name(self):
        response = self.guest_client.get(reverse('about:tech'))
        self.assertEqual(response.status_code, 200)
