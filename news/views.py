from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .forms import NewsForm
from .models import *
from .sample_app.filters import PostFilter


class PostList(LoginRequiredMixin,ListView):
    model = Post
    template_name = 'news/news.html'
    context_object_name = 'news'
    queryset = Post.objects.order_by('-time_create')
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_authors'] = not self.request.user.groups.filter(name='authors').exists()
        return context


# login Required Mixin add
class DetailPost(LoginRequiredMixin,DetailView):
    model = Post
    template_name = 'news/concrete_news.html'
    context_object_name = 'news'


class SearchList(LoginRequiredMixin,ListView):
    model = Post
    template_name = 'news/search.html'
    context_object_name = 'news'
    queryset = Post.objects.order_by('-time_create')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET,
                                       queryset=self.get_queryset())
        return context


class PostDetailView(LoginRequiredMixin,DetailView):
    template_name = 'news/news_detail.html'
    queryset = Post.objects.all()


class PostCreateView(LoginRequiredMixin,CreateView):
    template_name = 'news/news_create.html'
    form_class = NewsForm


class PostUpdateView(LoginRequiredMixin,UpdateView):
    template_name = 'news/news_create.html'
    form_class = NewsForm

    # метод get_object мы используем вместо queryset, чтобы получить информацию об объекте который мы собираемся редактировать
    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


# дженерик для удаления товара
class PostDeleteView(LoginRequiredMixin,DeleteView):
    template_name = 'news/news_delete.html'
    queryset = Post.objects.all()
    success_url = reverse_lazy(
        'news:home')  # не забываем импортировать функцию reverse_lazy из пакета django.urls


# Добавляем функциональное представление для повышения привилегий пользователя до членства в группе premium
@login_required
def upgrade_me(request):
   user = request.user
   premium_group = Group.objects.get(name='authors')
   if not request.user.groups.filter(name='authors').exists():
       premium_group.user_set.add(user)
   return redirect('/')