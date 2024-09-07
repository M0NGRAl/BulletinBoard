from django.db.models.signals import post_save
from django.core.mail import send_mail
from .models import Advertisement, Subscription
from django.contrib.auth.models import User
from allauth.account.signals import user_signed_up
from django.dispatch import receiver
from django.contrib.auth.models import Group

@receiver(post_save, sender=Advertisement)
def send_subscription_email(sender, instance, created, **kwargs):
    if created:
        category = instance.category
        # Находим всех пользователей, подписанных на эту категорию
        subscriptions = Subscription.objects.filter(category=category)
        emails = [subscription.user.email for subscription in subscriptions if subscription.user.email]

        if emails:
            send_mail(
                subject=f'Новое объявление в категории {category}',
                message=f'Новое объявление "{instance.heading}" было добавлено в категорию {category}.',
                from_email='no-reply@example.com',  # Замените на ваш email
                recipient_list=emails,
                fail_silently=False,
            )



@receiver(user_signed_up)
def add_user_to_group(sender, request, user, **kwargs):
    # Получаем группу, в которую нужно добавить пользователя
    group, created = Group.objects.get_or_create(name='common users')

    # Добавляем пользователя в группу
    user.groups.add(group)