from django.shortcuts import render

from django.views.generic import ListView, DetailView
from .models import *


class PostList(ListView):
    model = Post
    template_name = 'news/news.html'
    context_object_name = 'news'
    queryset = Post.objects.order_by('-time_create')





class DetailPost(DetailView):
    model = Post
    template_name = 'news/concrete_news.html'
    context_object_name = 'news'
