from django.urls import path
from .views import *

app_name = 'news'

urlpatterns = [
    # path -- означает путь. В данном случае путь ко всем товарам у нас останется пустым, позже станет ясно почему
    path('', PostList.as_view(), name='home'),
    # т.к. сам по себе это класс, то нам надо представить этот класс в виде view. Для этого вызываем метод as_view
    path('<int:pk>', PostDetailView.as_view(), name='post_detail'),
    path('search/', SearchList.as_view(), name='search'),
    path('news/add/', PostCreateView.as_view(), name='post_create'),
    path('news/<int:pk>/edit/', PostUpdateView.as_view(), name='post_update'),
    path('news/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete')
]