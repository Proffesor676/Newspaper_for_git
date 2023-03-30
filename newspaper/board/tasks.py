from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.template.loader import render_to_string
from newspaper.news.models import PostCategory
from django.conf import settings

@shared_task
def send_notifications (Preview, pk, title, subscribers):
    html_content = render_to_string(
        'post_created_email.html',
        {
            'text' : Preview,
            'link' : f'{settings.SITE_URL}/news/{pk}',
        }
    )
    msg = EmailMultiAlternatives(
        subject=title,
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers

    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()

@shared_task
@receiver(m2m_changed, sender=PostCategory)
def notify_about_new_post(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        categories = instance.postCategory.all()
        subscribers = []
        for category in categories:
            subscribers += category.subscribers.all()

        subscribers = [s.email for s in subscribers]

        send_notifications(instance.Preview(), instance.pk, instance.title, subscribers)