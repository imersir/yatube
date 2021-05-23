from django.test import Client, TestCase

from ..models import Group, Post, User


# Проверка доступности страниц в соответствии с правами пользователей
class IndexURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Автор
        cls.author = User.objects.create_user(username='leo1')
        cls.author_authorized = Client()
        cls.author_authorized.force_login(cls.author)

        cls.group = Group.objects.create(
            title='Заголовок',
            slug='slug',
            description='Описание'
        )
        cls.post = Post.objects.create(
            group=cls.group,
            text='Текст',
            author=cls.author,
        )

    def setUp(self):
        # Гость
        self.guest_client = Client()
        # Авторизованный клиент
        self.user = User.objects.create_user(username='leo2')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    # главная страница /
    def test_homepage(self):
        response = self.guest_client.get('/')
        self.assertEqual(response.status_code, 200)

    # страница группы /group/<slug>/
    def test_group_page(self):
        response = self.guest_client.get('/group/slug/')
        self.assertEqual(response.status_code, 200)

    # страница создания поста /new/
    def test_new_posts(self):
        response = self.authorized_client.get('/new/')
        self.assertEqual(response.status_code, 200)

    # профайла пользователя /<username>/
    def test_username(self):
        response = self.guest_client.get('/leo1/')
        self.assertEqual(response.status_code, 200)

    # отдельного поста /<username>/<post_id>/
    def test_username_post(self):
        response = self.guest_client.get('/leo1/1/')
        self.assertEqual(response.status_code, 200)

    # правильно ли работает редирект со страницы /<username>/<post_id>/edit/
    # для тех, у кого нет прав доступа к этой странице.
    def test_username_post_edit_guest(self):
        response = self.guest_client.get('/leo/1/edit/')
        self.assertRedirects(response, '/auth/login/?next=/leo/1/edit/')

    # доступность страницы редактирования поста /<username>/<post_id>/edit/
    # авторизованного пользователя — автора поста;
    def test_username_post_edit_post_author(self):
        response = self.author_authorized.get('/leo1/1/edit/')
        self.assertEqual(response.status_code, 200)

    # доступность страницы редактирования поста /<username>/<post_id>/edit/
    # авторизованного пользователя — не автора поста.
    def test_username_post_edit_authorized(self):
        response = self.authorized_client.get('/leo1/1/edit/')
        self.assertRedirects(response, '/leo1/1/')

    # Какой шаблон вызывается для страницы
    # редактирования поста /<username>/<post_id>/edit/
    def test_post_edit_url_uses_correct_template(self):
        response = self.author_authorized.get('/leo1/1/edit/')
        self.assertTemplateUsed(response, 'new.html')


# Проверка по URL - вызываются ли для них ожидаемые шаблоны
class PostGroupURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.group = Group.objects.create(
            title='Тестовый заголовок',
            slug='slug'
        )
        cls.post = Post.objects.create(
            author=User.objects.create_user(username='Test'),
            text='Тест заголовка ПОСТ'
        )

    def setUp(self):
        self.guest_client = Client()
        self.user = User.objects.create_user(username='Test2')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_urls_uses_correct_template(self):
        templates_url_names = {
            'index.html': '/',  # главная страница /
            'group.html': '/group/slug/',  # страница группы /group/<slug>/
            'new.html': '/new/',  # страница создания поста /new/
        }
        for template, adress in templates_url_names.items():
            with self.subTest(adress=adress):
                response = self.authorized_client.get(adress)
                self.assertTemplateUsed(response, template)
