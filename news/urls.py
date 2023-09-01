from django.urls import path
from .views import *

app_name = 'news'

urlpatterns = [
    # path -- означает путь. В данном случае путь ко всем товарам у нас останется пустым, позже станет ясно почему
    path('', PostList.as_view(), name='home'),
    # т.к. сам по себе это класс, то нам надо представить этот класс в виде view. Для этого вызываем метод as_view
    path('<int:pk>', PostDetailView.as_view(), name='post_detail'),
    path('search/', SearchList.as_view(), name='search'),
    path('add/', PostCreateView.as_view(), name='post_create'),
    path('<int:pk>/edit/', PostUpdateView.as_view(), name='post_update'),
    path('<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
    path('upgrade/', upgrade_me, name='upgrade'),
    path('<int:pk>/category/', CategoryList.as_view(), name='category'),
    path('<category_id>/subscribe/', subscribe_category, name='subscribe_category'),
]
