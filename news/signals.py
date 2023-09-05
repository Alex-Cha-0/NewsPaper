from django.db.models.signals import post_save
from django.dispatch import receiver  # импортируем нужный декоратор
from .models import Post


@receiver(post_save, sender=Post)
def notify_managers_appointment(sender, instance, created, **kwargs):
    print(instance)
    print(instance.author)
    print(instance.choice)
    print(instance.category)


