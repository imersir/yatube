
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import CommentForm, PostForm
from .models import Comment, Follow, Group, Post, User


def index(request):
    """Вывод на главной странице сообщества."""
    latest = Post.objects.all()
    paginator = Paginator(latest, settings.PAGINATOR_NUMBER_OF_PAGES)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'index.html', {'page': page})


def group_posts(request, slug):
    """Вывод на главной странице Группы."""
    group = get_object_or_404(Group,
                              slug=slug)  # Ошибка '404',при неравенстве URL`ов
    posts = group.posts.all()
    paginator = Paginator(posts, settings.PAGINATOR_NUMBER_OF_PAGES)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'group.html',
                  {'group': group, 'posts': posts, 'page': page})


class PostView(CreateView):
    """Generic для вывода form`ы на страницу."""
    form_class = PostForm
    success_url = reverse_lazy('index')
    template_name = 'new.html'


@login_required  # Декоратор проверки авторизации
def new_post(request):
    """Функция создания нового поста для авторизированных пользователей."""
    form = PostForm(request.POST or None)
    if form.is_valid():
        post = form.save(commit=False)  # Заполняем, но не сохраняем в БД.
        post.author = request.user
        post.save()
        return redirect('index')
    return render(request, 'new.html', {'form': form})


def profile(request, username):
    """Профиль пользователя."""
    user_r = get_object_or_404(User, username=username)
    posts = user_r.posts.all()
    follow = user_r.following.filter(user=request.user.id).exists()
    paginator = Paginator(posts, settings.PAGINATOR_NUMBER_OF_PAGES)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    flag_user = True
    if user_r == request.user:
        flag_user = False
    return render(request, 'profile.html',
                  {'user_r': user_r, 'page': page, 'paginator': paginator,
                   'follow': follow, 'flag_user': flag_user})


def post_view(request, username, post_id):
    """Просмотр постов пользователя."""
    user_r = get_object_or_404(User, username=username)
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all()
    form = CommentForm()
    return render(request, 'post.html',
                  {'user_r': user_r, 'post': post, 'comments': comments,
                   'form': form})


@login_required
def post_edit(request, username, post_id):
    """Редактирование записи."""
    post = get_object_or_404(Post, id=post_id, author__username=username)
    if post.author != request.user:
        return redirect('post', username, post_id)
    form = PostForm(request.POST or None, files=request.FILES or None,
                    instance=post)
    if form.is_valid():
        form.save()
        return redirect('post', username, post_id)
    return render(request, 'new.html',
                  {'form': form, 'post_id': post_id, 'post': post})


@login_required
def post_delete(request, username, post_id):
    """Удаление поста."""
    if request.user.username != username:
        return redirect(f'/{username}/{post_id}')
    post = get_object_or_404(Post, pk=post_id)
    post.delete()
    return redirect('profile', username=username)


@login_required
def add_comment(request, username, post_id):
    """Добавление комментария к посту."""
    post = get_object_or_404(Post, pk=post_id, author__username=username)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
        return redirect('post', username, post_id)
    return redirect('post', username, post_id)


@login_required
def comment_delete(request, username, post_id, comment_id):
    """Удаление комментария."""
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user.username == comment.author.username:
        comment.delete()
    return redirect('post', username=username, post_id=post_id)


@login_required
def follow_index(request):
    """Подписка на пользователя."""
    posts = Post.objects.filter(author__following__user=request.user)
    paginator = Paginator(posts, settings.PAGINATOR_NUMBER_OF_PAGES)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'follow.html', {'page': page})


@login_required
def profile_follow(request, username):
    """Подписка на пользователя."""
    author = get_object_or_404(User, username=username)
    if request.user != author:
        Follow.objects.get_or_create(user=request.user, author=author)
    return redirect('profile', username)


@login_required
def profile_unfollow(request, username):
    """Отписка от пользователя."""
    author = get_object_or_404(User, username=username)
    if request.user != author:
        Follow.objects.filter(user=request.user, author=author).delete()
    return redirect('profile', username)


def page_not_found(request, exception):
    # Переменная exception содержит отладочную информацию
    return render(
        request,
        'misc/404.html',
        {'path': request.path},
        status=404
    )


def server_error(request):
    return render(request, 'misc/500.html', status=500)
