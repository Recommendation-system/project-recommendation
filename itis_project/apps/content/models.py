from time import time

from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import reverse
from django.utils.text import slugify


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True, related_name='users',
                                verbose_name='Пользователь')
    registration_date = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Зарегестрирован')
    course_number = models.IntegerField(default=1, verbose_name="Курс")

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = 'Профили'
        verbose_name = 'Профиль'
        ordering = ['user']


class Subject(models.Model):
    name = models.CharField(max_length=25, db_index=True, verbose_name='Предмет')
    course_number = models.IntegerField(default=1, verbose_name="Курс")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Предметы'
        verbose_name = 'Предмет'
        ordering = ['name']


class Post(models.Model):
    slug = models.CharField(max_length=100, unique=True)
    author = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='Автор')
    title = models.TextField(max_length=50, verbose_name="Название")
    content = models.TextField(verbose_name='Тело')
    subject = models.ForeignKey(Subject, null=True, on_delete=models.PROTECT, verbose_name='Предмет')
    published = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Опубликовано')
    likes = models.ManyToManyField(User, default=None, blank=True, related_name='likes')

    def get_absolute_url(self):
        return reverse('post_detail_url', kwargs={'post_slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.id:
            new_slug = slugify(self.title, allow_unicode=True)
            new_slug += '-' + (str(int(time())))
            self.slug = new_slug

        super().save(*args, **kwargs)

    def total_likes(self):
        return self.likes.count()

    class Meta:
        verbose_name_plural = 'Посты'
        verbose_name = 'Пост'
        ordering = ['-published']


LIKE_CHOICES = (
    ('Like', 'Like'),
    ('Unlike', 'Unlike'),
)


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    value = models.CharField(choices=LIKE_CHOICES, default='Like', max_length=10)

    def __str__(self):
        return str(self.post)
