from django.contrib import admin
from .models import *


# Register your models here.

# напишем уже знакомую нам функцию обнуления товара на складе
def nullfy_rating(modeladmin, request,
                    queryset):  # все аргументы уже должны быть вам знакомы, самые нужные из них это request — объект хранящий информацию о запросе и queryset — грубо говоря набор объектов, которых мы выделили галочками.
    queryset.update(rating=0)


nullfy_rating.short_description = 'Обнулить рейтинг'  # описание для более понятного представления в админ панеле задаётся, как будто это объект


class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'post', 'user', 'text_comm', 'date_comm', 'rating')


class PostCategoryAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'post', 'category')


class AuthorAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'user', 'user_id', 'rating_author')


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'category',)


class PostAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'author', 'choice', 'time_create', 'header', 'preview', 'rating',)
    # list_filter = ('sender_name', 'datetime_send', 'open_order', 'close_order')
    # list_display_links = ('id', 'subject')
    # search_fields = ('subject', 'sender_name')
    fields = ('author', 'choice', 'time_create', 'header', 'text', 'rating',)
    readonly_fields = ('time_create',)
    list_filter = ('author', 'time_create', 'rating',)
    search_fields = ('author', 'category__category',)
    actions = [nullfy_rating]
    save_on_top = True


admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(PostCategory, PostCategoryAdmin)
admin.site.register(Comment, CommentAdmin)
