from allauth.account.signals import email_confirmed
from django.core.mail import EmailMultiAlternatives, send_mail
from django.db.models.signals import post_save, m2m_changed
from django.core.signals import request_finished
from django.dispatch import receiver  # импортируем нужный декоратор
from django.template.loader import render_to_string

from .models import Post, Category


@receiver(m2m_changed, sender=Post.category.through)
def update_post(sender, **kwargs):
    instance = kwargs.pop('instance', None)
    categories = kwargs['pk_set']  # Категории добавленного поста
    if kwargs.get('action') == 'post_add':
        # получем наш html
        html_content = render_to_string(
            'news/subs_users.html',
            {
                'data': instance,
            }
        )
        for value in categories:
            category = Category.objects.get(id=value)  # Обьект Категории
            subscribers = category.subscribers.all()  # Подписчики одной категории
            for data in subscribers:
                msg = EmailMultiAlternatives(
                    subject=f'Здравствуй, {data.username} Новая статья в твоём любимом разделе!»',
                    body=instance.text,
                    from_email='alexei.chavlitko@yandex.ru',
                    to=[data.email]
                )
                print('Сообщение сформировано')
                msg.attach_alternative(html_content, "text/html")  # добавляем html
                print('Добавлен html')
                msg.send()
                print('Сообщение отправлено')
                print('--------------')

@receiver(email_confirmed)
def user_signed_up_(request, email_address, **kwargs):
    send_mail(
        "Привет!",
        "Добро пожаловать на новостной портал!",
        "alexei.chavlitko@yandex.ru",
        [email_address],
        fail_silently=False,
    )

