import logging

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.mail import send_mail, EmailMultiAlternatives
from django.core.management.base import BaseCommand
from django.template.loader import render_to_string
from django.utils import timezone
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from news.models import Post

logger = logging.getLogger(__name__)


# наша задача по выводу текста на экран
def my_job():
    print('Show records created in the database for the week')
    start_date = timezone.now() - timezone.timedelta(days=7)
    end_date = timezone.now()
    weekly_records = Post.objects.filter(time_create__range=[start_date, end_date]).values('id', 'text', 'header',
                                                                                           'category__subscribers__username',
                                                                                           'category__subscribers__email')
    count = 0
    for data in weekly_records:

        html_content = render_to_string(
            'news/subs_users.html',
            {
                'data': data,
            }
        )
        msg = EmailMultiAlternatives(
            subject=f'Здравствуй, {data["category__subscribers__username"]} Новая статья в твоём любимом разделе!»',
            body=str(data["text"]),
            from_email='alexei.chavlitko@yandex.ru',
            to=[data["category__subscribers__email"]]
        )
        print(f'Message {count} - Сообщение сформировано для {data["category__subscribers__email"]}')
        msg.attach_alternative(html_content, "text/html")  # добавляем html
        print('Добавлен html')
        msg.send()
        print('Сообщение отправлено')
        print('--------------')
        count += 1
    print('record_shown')


# функция которая будет удалять неактуальные задачи
def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        # добавляем работу нашему задачнику
        scheduler.add_job(
            my_job,
            trigger=CronTrigger(day_of_week="0"),
            # Тоже самое что и интервал, но задача тригера таким образом более понятна django
            id="my_job",  # уникальный айди
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            # Каждую неделю будут удаляться старые задачи, которые либо не удалось выполнить, либо уже выполнять не надо.
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
