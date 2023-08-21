from django.urls import path
from .views import ProductsList, ProductDetail, Products, ProductDetailView, ProductCreateView, ProductUpdateView, \
   ProductDeleteView

app_name = 'product'

urlpatterns = [
    path('', ProductsList.as_view(), name='products'),
    # Т.к. это класс, нам надо представить этот класс в виде view. Для этого вызываем метод as_view
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),  # Ссылка на детали товара

    path('product/create/', ProductCreateView.as_view(), name='product_create'),  # Ссылка на создание товара
    path('product/update/<int:pk>/', ProductUpdateView.as_view(), name='product_update'),
    # Ссылка на редактирование товара
    path('product/delete/<int:pk>/', ProductDeleteView.as_view(), name='product_delete'),  # Ссылка на удаеление товара
]
