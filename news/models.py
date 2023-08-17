from django.conf import settings
from django.contrib.auth.models import User

from django.db import models
from django.db.models import Sum


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating_author = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username

    def update_rating(self):
        # self.rating_author = 0
        # # queryset = Post.objects.filter(author=self.user.id)
        # post_queryset = Post.objects.filter(author=Author.objects.get(user_id=self.user.id))
        # for post_rating in post_queryset:
        #     self.rating_author = self.rating_author + post_rating.rating
        #     self.save()
        # self.rating_author = self.rating_author * 3
        # self.save()
        #
        # comm_queryset = Comment.objects.filter(user_id=self.user.id)
        # for comment_rating in comm_queryset:
        #     self.rating_author = self.rating_author + comment_rating.rating
        #     self.save()
        postRat = self.post_set.all().aggregate(postRating=Sum('rating'))
        pRat = 0
        pRat += postRat.get('postRating')

        commentRat = self.user.comment_set.all().aggregate(commentRating=Sum('rating'))
        cRAt = 0
        cRAt += commentRat.get('commentRating')

        self.rating_author = pRat * 3 + cRAt
        self.save()


class Category(models.Model):
    category = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.category


class Post(models.Model):
    news_article = 'ARC'
    news = 'NWS'

    TYPE_CHOICES = (
        (news_article, 'Article'),
        (news, 'News'),
    )
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    choice = models.CharField(max_length=4, choices=TYPE_CHOICES, default=news_article)
    time_create = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through='PostCategory')
    header = models.CharField(max_length=100)
    text = models.TextField()
    rating = models.IntegerField(default=0)

    def __str__(self):
        return f'Дата добавления - {self.time_create} - Author: {self.author} - Raiting: ' \
               f'{self.rating} - Header: {self.header} - Preview: {self.preview}'

    def post_like(self):
        self.rating = self.rating + 1
        self.save()

    def post_dislike(self):
        if self.rating == 0:
            self.rating = 0
            self.save()
        else:
            self.rating = self.rating - 1
            self.save()

    @property
    def preview(self):
        return self.text[:124] + '...'


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text_comm = models.TextField()
    date_comm = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def __str__(self):
        return f'Date: {self.date_comm} User: {self.user.username} Rating: {self.rating} Text: {self.text_comm}'

    def comment_like(self):
        self.rating = self.rating + 1
        self.save()

    def comment_dislike(self):
        if self.rating == 0:
            self.rating = 0
            self.save()
        else:
            self.rating = self.rating - 1
            self.save()
