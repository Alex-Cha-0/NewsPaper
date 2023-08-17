from django.contrib import admin
from .models import *


# Register your models here.

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
        'id','author', 'choice', 'time_create', 'header', 'text', 'rating')
    # list_filter = ('sender_name', 'datetime_send', 'open_order', 'close_order')
    # list_display_links = ('id', 'subject')
    # search_fields = ('subject', 'sender_name')
    fields = ('author', 'choice', 'time_create', 'header', 'text', 'rating')
    readonly_fields = ('time_create',)
    save_on_top = True


admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(PostCategory, PostCategoryAdmin)
admin.site.register(Comment, CommentAdmin)
