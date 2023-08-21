# from django.shortcuts import render
from datetime import datetime

from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import \
    ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Product
from django.core.paginator import Paginator
from product.sample_app.filters import ProductFilter
from .forms import ProductForm


class ProductsList(ListView):
    model = Product  # указываем модель, объекты которой мы будем выводить
    template_name = 'product/products.html'  # указываем имя шаблона, в котором будет лежать HTML, в нём будут все инструкции о том, как именно пользователю должны вывестись наши объекты
    context_object_name = 'products'
    queryset = Product.objects.order_by('-id')
    ordering = ['-price']  # сортировка по цене в порядке убывания
    paginate_by = 5  # поставим постраничный вывод в один элемент

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['value1'] = None
        context['filter'] = ProductFilter(self.request.GET,
                                          queryset=self.get_queryset())  # вписываем наш фильтр в контекст
        context['choices'] = Product.TYPE_CHOICES
        context['form'] = ProductForm()
        return context

    def post(self, request, *args, **kwargs):
        form = ProductForm(request.POST)  # создаём новую форму, забиваем в неё данные из POST-запроса
        if form.is_valid():  # если пользователь ввёл всё правильно и нигде не накосячил, то сохраняем новый товар
            form.save()
        return super().get(request, *args, **kwargs)


class ProductDetail(DetailView):
    model = Product
    template_name = 'product/product.html'
    context_object_name = 'product'


class Products(View):

    def get(self, request):
        products = Product.objects.order_by('-price')
        p = Paginator(products,
                      1)  # Создаём объект класса пагинатор, передаём ему список наших товаров и их количество для одной страницы
        products = p.get_page(request.GET.get('page',
                                              1))  # Берём номер страницы из get-запроса. Если ничего не передали, будем показывать первую страницу
        # Теперь вместо всех объектов в списке товаров хранится только нужная нам страница с товарами

        data = {
            'products': products,
        }

        return render(request, 'product/products.html', data)


# дженерик для получения деталей о товаре
class ProductDetailView(DetailView):
    template_name = 'product/product_detail.html'
    queryset = Product.objects.all()


# дженерик для создания объекта. Надо указать только имя шаблона и класс формы, который мы написали в прошлом юните. Остальное он сделает за вас
class ProductCreateView(CreateView):
    template_name = 'product/product_create.html'
    form_class = ProductForm


class ProductUpdateView(UpdateView):
    template_name = 'product/product_create.html'
    form_class = ProductForm

    # метод get_object мы используем вместо queryset, чтобы получить информацию об объекте который мы собираемся редактировать
    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Product.objects.get(pk=id)


# дженерик для удаления товара
class ProductDeleteView(DeleteView):
    template_name = 'product/product_delete.html'
    queryset = Product.objects.all()
    success_url = reverse_lazy(
        'product:products')  # не забываем импортировать функцию reverse_lazy из пакета django.urls
