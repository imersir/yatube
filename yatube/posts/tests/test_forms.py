import shutil
import tempfile

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase
from django.urls import reverse

from ..forms import PostForm
from ..models import Group, Post, User


class PostFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create(username='leo2')
        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.user)

        cls.group = Group.objects.create(
            title='Заголовок',
            slug='slug',
        )
        cls.post = Post.objects.create(
            text='Текст',
            author=cls.user,
            group=cls.group,
        )

    # 1. проверки формы создания нового поста (страница /new/)
    # 2. если указать группу, то пост появляется на глав. странице
    def test_create_post(self):
        """Валидная форма создает запись в Post."""
        post_count = Post.objects.count()
        form_data = {
            'text': 'Текст',
            'group': self.group.id
        }
        # Отправляем POST-запрос
        response = self.authorized_client.post(reverse('new_post'),
                                               data=form_data, )
        self.assertRedirects(response, reverse('index'))
        self.assertEqual(Post.objects.count(), post_count + 1)
        self.assertTrue(
            Post.objects.filter(text='Текст', group=self.group.id).exists())

    # проверка, что при редактировании поста через форму на странице
    # /<username>/<post_id>/edit/ изменяется соответствующая запись.
    def test_post_edit_form(self):
        """Редактирование поста"""
        form_data = {
            'text': 'Меняю текст',
            'group': self.group.id
        }
        self.authorized_client.post(reverse('post_edit',
                                            kwargs={'username': 'leo2',
                                                    'post_id': self.post.id}),
                                    data=form_data)
        self.assertEqual(Post.objects.get(id=1).text, form_data['text'])


# (Спринт 6) При отправке поста с картинкой,создаётся запись в БД.
class PostFormImageTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        settings.MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)

        cls.user = User.objects.create(username='leo')
        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.user)

        cls.group = Group.objects.create(
            title='Заголовок',
            slug='slug'
        )
        cls.post = Post.objects.create(
            author=cls.user,
            group=cls.group,
            text='Текст',
        )
        cls.form = PostForm()

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(settings.MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()

    def test_create_new_posts(self):
        count = Post.objects.count()

        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x02\x00'
            b'\x01\x00\x80\x00\x00\x00\x00\x00'
            b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
            b'\x00\x00\x00\x2C\x00\x00\x00\x00'
            b'\x02\x00\x01\x00\x00\x02\x02\x0C'
            b'\x0A\x00\x3B'
        )
        uploaded = SimpleUploadedFile(
            name='small.gif',
            content=small_gif,
            content_type='image/gif'
        )
        form_data = {
            'title': self.group.title,
            'text': self.post.text,
            'author': self.post.author,
            'image': uploaded,
        }

        response = self.authorized_client.post(
            reverse('new_post'),
            data=form_data,
        )
        self.assertRedirects(response, reverse('index'))
        self.assertEqual(Post.objects.count(), count + 1)
        self.assertTrue(
            Post.objects.filter(
                author=self.post.author,
                text=self.post.text,
                group=self.group.id,
                image=self.post.image,
            ).exists()
        )
