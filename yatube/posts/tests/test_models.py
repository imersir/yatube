from django.contrib.auth import get_user_model
from django.test import TestCase

from ..models import Group, Post

User = get_user_model()


# Тест модели приложения posts в Yatube.
class PostGroupModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.group = Group.objects.create(title='Тестовый текст')
        cls.post = Post.objects.create(
            text='T' * 20,
            author=User.objects.create(username='Test', password='1234',
                                       email='test@test.ru')
        )

    # Post — первые пятнадцать символов поста:post.text[:15]
    def test_str_post(self):
        posts = PostGroupModelTest.post
        expected_object_name = posts.text[:15]
        self.assertEqual(expected_object_name, str(posts))

    # для класса Group — название группы.
    def test_str_group(self):
        groups = PostGroupModelTest.group
        expected_object_name = groups.title
        self.assertEqual(expected_object_name, str(groups))
