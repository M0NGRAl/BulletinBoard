from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField

class Author(models.Model):
    name = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name.username  # Возвращаем имя пользователя


class Advertisement(models.Model):
    CATEGORY = [("Tanks", "Танки"),
                ("Healers", "Хилы"),
                ("DD", "ДД"),
                ("Merchants", "Торговцы"),
                ("Guild Masters", "Гилдмастеры"),
                ("Quest Givers", "Квестгиверы"),
                ("Blacksmiths", "Кузнецы"),
                ("Tanners", "Кожевники"),
                ("Potion Makers", "Зельевары"),
                ("Spell_Masters", "Мастера заклинаний")]
    category = models.CharField(max_length=20, choices=CATEGORY)
    heading = models.CharField(max_length=200)
    content = RichTextField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    time_in = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        formatted_time = self.time_in.strftime('%d %B %Y')
        return f'{self.heading}: {self.category}:{formatted_time}: {self.content}'


class Response(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    advertisement = models.ForeignKey(Advertisement, on_delete=models.CASCADE)
    text = models.TextField()
    answer = models.BooleanField(default=False)


    def __str__(self):
        return f'{self.user}:{self.advertisement}:{self.text}'

class Subscription(models.Model):
    CATEGORY = [("Tanks", "Танки"),
                ("Healers", "Хилы"),
                ("DD", "ДД"),
                ("Merchants", "Торговцы"),
                ("Guild Masters", "Гилдмастеры"),
                ("Quest Givers", "Квестгиверы"),
                ("Blacksmiths", "Кузнецы"),
                ("Tanners", "Кожевники"),
                ("Potion Makers", "Зельевары"),
                ("Spell_Masters", "Мастера заклинаний")]
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='subscriptions',
    )
    category = models.CharField(max_length=20, choices=CATEGORY)


