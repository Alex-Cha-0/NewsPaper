from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .forms import NewsForm
from .models import *
from .sample_app.filters import PostFilter


class PostList(ListView):
    model = Post
    template_name = 'news/news.html'
    context_object_name = 'news'
    queryset = Post.objects.order_by('-time_create')
    paginate_by = 10



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
