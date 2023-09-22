from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import Group
from django.core.cache import cache
from django.core.mail import EmailMultiAlternatives, send_mail
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .forms import NewsForm
from .models import *
from .sample_app.filters import PostFilter
import logging
from django.db.models.signals import post_save

logger = logging.getLogger(__name__)


class CategoryList(ListView):
    model = Category
    template_name = 'news/news_category.html'
    queryset = Category.objects.all()
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super(CategoryList, self).get_context_data(**kwargs)
        category_id = self.kwargs.get('pk', None)
        context['is_not_authors'] = not self.request.user.groups.filter(name='authors').exists()
        context['news'] = Post.objects.filter(category=category_id)
        context['category'] = Category.objects.all()
        context['category_id'] = category_id
        context['category_subscribe'] = Category.objects.filter(subscribers__username=self.request.user.username)
        context['if_not_subscribe'] = Category.objects.filter(subscribers__category=category_id,
                                                              subscribers__username=self.request.user.username)
        return context


class PostList(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'news/news.html'
    context_object_name = 'news'
    queryset = Post.objects.order_by('-time_create')
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_authors'] = not self.request.user.groups.filter(name='authors').exists()
        context['category'] = Category.objects.all()
        context['category_subscribe'] = Category.objects.filter(subscribers__username=self.request.user.username)
        return context


# login Required Mixin add
class DetailPost(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'news/concrete_news.html'
    context_object_name = 'news'


class SearchList(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'news/search.html'
    context_object_name = 'news'
    queryset = Post.objects.order_by('-time_create')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET,
                                       queryset=self.get_queryset())
        return context


class PostDetailView(LoginRequiredMixin, DetailView):
    template_name = 'news/news_detail.html'
    queryset = Post.objects.all()

    def get_object(self, *args, **kwargs):  # переопределяем метод получения объекта, как ни странно
        obj = cache.get(f'news{self.kwargs["pk"]}',
                        None)  # кэш очень похож на словарь, и метод get действует также. Он забирает значение по
        # ключу, если его нет, то забирает None.
        # если объекта нет в кэше, то получаем его и записываем в кэш
        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'news{self.kwargs["pk"]}', obj)

        return obj


class PostCreateView(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    template_name = 'news/news_create.html'
    form_class = NewsForm
    success_url = reverse_lazy(
        'news:home')

    def post(self, request, *args, **kwargs):
        author = Author.objects.get(id=request.POST['author'])
        post = Post(
            author=author,
            choice=request.POST['choice'],
            header=request.POST['header'],
            text=request.POST['text'],
        )
        # Число созданных постов за сегодня
        post_author_count = Post.objects.filter(author_id=author.id, time_create__date=timezone.now()).count()
        if post_author_count <= 3:
            post.save()
            logger.warning(f'Post created by {author}, id - {post}')

            categoryes = request.POST.getlist('category')
            for cat in categoryes:
                cat_obj = Category.objects.get(id=cat)
                post.category.add(cat_obj)

            return redirect('news:post_create')
        else:
            logger.info(f'Post creation limit exceeded by - {author}')
            return redirect('news:erorr')


class PostUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
    template_name = 'news/news_create.html'
    form_class = NewsForm
    success_url = reverse_lazy(
        'news:home')

    # метод get_object мы используем вместо queryset, чтобы получить информацию об объекте который мы собираемся редактировать
    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


# дженерик для удаления товара
class PostDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_post',)
    template_name = 'news/news_delete.html'
    queryset = Post.objects.all()
    success_url = reverse_lazy(
        'news:home')


# Добавляем функциональное представление для повышения привилегий пользователя до членства в группе authors


@login_required
def upgrade_me(request):
    user = request.user
    premium_group = Group.objects.get(name='authors')

    if not request.user.groups.filter(name='authors').exists():
        Author.objects.create(user=user)
        premium_group.user_set.add(user)
    return redirect('/')


def subscribe_category(request, category_id):
    user = request.user.id
    category = Category.objects.get(id=category_id)
    if not Category.objects.filter(subscribers__username=user).exists():
        category.subscribers.add(user)
    return redirect(f'/{category_id}/category/')


def error(request):
    return HttpResponse("Превишен лимит создания постов", status=400, reason="Limits")
