from news.models import *
from django.contrib.auth.models import User

# Создать двух пользователей (с помощью метода User.objects.create_user).
user1 = User.objects.create_user('Alex', password='Password')
user2 = User.objects.create_user('Bob', password='Password')

# Создать два объекта модели Author, связанные с пользователями.
user_alex = User.objects.get(username='Alex')
author_alex_create = Author.objects.create(name=user_alex)

user_bob = User.objects.get(username='Bob')
author_bob_create = Author.objects.create(user=user_bob)

# Добавить 4 категории в модель Category.
category1 = Category.objects.create(category='Главное')
category2 = Category.objects.create(category='Спорт')
category3 = Category.objects.create(category='Экономика')
category4 = Category.objects.create(category='Авто')

# Добавить 2 статьи и 1 новость.
post1 = Post.objects.create(author=Author.objects.get(pk=1),
                            choice=Post.news_article,
                            header='В России резко '
                                   'возрос экспорт '
                                   'автомобилей из Японии',
                            text='Согласно данным Дальневосточного таможенного управления, '
                                 'в период с 24 июля по 6 августа частными лицами было '
                                 'ввезено в общей сложности 15 071 транспортное '
                                 'средство через таможни Дальнего Востока.Отмечается, что '
                                 'указанное число сравнимо с периодом с 1 по 14 июля, '
                                 'когда было ввезено 11 254 автомобиля. '
                                 'Это составляет приблизительно 33% увеличения ввоза'
                            )

post2 = Post.objects.create(author=Author.objects.get(pk=2),
                            choice=Post.news_article,
                            header='В Госдуме анонсировали возобновление производства автомобилей «Волга»',
                            text='После предложения Госдумы пересадить чиновников '
                                 'в России на отечественные авто, спикер Вячеслав Володин '
                                 'сообщил о возрождении сборки "Волги" в цехах нижегородского '
                                 'предприятия.'
                            )

post3 = Post.objects.create(author=Author.objects.get(pk=2),
                            choice=Post.news,
                            header='Сбер повысил ставки по базовым программам ипотеки до 11,7%',
                            text='"Сбербанк дольше всех на рынке из крупнейших банков '
                                 'удерживал ставки по ипотеке на неизменном уровне после '
                                 'повышения ключевой ставки ЦБ. Однако текущие рыночные условия '
                                 'вынуждают нас с 8 августа скорректировать ставки на 0,8 п.п. по '
                                 'базовым ипотечным программам", - сказано в сообщении.'
                            )

# Присвоить им категории (как минимум в одной статье/новости должно быть не меньше 2 категорий).
post1_category = PostCategory.objects.create(post=Post.objects.get(pk=1), category=Category.objects.get(pk=4))
post1_category2 = PostCategory.objects.create(post=Post.objects.get(pk=1), category=Category.objects.get(pk=1))

post2_category = PostCategory.objects.create(post=Post.objects.get(pk=2), category=Category.objects.get(pk=4))
post2_category2 = PostCategory.objects.create(post=Post.objects.get(pk=2), category=Category.objects.get(pk=1))

post3_category = PostCategory.objects.create(post=Post.objects.get(pk=3), category=Category.objects.get(pk=3))
post3_category3 = PostCategory.objects.create(post=Post.objects.get(pk=3), category=Category.objects.get(pk=1))

# Создать как минимум 4 комментария к разным объектам модели Post
# (в каждом объекте должен быть как минимум один комментарий).
comment_post = Comment.objects.create(post=Post.objects.get(pk=1), user=User.objects.get(pk=1),
                                      text_comm='Мне понравился '
                                                'ваш пост',
                                      )
comment_post1 = Comment.objects.create(post=Post.objects.get(pk=1), user=User.objects.get(pk=2),
                                       text_comm='Статья просто великолепная!'
                                       )
comment_post2 = Comment.objects.create(post=Post.objects.get(pk=2), user=User.objects.get(pk=1),
                                       text_comm='Я не согласен с этим!'
                                       )
comment_post3 = Comment.objects.create(post=Post.objects.get(pk=3), user=User.objects.get(pk=2),
                                       text_comm='Отлично!'
                                       )
# Применяя функции like() и dislike() к статьям/новостям и комментариям, скорректировать рейтинги этих объектов.
post1.post_like()
post1.post_like()
post1.post_like()
post2.post_like()
post2.post_like()
post2.post_like()
post3.post_like()
post2.post_dislike()
post1.post_dislike()
post3.post_dislike()
post3.post_like()
post3.post_like()

comment_post1.comment_like()
comment_post2.comment_like()
comment_post3.comment_like()
comment_post3.comment_dislike()
comment_post2.comment_like()
comment_post2.comment_like()
comment_post1.comment_like()
comment_post3.comment_like()
comment_post3.comment_dislike()
comment_post2.comment_dislike()
comment_post1.comment_dislike()

# Обновить рейтинги пользователей.
author_alex = Author.objects.get(pk=1)
author_bob = Author.objects.get(pk=2)

author_bob.update_rating()
author_alex.update_rating()

# Вывести username и рейтинг лучшего пользователя (применяя сортировку и возвращая поля первого объекта).
best_user = Author.objects.order_by('-rating_author')
print(best_user[0])

# Вывести дату добавления, username автора, рейтинг, заголовок и
# превью лучшей статьи, основываясь на лайках/дислайках к этой статье.
best_post = Post.objects.order_by('-rating')
print(best_post[0])

# Вывести все комментарии (дата, пользователь, рейтинг, текст) к этой статье.
best_post_id = best_post.values('id')[0]['id']
comment_for_post = Comment.objects.filter(post_id=best_post_id)
print(comment_for_post)
