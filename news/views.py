from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import Group
from django.core.mail import EmailMultiAlternatives, send_mail
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .forms import NewsForm
from .models import *
from .sample_app.filters import PostFilter

from django.db.models.signals import post_save




class CategoryList(ListView):
    model = Category
    template_name = 'news/news_category.html'
    queryset = Category.objects.all()
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(CategoryList, self).get_context_data(**kwargs)
        category_id = self.kwargs.get('pk', None)
        context['is_not_authors'] = not self.request.user.groups.filter(name='authors').exists()
        context['news'] = Post.objects.filter(category=category_id)
        context['category'] = Category.objects.all()
        context['category_id'] = category_id
        context['category_subscribe'] = Category.objects.filter(subscribers__username=self.request.user.username)
        return context


class PostList(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'news/news.html'
    context_object_name = 'news'
    queryset = Post.objects.order_by('-time_create')
    paginate_by = 10

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
        post.save()
        data = dict(request.POST)
        print(data)
        # Данные созданного поста
        # data = dict(request.POST)
        # print(data)
        # # Подписчики категории созданного поста
        # subcribs = {}
        # # Получаем подписчиков категорий добавленной новости.
        # for value in data['category']:
        #     category = Category.objects.get(id=value)
        #     subscribers = category.subscribers.all()
        #     subcribs[category] = subscribers
        #
        # # получем наш html
        # html_content = render_to_string(
        #     'news/subs_users.html',
        #     {
        #         'data': post,
        #     }
        # )
        #
        # # Алгоритм отправки сообщений подписчикам категорий!
        # seq = 0
        # for category in subcribs:
        #     print('Добавление поста в категорию')
        #     post.category.add(category)
        #     print(f'Пост добавлен в категорию - {category}')
        #     subscriber = category.subscribers.values('username', 'email')
        #     for subsc in subscriber:
        #         print(subsc)
        #         print(
        #             f'Получен подписчик на категорию - {category} - {subsc["username"]}, {subsc["email"]}')
        #         print('Отправка оповещения о добавления новой статьи в любимой категории')
        #
        #         msg = EmailMultiAlternatives(
        #             subject=f'Здравствуй, {subsc["username"]} Новая статья в твоём любимом разделе!»',
        #             body=str(data['text']),
        #             from_email='alexei.chavlitko@yandex.ru',
        #             to=[subsc["email"]]
        #         )
        #         print('Сообщение сформировано')
        #         msg.attach_alternative(html_content, "text/html")  # добавляем html
        #         print('Добавлен html')
        #         msg.send()
        #         print('Сообщение отправлено')
        #         print('--------------')
        #
        #     seq += 1

        return redirect('news:post_create')


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
        'news:home')  # не забываем импортировать функцию reverse_lazy из пакета django.urls


# Добавляем функциональное представление для повышения привилегий пользователя до членства в группе authors
@login_required
def upgrade_me(request):
    user = request.user
    premium_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        premium_group.user_set.add(user)
    return redirect('/')


def subscribe_category(request, category_id):
    user = request.user.id
    category = Category.objects.get(id=category_id)
    if not Category.objects.filter(subscribers__username=user).exists():
        category.subscribers.add(user)
    return redirect('/')
